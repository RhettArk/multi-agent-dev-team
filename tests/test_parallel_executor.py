# tests/test_parallel_executor.py
"""Tests for parallel execution engine."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from utils.parallel_executor import ParallelExecutor, execute_plan_parallel
from utils.dag_parser import parse_task_list


class TestParallelExecutor:
    """Tests for ParallelExecutor class."""

    @pytest.fixture
    def simple_plan(self):
        """Create a simple test plan."""
        return {
            'plan_id': 'test-plan',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'First task',
                    'specialist': 'backend-architect',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Second task',
                    'specialist': 'fastapi-specialist',
                    'status': 'pending',
                    'dependencies': ['task-1']
                },
                'task-3': {
                    'id': 'task-3',
                    'title': 'Third task',
                    'specialist': 'docker-specialist',
                    'status': 'pending',
                    'dependencies': ['task-2']
                }
            }
        }

    @pytest.fixture
    def parallel_ready_plan(self):
        """Create a plan with multiple tasks ready to run in parallel."""
        return {
            'plan_id': 'parallel-test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Independent task 1',
                    'specialist': 'backend-architect',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Independent task 2',
                    'specialist': 'ui-ux',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-3': {
                    'id': 'task-3',
                    'title': 'Independent task 3',
                    'specialist': 'docker-specialist',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-4': {
                    'id': 'task-4',
                    'title': 'Dependent task',
                    'specialist': 'code-reviewer',
                    'status': 'pending',
                    'dependencies': ['task-1', 'task-2', 'task-3']
                }
            }
        }

    def test_executor_initialization(self, simple_plan):
        """Test that executor initializes correctly."""
        executor = ParallelExecutor(simple_plan)

        assert executor.plan == simple_plan
        assert len(executor.running_tasks) == 0
        assert executor.max_parallel == 3

    def test_max_parallel_limit(self, simple_plan):
        """Test that max_parallel is set to 3."""
        executor = ParallelExecutor(simple_plan)

        assert executor.max_parallel == 3

    @pytest.mark.asyncio
    async def test_execute_single_task(self, simple_plan):
        """Test executing a single task."""
        executor = ParallelExecutor(simple_plan)

        # Mock the specialist invocation
        executor.invoke_specialist = AsyncMock(return_value={
            'task_id': 'task-1',
            'specialist': 'backend-architect',
            'output': 'Task completed',
            'workspace_files': ['work/task-1-output.md'],
            'kb_updates': []
        })
        executor.run_checkpoint = AsyncMock()

        # Execute the task
        await executor.execute_task('task-1')

        # Verify task was executed
        assert simple_plan['tasks']['task-1']['status'] == 'completed'
        assert executor.invoke_specialist.called
        assert executor.run_checkpoint.called

    @pytest.mark.asyncio
    async def test_execute_task_failure(self, simple_plan):
        """Test that task failure is handled correctly."""
        executor = ParallelExecutor(simple_plan)

        # Mock specialist to raise exception
        executor.invoke_specialist = AsyncMock(side_effect=Exception("Test error"))
        executor.run_checkpoint = AsyncMock()

        # Execute the task (should handle exception)
        await executor.execute_task('task-1')

        # Verify task status is failed
        assert simple_plan['tasks']['task-1']['status'] == 'failed'
        assert 'error_context' in simple_plan['tasks']['task-1']

    @pytest.mark.asyncio
    async def test_task_status_transitions(self, simple_plan):
        """Test that task goes through correct status transitions."""
        executor = ParallelExecutor(simple_plan)

        # Track status changes
        statuses = []

        # Mock invoke_specialist to capture status
        async def mock_invoke(*args, **kwargs):
            statuses.append(simple_plan['tasks']['task-1']['status'])
            await asyncio.sleep(0.1)
            return {
                'task_id': 'task-1',
                'specialist': 'backend-architect',
                'output': 'Done',
                'workspace_files': [],
                'kb_updates': []
            }

        executor.invoke_specialist = mock_invoke
        executor.run_checkpoint = AsyncMock()

        # Execute task
        await executor.execute_task('task-1')

        # Verify status progression: pending → in-progress → completed
        assert 'in-progress' in statuses
        assert simple_plan['tasks']['task-1']['status'] == 'completed'

    @pytest.mark.asyncio
    async def test_parallel_execution_limit(self, parallel_ready_plan):
        """Test that max 3 tasks run in parallel."""
        executor = ParallelExecutor(parallel_ready_plan)

        # Track how many tasks run simultaneously
        max_concurrent = 0
        current_concurrent = 0
        lock = asyncio.Lock()

        async def mock_invoke(*args, **kwargs):
            nonlocal current_concurrent, max_concurrent
            async with lock:
                current_concurrent += 1
                max_concurrent = max(max_concurrent, current_concurrent)

            await asyncio.sleep(0.2)  # Simulate work

            async with lock:
                current_concurrent -= 1

            return {
                'task_id': args[2],
                'specialist': args[0],
                'output': 'Done',
                'workspace_files': [],
                'kb_updates': []
            }

        executor.invoke_specialist = mock_invoke
        executor.run_checkpoint = AsyncMock()

        # Execute plan
        await executor.execute_plan()

        # Verify no more than 3 tasks ran concurrently
        assert max_concurrent <= 3

    @pytest.mark.asyncio
    async def test_dependency_resolution(self, simple_plan):
        """Test that tasks respect dependency order."""
        executor = ParallelExecutor(simple_plan)

        # Track execution order
        execution_order = []

        async def mock_invoke(specialist, task_title, task_id):
            execution_order.append(task_id)
            await asyncio.sleep(0.1)
            return {
                'task_id': task_id,
                'specialist': specialist,
                'output': 'Done',
                'workspace_files': [],
                'kb_updates': []
            }

        executor.invoke_specialist = mock_invoke
        executor.run_checkpoint = AsyncMock()

        # Execute plan
        await executor.execute_plan()

        # Verify execution order respects dependencies
        # task-1 must complete before task-2
        task1_idx = execution_order.index('task-1')
        task2_idx = execution_order.index('task-2')
        task3_idx = execution_order.index('task-3')

        assert task1_idx < task2_idx
        assert task2_idx < task3_idx

    @pytest.mark.asyncio
    async def test_is_plan_complete(self, simple_plan):
        """Test plan completion detection."""
        executor = ParallelExecutor(simple_plan)

        # Initially not complete
        assert not executor.is_plan_complete()

        # Mark all tasks completed
        for task in simple_plan['tasks'].values():
            task['status'] = 'completed'

        assert executor.is_plan_complete()

    @pytest.mark.asyncio
    async def test_is_plan_complete_with_failures(self, simple_plan):
        """Test that plan is considered complete with failed tasks."""
        executor = ParallelExecutor(simple_plan)

        # Mark tasks as various end states
        simple_plan['tasks']['task-1']['status'] = 'completed'
        simple_plan['tasks']['task-2']['status'] = 'failed'
        simple_plan['tasks']['task-3']['status'] = 'blocked'

        assert executor.is_plan_complete()

    @pytest.mark.asyncio
    async def test_checkpoint_validation(self, simple_plan):
        """Test that checkpoint validation is called after task completion."""
        executor = ParallelExecutor(simple_plan)

        checkpoint_called = False

        async def mock_checkpoint(task_id, result):
            nonlocal checkpoint_called
            checkpoint_called = True
            # Verify result structure
            assert 'task_id' in result
            assert 'workspace_files' in result
            assert 'kb_updates' in result

        executor.invoke_specialist = AsyncMock(return_value={
            'task_id': 'task-1',
            'specialist': 'backend-architect',
            'output': 'Done',
            'workspace_files': ['file1.md'],
            'kb_updates': []
        })
        executor.run_checkpoint = mock_checkpoint

        await executor.execute_task('task-1')

        assert checkpoint_called

    @pytest.mark.asyncio
    async def test_running_tasks_cleanup(self, simple_plan):
        """Test that running_tasks set is properly cleaned up."""
        executor = ParallelExecutor(simple_plan)

        executor.invoke_specialist = AsyncMock(return_value={
            'task_id': 'task-1',
            'specialist': 'backend-architect',
            'output': 'Done',
            'workspace_files': [],
            'kb_updates': []
        })
        executor.run_checkpoint = AsyncMock()

        # Running tasks should be empty initially
        assert len(executor.running_tasks) == 0

        # Execute task
        await executor.execute_task('task-1')

        # Running tasks should be cleaned up after execution
        assert len(executor.running_tasks) == 0


class TestExecutePlanParallel:
    """Tests for execute_plan_parallel function."""

    @pytest.mark.asyncio
    async def test_execute_plan_parallel_returns_updated_plan(self):
        """Test that execute_plan_parallel returns updated plan."""
        plan = {
            'plan_id': 'test',
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

        # Mock the executor
        with patch('utils.parallel_executor.ParallelExecutor') as MockExecutor:
            mock_instance = MockExecutor.return_value
            mock_instance.plan = plan
            mock_instance.execute_plan = AsyncMock()

            result = await execute_plan_parallel(plan)

            # Verify executor was created and executed
            MockExecutor.assert_called_once_with(plan)
            mock_instance.execute_plan.assert_called_once()

            # Verify plan was returned
            assert result == plan


class TestDAGExecution:
    """Integration tests for DAG-based execution."""

    @pytest.mark.asyncio
    async def test_dag_parallel_branches(self):
        """Test executing DAG with parallel branches."""
        plan = {
            'plan_id': 'dag-test',
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'title': 'Root task',
                    'specialist': 'code-reviewer',
                    'status': 'pending',
                    'dependencies': []
                },
                'task-2': {
                    'id': 'task-2',
                    'title': 'Branch A',
                    'specialist': 'backend-architect',
                    'status': 'pending',
                    'dependencies': ['task-1']
                },
                'task-3': {
                    'id': 'task-3',
                    'title': 'Branch B',
                    'specialist': 'ui-ux',
                    'status': 'pending',
                    'dependencies': ['task-1']
                },
                'task-4': {
                    'id': 'task-4',
                    'title': 'Merge task',
                    'specialist': 'code-reviewer',
                    'status': 'pending',
                    'dependencies': ['task-2', 'task-3']
                }
            }
        }

        executor = ParallelExecutor(plan)

        # Track which tasks ran in parallel
        running = []
        lock = asyncio.Lock()

        async def mock_invoke(specialist, task_title, task_id):
            async with lock:
                running.append(task_id)
            await asyncio.sleep(0.1)
            async with lock:
                running.remove(task_id)
            return {
                'task_id': task_id,
                'specialist': specialist,
                'output': 'Done',
                'workspace_files': [],
                'kb_updates': []
            }

        executor.invoke_specialist = mock_invoke
        executor.run_checkpoint = AsyncMock()

        await executor.execute_plan()

        # Verify all tasks completed
        assert all(
            task['status'] == 'completed'
            for task in plan['tasks'].values()
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
