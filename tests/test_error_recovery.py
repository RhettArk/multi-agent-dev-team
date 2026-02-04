# tests/test_error_recovery.py
"""Tests for error recovery system."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from utils.error_recovery import (
    ErrorRecovery,
    FailureType,
    handle_task_failure
)


class TestFailureClassification:
    """Tests for failure classification logic."""

    @pytest.fixture
    def sample_plan(self):
        """Create a sample plan for testing."""
        return {
            'plan_id': 'test-plan',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'First task',
                    'specialist': 'backend-architect',
                    'status': 'completed',
                    'dependencies': []
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Failed task',
                    'specialist': 'fastapi-specialist',
                    'status': 'failed',
                    'dependencies': ['task-1']
                },
                'task-3': {
                    'id': 'task-3',
                    'title': 'Dependent task',
                    'specialist': 'docker-specialist',
                    'status': 'pending',
                    'dependencies': ['task-2']
                }
            }
        }

    def test_classify_fixable_failure(self, sample_plan):
        """Test classification of fixable failures."""
        recovery = ErrorRecovery(sample_plan, 'task-2')

        # Test with fixable keywords
        fixable_errors = [
            Exception("Information unclear, need clarification"),
            Exception("Missing required parameter"),
            Exception("Data not found in upstream task"),
            Exception("Need more information about requirements")
        ]

        for error in fixable_errors:
            context = recovery.capture_failure_context(error)
            failure_type = recovery.classify_failure(error, context)
            assert failure_type == FailureType.FIXABLE

    def test_classify_fundamental_failure(self, sample_plan):
        """Test classification of fundamental failures."""
        recovery = ErrorRecovery(sample_plan, 'task-2')

        # Test with fundamental keywords
        fundamental_errors = [
            Exception("Impossible to implement this architecture"),
            Exception("Conflict with existing system design"),
            Exception("Incompatible with current infrastructure"),
            Exception("Cannot violate architectural constraints")
        ]

        for error in fundamental_errors:
            context = recovery.capture_failure_context(error)
            failure_type = recovery.classify_failure(error, context)
            assert failure_type == FailureType.FUNDAMENTAL

    def test_classify_by_retry_count(self, sample_plan):
        """Test that retry count affects classification."""
        recovery = ErrorRecovery(sample_plan, 'task-2')

        error = Exception("Generic error")

        # With low retry count, should be fixable
        context = recovery.capture_failure_context(error)
        context['retry_count'] = 1
        failure_type = recovery.classify_failure(error, context)
        assert failure_type == FailureType.FIXABLE

        # With max retries exceeded, should be fundamental
        context['retry_count'] = 3
        failure_type = recovery.classify_failure(error, context)
        assert failure_type == FailureType.FUNDAMENTAL


class TestFailureContext:
    """Tests for failure context capture."""

    @pytest.fixture
    def sample_plan(self):
        """Create a sample plan."""
        return {
            'plan_id': 'test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Test task',
                    'specialist': 'backend-architect',
                    'status': 'failed',
                    'dependencies': ['task-0'],
                    'retry_count': 1,
                    'output_workspace': 'work/task-1.md'
                }
            }
        }

    def test_capture_failure_context(self, sample_plan):
        """Test that failure context is captured correctly."""
        recovery = ErrorRecovery(sample_plan, 'task-1')
        error = Exception("Test error message")

        context = recovery.capture_failure_context(error)

        # Verify context structure
        assert context['task_id'] == 'task-1'
        assert context['specialist'] == 'backend-architect'
        assert context['error_message'] == 'Test error message'
        assert context['retry_count'] == 1
        assert context['dependencies'] == ['task-0']
        assert 'workspace_files' in context
        assert 'kb_state' in context


class TestFixableFailureRecovery:
    """Tests for fixable failure recovery logic."""

    @pytest.fixture
    def sample_plan(self):
        """Create plan with dependencies."""
        return {
            'plan_id': 'test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Prerequisite task',
                    'specialist': 'backend-architect',
                    'status': 'completed',
                    'dependencies': [],
                    'output_workspace': 'work/task-1.md'
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Failed task',
                    'specialist': 'fastapi-specialist',
                    'status': 'failed',
                    'dependencies': ['task-1'],
                    'retry_count': 0
                }
            }
        }

    @pytest.mark.asyncio
    async def test_handle_fixable_failure_under_retry_limit(self, sample_plan):
        """Test handling fixable failure with retries remaining."""
        recovery = ErrorRecovery(sample_plan, 'task-2')

        context = {
            'task_id': 'task-2',
            'specialist': 'fastapi-specialist',
            'error_message': 'Unclear requirement',
            'retry_count': 1,
            'dependencies': ['task-1'],
            'workspace_files': [],
            'kb_state': {}
        }

        # Mock recovery attempt
        recovery.attempt_recovery = AsyncMock(return_value=True)

        result = await recovery.handle_fixable_failure(context)

        assert result is True
        assert recovery.attempt_recovery.called
        assert sample_plan['tasks']['task-2']['retry_count'] == 2

    @pytest.mark.asyncio
    async def test_handle_fixable_failure_exceeds_retry_limit(self, sample_plan):
        """Test handling fixable failure with max retries exceeded."""
        recovery = ErrorRecovery(sample_plan, 'task-2')

        context = {
            'task_id': 'task-2',
            'specialist': 'fastapi-specialist',
            'error_message': 'Unclear requirement',
            'retry_count': 3,  # Max retries
            'dependencies': ['task-1'],
            'workspace_files': [],
            'kb_state': {}
        }

        result = await recovery.handle_fixable_failure(context)

        assert result is False

    @pytest.mark.asyncio
    async def test_attempt_recovery_with_dependencies(self, sample_plan):
        """Test recovery attempt loops back to prerequisite task."""
        recovery = ErrorRecovery(sample_plan, 'task-2')

        context = {
            'task_id': 'task-2',
            'specialist': 'fastapi-specialist',
            'error_message': 'Need clarification',
            'retry_count': 1,
            'dependencies': ['task-1'],
            'workspace_files': [],
            'kb_state': {}
        }

        # Mock get_clarification
        recovery.get_clarification = AsyncMock(return_value="Clarification response")

        result = await recovery.attempt_recovery(context)

        assert result is True
        assert recovery.get_clarification.called

    @pytest.mark.asyncio
    async def test_attempt_recovery_no_dependencies(self, sample_plan):
        """Test recovery fails when no dependencies to loop back to."""
        # Remove dependencies
        sample_plan['tasks']['task-2']['dependencies'] = []

        recovery = ErrorRecovery(sample_plan, 'task-2')

        context = {
            'task_id': 'task-2',
            'specialist': 'fastapi-specialist',
            'error_message': 'Need clarification',
            'retry_count': 1,
            'dependencies': [],
            'workspace_files': [],
            'kb_state': {}
        }

        result = await recovery.attempt_recovery(context)

        assert result is False


class TestFundamentalFailureHandling:
    """Tests for fundamental failure handling."""

    @pytest.fixture
    def sample_plan(self):
        """Create plan with dependents."""
        return {
            'plan_id': 'test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Failed task',
                    'specialist': 'backend-architect',
                    'status': 'failed',
                    'dependencies': []
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Dependent task 1',
                    'specialist': 'fastapi-specialist',
                    'status': 'pending',
                    'dependencies': ['task-1']
                },
                'task-3': {
                    'id': 'task-3',
                    'title': 'Dependent task 2',
                    'specialist': 'docker-specialist',
                    'status': 'pending',
                    'dependencies': ['task-1']
                },
                'task-4': {
                    'id': 'task-4',
                    'title': 'Independent task',
                    'specialist': 'ui-ux',
                    'status': 'pending',
                    'dependencies': []
                }
            }
        }

    @pytest.mark.asyncio
    async def test_fundamental_failure_blocks_dependents(self, sample_plan):
        """Test that fundamental failure blocks all dependent tasks."""
        recovery = ErrorRecovery(sample_plan, 'task-1')

        context = {
            'task_id': 'task-1',
            'specialist': 'backend-architect',
            'error_message': 'Impossible architecture',
            'retry_count': 0,
            'dependencies': [],
            'workspace_files': [],
            'kb_state': {}
        }

        result = await recovery.handle_fundamental_failure(context)

        # Recovery should fail
        assert result is False

        # Failed task should be blocked
        assert sample_plan['tasks']['task-1']['status'] == 'blocked'

        # Dependent tasks should be blocked
        assert sample_plan['tasks']['task-2']['status'] == 'blocked'
        assert sample_plan['tasks']['task-3']['status'] == 'blocked'

        # Independent task should remain pending
        assert sample_plan['tasks']['task-4']['status'] == 'pending'

    @pytest.mark.asyncio
    async def test_failure_report_generation(self, sample_plan):
        """Test that failure report is generated correctly."""
        recovery = ErrorRecovery(sample_plan, 'task-1')

        context = {
            'task_id': 'task-1',
            'specialist': 'backend-architect',
            'error_message': 'Architectural conflict',
            'retry_count': 2,
            'dependencies': [],
            'workspace_files': [],
            'kb_state': {}
        }

        report = recovery.generate_failure_report(context)

        # Verify report contains key information
        assert 'Failed task' in report or 'task-1' in report
        assert 'backend-architect' in report
        assert 'Architectural conflict' in report
        assert 'Dependent task 1' in report or 'task-2' in report
        assert 'Options' in report or 'Recommendation' in report


class TestErrorRecoveryIntegration:
    """Integration tests for full error recovery flow."""

    @pytest.fixture
    def full_plan(self):
        """Create a complete plan for integration testing."""
        return {
            'plan_id': 'integration-test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Architecture design',
                    'specialist': 'backend-architect',
                    'status': 'completed',
                    'dependencies': []
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'API implementation',
                    'specialist': 'fastapi-specialist',
                    'status': 'failed',
                    'dependencies': ['task-1'],
                    'retry_count': 0
                },
                'task-3': {
                    'id': 'task-3',
                    'title': 'Deployment config',
                    'specialist': 'docker-specialist',
                    'status': 'pending',
                    'dependencies': ['task-2']
                }
            }
        }

    @pytest.mark.asyncio
    async def test_handle_task_failure_function(self, full_plan):
        """Test the handle_task_failure convenience function."""
        error = Exception("Need clarification on API design")

        # Mock the ErrorRecovery class
        with patch('utils.error_recovery.ErrorRecovery') as MockRecovery:
            mock_instance = MockRecovery.return_value
            mock_instance.handle_failure = AsyncMock(return_value=True)

            result = await handle_task_failure(full_plan, 'task-2', error)

            # Verify ErrorRecovery was created and used
            MockRecovery.assert_called_once_with(full_plan, 'task-2')
            mock_instance.handle_failure.assert_called_once_with(error)

            # Verify result
            assert result is True

    @pytest.mark.asyncio
    async def test_full_recovery_flow_fixable(self, full_plan):
        """Test complete recovery flow for fixable error."""
        recovery = ErrorRecovery(full_plan, 'task-2')

        # Mock methods
        recovery.get_clarification = AsyncMock(return_value="Clarification")
        recovery.update_workspace_with_clarification = MagicMock()

        error = Exception("Unclear API requirements")
        result = await recovery.handle_failure(error)

        # Should recover successfully
        assert result is True
        assert full_plan['tasks']['task-2'].get('retry_count', 0) > 0

    @pytest.mark.asyncio
    async def test_full_recovery_flow_fundamental(self, full_plan):
        """Test complete recovery flow for fundamental error."""
        recovery = ErrorRecovery(full_plan, 'task-2')

        error = Exception("Impossible to implement this architecture")
        result = await recovery.handle_failure(error)

        # Should not recover
        assert result is False
        assert full_plan['tasks']['task-2']['status'] == 'blocked'
        assert full_plan['tasks']['task-3']['status'] == 'blocked'

    @pytest.mark.asyncio
    async def test_max_retry_transitions_to_fundamental(self, full_plan):
        """Test that exceeding max retries transitions to fundamental failure."""
        # Set retry count to max
        full_plan['tasks']['task-2']['retry_count'] = 3

        recovery = ErrorRecovery(full_plan, 'task-2')

        error = Exception("Generic error")
        result = await recovery.handle_failure(error)

        # Should be treated as fundamental after max retries
        assert result is False


class TestHelperMethods:
    """Tests for helper methods."""

    @pytest.fixture
    def sample_plan(self):
        """Create sample plan."""
        return {
            'plan_id': 'test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Test',
                    'specialist': 'backend-architect',
                    'status': 'failed',
                    'dependencies': []
                }
            }
        }

    def test_extract_clarification_question(self, sample_plan):
        """Test extracting clarification question from error."""
        recovery = ErrorRecovery(sample_plan, 'task-1')

        context = {
            'error_message': 'Missing parameter X'
        }

        question = recovery.extract_clarification_question(context)

        assert 'Missing parameter X' in question
        assert 'Clarification' in question or 'clarification' in question

    def test_block_task_and_dependents(self, sample_plan):
        """Test blocking task and all dependents."""
        # Add dependent tasks
        sample_plan['tasks']['task-2'] = {
            'id': 'task-2',
            'title': 'Dependent',
            'specialist': 'fastapi-specialist',
            'status': 'pending',
            'dependencies': ['task-1']
        }
        sample_plan['tasks']['task-3'] = {
            'id': 'task-3',
            'title': 'Independent',
            'specialist': 'ui-ux',
            'status': 'pending',
            'dependencies': []
        }

        recovery = ErrorRecovery(sample_plan, 'task-1')
        recovery.block_task_and_dependents()

        # Failed task should be blocked
        assert sample_plan['tasks']['task-1']['status'] == 'blocked'

        # Dependent should be blocked
        assert sample_plan['tasks']['task-2']['status'] == 'blocked'

        # Independent should remain pending
        assert sample_plan['tasks']['task-3']['status'] == 'pending'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
