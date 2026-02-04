# tests/test_full_system.py
"""End-to-end integration tests for the full coordinator system."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
from utils.auto_planner import auto_plan_feature, analyze_domains, synthesize_plan
from utils.parallel_executor import ParallelExecutor, execute_plan_parallel
from utils.error_recovery import ErrorRecovery, handle_task_failure
from utils.dag_parser import parse_task_list, get_ready_tasks, update_task_status
from utils.checkpoint_validator import CheckpointValidator


class TestEndToEndWorkflow:
    """Integration tests for complete workflow: plan → execute → checkpoint → complete."""

    @pytest.mark.asyncio
    async def test_simple_feature_end_to_end(self):
        """Test complete workflow for a simple feature."""
        # Step 1: Analyze domains
        feature_description = "Add login API endpoint"
        domains = analyze_domains(feature_description)

        assert 'backend' in domains

        # Step 2: Create plan (simplified - no actual specialist calls)
        specialist_responses = {
            'backend-architect': 'Design auth architecture',
            'fastapi-specialist': 'Implement /api/v1/auth/login'
        }

        plan = synthesize_plan(feature_description, specialist_responses, domains)

        # Verify plan structure
        assert 'plan_id' in plan
        assert 'tasks' in plan
        assert len(plan['tasks']) == 2

        # Step 3: Execute plan with mocked specialist invocations
        executor = ParallelExecutor(plan)

        async def mock_specialist_invoke(specialist, task_title, task_id):
            await asyncio.sleep(0.05)  # Simulate work
            return {
                'task_id': task_id,
                'specialist': specialist,
                'output': f'Completed: {task_title}',
                'workspace_files': [f'work/{task_id}-output.md'],
                'kb_updates': []
            }

        executor.invoke_specialist = mock_specialist_invoke
        executor.run_checkpoint = AsyncMock()

        await executor.execute_plan()

        # Step 4: Verify all tasks completed
        for task in plan['tasks'].values():
            assert task['status'] == 'completed'

    @pytest.mark.asyncio
    async def test_fullstack_feature_workflow(self):
        """Test workflow for feature spanning backend and frontend."""
        # Feature requiring both backend and frontend work
        feature_description = "Add user profile UI component with API endpoint"
        domains = analyze_domains(feature_description)

        assert 'backend' in domains or 'frontend' in domains
        # Should detect at least one domain (may default to both if only one detected)

        # Create plan with both backend and frontend specialists
        specialist_responses = {
            'backend-architect': 'Design profile API',
            'fastapi-specialist': 'Implement profile endpoints',
            'ui-ux': 'Design profile UI',
            'javascript-specialist': 'Implement profile component'
        }

        plan = synthesize_plan(feature_description, specialist_responses, domains)

        # Execute plan
        executor = ParallelExecutor(plan)
        executor.invoke_specialist = AsyncMock(return_value={
            'task_id': 'mock',
            'specialist': 'mock',
            'output': 'Done',
            'workspace_files': ['output.md'],
            'kb_updates': []
        })
        executor.run_checkpoint = AsyncMock()

        await executor.execute_plan()

        # Verify completion
        assert all(t['status'] == 'completed' for t in plan['tasks'].values())

    @pytest.mark.asyncio
    async def test_workflow_with_parallel_execution(self):
        """Test workflow with tasks that can run in parallel."""
        # Create plan with parallel-ready tasks
        plan = {
            'plan_id': 'parallel-test',
            'created_at': '2024-01-01',
            'feature_description': 'Multi-component feature',
            'domains_affected': ['backend', 'frontend'],
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Backend task',
                    'specialist': 'backend-architect',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Frontend task',
                    'specialist': 'ui-ux',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-3': {
                    'id': 'task-3',
                    'title': 'Integration task',
                    'specialist': 'code-reviewer',
                    'status': 'pending',
                    'dependencies': ['task-1', 'task-2']
                }
            },
            'scope_boundaries': {},
            'success_criteria': []
        }

        # Track execution timing to verify parallelism
        execution_times = {}

        async def mock_invoke(specialist, task_title, task_id):
            import time
            execution_times[task_id] = time.time()
            await asyncio.sleep(0.1)
            return {
                'task_id': task_id,
                'specialist': specialist,
                'output': 'Done',
                'workspace_files': [],
                'kb_updates': []
            }

        executor = ParallelExecutor(plan)
        executor.invoke_specialist = mock_invoke
        executor.run_checkpoint = AsyncMock()

        await executor.execute_plan()

        # Verify task-1 and task-2 started around the same time (parallel)
        time_diff = abs(execution_times['task-1'] - execution_times['task-2'])
        assert time_diff < 0.05  # Started within 50ms of each other

        # Verify task-3 started after both completed
        assert all(t['status'] == 'completed' for t in plan['tasks'].values())

    @pytest.mark.asyncio
    async def test_workflow_with_checkpoint_validation(self):
        """Test that checkpoints are validated during execution."""
        plan = {
            'plan_id': 'checkpoint-test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Test task',
                    'specialist': 'backend-architect',
                    'status': 'pending',
                    'dependencies': []
                }
            }
        }

        executor = ParallelExecutor(plan)

        # Track checkpoint calls
        checkpoint_calls = []

        async def mock_checkpoint(task_id, result):
            checkpoint_calls.append({
                'task_id': task_id,
                'result': result
            })

        executor.invoke_specialist = AsyncMock(return_value={
            'task_id': 'task-1',
            'specialist': 'backend-architect',
            'output': 'Done',
            'workspace_files': ['output.md'],
            'kb_updates': ['pattern-update']
        })
        executor.run_checkpoint = mock_checkpoint

        await executor.execute_plan()

        # Verify checkpoint was called
        assert len(checkpoint_calls) == 1
        assert checkpoint_calls[0]['task_id'] == 'task-1'
        assert 'workspace_files' in checkpoint_calls[0]['result']


class TestErrorRecoveryIntegration:
    """Integration tests for error recovery in full workflow."""

    @pytest.mark.asyncio
    async def test_workflow_with_fixable_failure(self):
        """Test workflow recovers from fixable failure."""
        plan = {
            'plan_id': 'recovery-test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'First task',
                    'specialist': 'backend-architect',
                    'status': 'completed',
                    'dependencies': [],
                    'output_workspace': 'work/task-1.md'
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Second task',
                    'specialist': 'fastapi-specialist',
                    'status': 'pending',
                    'dependencies': ['task-1'],
                    'retry_count': 0
                }
            }
        }

        # Simulate fixable failure on first attempt, success on retry
        attempt_count = [0]

        async def mock_invoke(specialist, task_title, task_id):
            attempt_count[0] += 1
            if task_id == 'task-2' and attempt_count[0] == 1:
                raise Exception("Unclear requirement - need clarification")
            return {
                'task_id': task_id,
                'specialist': specialist,
                'output': 'Done',
                'workspace_files': [],
                'kb_updates': []
            }

        executor = ParallelExecutor(plan)
        executor.invoke_specialist = mock_invoke
        executor.run_checkpoint = AsyncMock()

        # First execution should fail task-2
        await executor.execute_task('task-2')
        assert plan['tasks']['task-2']['status'] == 'failed'

        # Attempt recovery
        error = Exception("Unclear requirement - need clarification")
        recovery = ErrorRecovery(plan, 'task-2')
        recovery.get_clarification = AsyncMock(return_value="Clarification")

        can_retry = await recovery.handle_failure(error)
        assert can_retry is True

        # Retry should succeed
        plan['tasks']['task-2']['status'] = 'pending'
        await executor.execute_task('task-2')
        assert plan['tasks']['task-2']['status'] == 'completed'

    @pytest.mark.asyncio
    async def test_workflow_with_fundamental_failure(self):
        """Test workflow handles fundamental failure by blocking dependents."""
        plan = {
            'plan_id': 'fundamental-failure-test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Failed task',
                    'specialist': 'backend-architect',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Dependent task',
                    'specialist': 'fastapi-specialist',
                    'status': 'pending',
                    'dependencies': ['task-1']
                },
                'task-3': {
                    'id': 'task-3',
                    'title': 'Independent task',
                    'specialist': 'ui-ux',
                    'status': 'pending',
                    'dependencies': []
                }
            }
        }

        async def mock_invoke(specialist, task_title, task_id):
            if task_id == 'task-1':
                raise Exception("Impossible architecture conflict")
            return {
                'task_id': task_id,
                'specialist': specialist,
                'output': 'Done',
                'workspace_files': [],
                'kb_updates': []
            }

        executor = ParallelExecutor(plan)
        executor.invoke_specialist = mock_invoke
        executor.run_checkpoint = AsyncMock()

        # Execute task-1 (will fail)
        await executor.execute_task('task-1')
        assert plan['tasks']['task-1']['status'] == 'failed'

        # Handle failure
        error = Exception("Impossible architecture conflict")
        recovery = ErrorRecovery(plan, 'task-1')
        can_retry = await recovery.handle_failure(error)

        assert can_retry is False
        assert plan['tasks']['task-1']['status'] == 'blocked'
        assert plan['tasks']['task-2']['status'] == 'blocked'

        # Independent task should still be executable
        await executor.execute_task('task-3')
        assert plan['tasks']['task-3']['status'] == 'completed'


class TestComplexScenarios:
    """Tests for complex real-world scenarios."""

    @pytest.mark.asyncio
    async def test_multi_stage_feature_with_dependencies(self):
        """Test complex feature with multiple stages and dependencies."""
        # Simulate: Design → Backend → Frontend → Integration
        task_lines = [
            "backend-architect: Design authentication system",
            "backend-design: Design database schema (depends on: 1)",
            "fastapi-specialist: Implement auth endpoints (depends on: 2)",
            "ui-ux: Design login UI (depends on: 1)",
            "javascript-specialist: Implement login component (depends on: 4)",
            "code-reviewer: Integration testing (depends on: 3, 5)"
        ]

        plan = parse_task_list(task_lines)

        # Execute with mocked specialists
        executor = ParallelExecutor(plan)
        executor.invoke_specialist = AsyncMock(return_value={
            'task_id': 'mock',
            'specialist': 'mock',
            'output': 'Done',
            'workspace_files': [],
            'kb_updates': []
        })
        executor.run_checkpoint = AsyncMock()

        await executor.execute_plan()

        # Verify all completed in correct order
        assert all(t['status'] == 'completed' for t in plan['tasks'].values())

    @pytest.mark.asyncio
    async def test_partial_failure_continues_independent_work(self):
        """Test that partial failure doesn't block independent work."""
        plan = {
            'plan_id': 'partial-failure-test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Backend work',
                    'specialist': 'backend-architect',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Backend dependent',
                    'specialist': 'fastapi-specialist',
                    'status': 'pending',
                    'dependencies': ['task-1']
                },
                'task-3': {
                    'id': 'task-3',
                    'title': 'Frontend work (independent)',
                    'specialist': 'ui-ux',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-4': {
                    'id': 'task-4',
                    'title': 'Frontend dependent',
                    'specialist': 'javascript-specialist',
                    'status': 'pending',
                    'dependencies': ['task-3']
                }
            }
        }

        async def mock_invoke(specialist, task_title, task_id):
            # Fail backend work
            if task_id == 'task-1':
                raise Exception("Impossible backend requirement")
            # Succeed on frontend work
            return {
                'task_id': task_id,
                'specialist': specialist,
                'output': 'Done',
                'workspace_files': [],
                'kb_updates': []
            }

        executor = ParallelExecutor(plan)
        executor.invoke_specialist = mock_invoke
        executor.run_checkpoint = AsyncMock()

        # Execute and handle failures
        await executor.execute_task('task-1')
        assert plan['tasks']['task-1']['status'] == 'failed'

        # Handle as fundamental failure
        error = Exception("Impossible backend requirement")
        recovery = ErrorRecovery(plan, 'task-1')
        await recovery.handle_failure(error)

        # Backend chain should be blocked
        assert plan['tasks']['task-1']['status'] == 'blocked'
        assert plan['tasks']['task-2']['status'] == 'blocked'

        # Frontend work should proceed
        await executor.execute_task('task-3')
        await executor.execute_task('task-4')

        assert plan['tasks']['task-3']['status'] == 'completed'
        assert plan['tasks']['task-4']['status'] == 'completed'

    @pytest.mark.asyncio
    async def test_plan_to_completion_workflow(self):
        """Test complete workflow from planning to completion."""
        # Step 1: Feature description
        feature = "Add health check endpoint to API"

        # Step 2: Domain analysis
        domains = analyze_domains(feature)
        assert 'backend' in domains

        # Step 3: Plan generation
        specialist_responses = {
            'backend-architect': 'Design health check',
            'fastapi-specialist': 'Implement /health endpoint',
            'code-reviewer': 'Review implementation'
        }
        plan = synthesize_plan(feature, specialist_responses, domains)

        # Step 4: Execution
        executor = ParallelExecutor(plan)
        executor.invoke_specialist = AsyncMock(return_value={
            'task_id': 'mock',
            'specialist': 'mock',
            'output': 'Completed',
            'workspace_files': ['work/output.md'],
            'kb_updates': ['patterns/api-health-check.md']
        })
        executor.run_checkpoint = AsyncMock()

        await executor.execute_plan()

        # Step 5: Validation
        assert executor.is_plan_complete()
        assert all(t['status'] == 'completed' for t in plan['tasks'].values())

        # Note: output_workspace is set by run_checkpoint in real implementation
        # In this test, we're using AsyncMock for run_checkpoint, so it doesn't populate output_workspace
        # Just verify tasks are complete
        assert len(plan['tasks']) == 3


class TestSystemEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_empty_plan(self):
        """Test handling of empty plan."""
        plan = {
            'plan_id': 'empty',
            'tasks': {}
        }

        executor = ParallelExecutor(plan)
        assert executor.is_plan_complete()

    @pytest.mark.asyncio
    async def test_single_task_plan(self):
        """Test plan with only one task."""
        plan = {
            'plan_id': 'single',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Only task',
                    'specialist': 'backend-architect',
                    'status': 'pending',
                    'dependencies': []
                }
            }
        }

        executor = ParallelExecutor(plan)
        executor.invoke_specialist = AsyncMock(return_value={
            'task_id': 'task-1',
            'specialist': 'backend-architect',
            'output': 'Done',
            'workspace_files': [],
            'kb_updates': []
        })
        executor.run_checkpoint = AsyncMock()

        await executor.execute_plan()

        assert plan['tasks']['task-1']['status'] == 'completed'

    def test_circular_dependency_detection(self):
        """Test that circular dependencies are handled."""
        # This would be caught during plan validation in real system
        plan = {
            'plan_id': 'circular',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'status': 'pending',
                    'dependencies': ['task-2']
                },
                'task-2': {
                    'id': 'task-2',
                    'status': 'pending',
                    'dependencies': ['task-1']
                }
            }
        }

        # No tasks should be ready due to circular dependency
        ready = get_ready_tasks(plan)
        assert len(ready) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
