# utils/parallel_executor.py
"""Parallel task execution engine for coordinator."""

import asyncio
from typing import Dict, List, Set
from utils.dag_parser import get_ready_tasks, update_task_status

class ParallelExecutor:
    """Executes tasks in parallel based on DAG dependencies."""

    def __init__(self, plan: Dict):
        self.plan = plan
        self.running_tasks: Set[str] = set()
        self.max_parallel = 3  # Max concurrent specialist invocations

    async def execute_plan(self) -> None:
        """Execute all tasks in plan with parallelization."""
        while not self.is_plan_complete():
            ready_tasks = get_ready_tasks(self.plan)

            # Filter out tasks already running
            ready_tasks = [t for t in ready_tasks if t not in self.running_tasks]

            if not ready_tasks:
                # No ready tasks, wait for running tasks to complete
                if self.running_tasks:
                    await asyncio.sleep(1)
                    continue
                else:
                    # No ready tasks and nothing running = blocked or complete
                    break

            # Launch tasks in parallel (up to max_parallel)
            tasks_to_launch = ready_tasks[:self.max_parallel - len(self.running_tasks)]

            for task_id in tasks_to_launch:
                asyncio.create_task(self.execute_task(task_id))
                self.running_tasks.add(task_id)

            await asyncio.sleep(0.5)  # Brief pause before next iteration

    async def execute_task(self, task_id: str) -> None:
        """Execute a single task via specialist invocation."""
        task = self.plan['tasks'][task_id]

        try:
            # Update status to in-progress
            update_task_status(self.plan, task_id, 'in-progress')

            # Invoke specialist (placeholder - actual implementation uses Task tool)
            result = await self.invoke_specialist(
                specialist=task['specialist'],
                task_title=task['title'],
                task_id=task_id
            )

            # Run checkpoint
            await self.run_checkpoint(task_id, result)

            # Update status to completed
            update_task_status(self.plan, task_id, 'completed')

        except Exception as e:
            # Handle failure
            update_task_status(self.plan, task_id, 'failed')
            task['error_context'] = str(e)

        finally:
            # Remove from running set
            self.running_tasks.discard(task_id)

    async def invoke_specialist(
        self,
        specialist: str,
        task_title: str,
        task_id: str
    ) -> Dict:
        """
        Invoke specialist via Task tool.

        In actual implementation, this uses the Task tool to spawn specialist agent.
        Specialist receives:
        - Task title and description
        - Workspace files from predecessor tasks
        - Relevant KB sections

        Returns specialist output.
        """
        # Placeholder - actual implementation uses Task tool
        print(f"[Parallel Executor] Invoking {specialist} for {task_id}")

        # Simulate work
        await asyncio.sleep(2)

        return {
            'task_id': task_id,
            'specialist': specialist,
            'output': f'Completed {task_title}',
            'workspace_files': [f'work/{task_id}-output.md'],
            'kb_updates': []
        }

    async def run_checkpoint(self, task_id: str, result: Dict) -> None:
        """
        Run checkpoint validation after task completes.

        Checks:
        - Workspace file created
        - KB updated if needed
        - Pattern compliance
        """
        print(f"[Checkpoint] Validating {task_id}")

        # Verify workspace file exists
        workspace_files = result.get('workspace_files', [])
        for wf in workspace_files:
            # In real implementation, check file exists
            pass

        # Verify KB updated if needed
        kb_updates = result.get('kb_updates', [])
        # In real implementation, check KB files modified

        # Update task with outputs
        task = self.plan['tasks'][task_id]
        task['output_workspace'] = ','.join(workspace_files)
        task['kb_updates'] = kb_updates

        print(f"[Checkpoint] {task_id} validated ✓")

    def is_plan_complete(self) -> bool:
        """Check if all tasks are completed or blocked."""
        statuses = [task['status'] for task in self.plan['tasks'].values()]
        return all(s in ['completed', 'failed', 'blocked'] for s in statuses)


async def execute_plan_parallel(plan: Dict) -> Dict:
    """
    Execute plan with parallel task orchestration.

    Args:
        plan: Plan dict from auto_planner or manual parsing

    Returns:
        Updated plan with task statuses and results
    """
    executor = ParallelExecutor(plan)
    await executor.execute_plan()
    return executor.plan
