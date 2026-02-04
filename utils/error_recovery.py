# utils/error_recovery.py
"""Adaptive error recovery for specialist task failures."""

from typing import Dict, Optional
from enum import Enum

class FailureType(Enum):
    FIXABLE = "fixable"
    FUNDAMENTAL = "fundamental"

class ErrorRecovery:
    """Handles specialist task failures with adaptive recovery."""

    def __init__(self, plan: Dict, task_id: str):
        self.plan = plan
        self.task = plan['tasks'][task_id]
        self.task_id = task_id
        self.max_retries = 3

    async def handle_failure(self, error: Exception) -> bool:
        """
        Handle task failure with adaptive recovery.

        Returns True if recovery successful and task can retry,
        False if fundamental failure requiring user escalation.
        """
        print(f"\n=== Error Recovery: {self.task_id} ===")
        print(f"Error: {error}")

        # Step 1: Capture context
        context = self.capture_failure_context(error)

        # Step 2: Classify failure type
        failure_type = self.classify_failure(error, context)

        if failure_type == FailureType.FIXABLE:
            return await self.handle_fixable_failure(context)
        else:
            return await self.handle_fundamental_failure(context)

    def capture_failure_context(self, error: Exception) -> Dict:
        """Capture full context of failure."""
        return {
            'task_id': self.task_id,
            'specialist': self.task['specialist'],
            'error_message': str(error),
            'retry_count': self.task.get('retry_count', 0),
            'dependencies': self.task.get('dependencies', []),
            'workspace_files': self.get_workspace_files(),
            'kb_state': self.get_kb_state()
        }

    def classify_failure(self, error: Exception, context: Dict) -> FailureType:
        """
        Classify failure as fixable or fundamental.

        Fixable:
        - Missing information from upstream task
        - Unclear requirements
        - Dependency conflict (can be resolved)

        Fundamental:
        - Plan assumption incorrect
        - Architectural conflict
        - Impossible requirement
        """
        error_msg = str(error).lower()

        # Fixable indicators
        fixable_keywords = [
            'unclear', 'missing', 'not found', 'undefined',
            'need more', 'clarification', 'incomplete'
        ]

        # Fundamental indicators
        fundamental_keywords = [
            'impossible', 'conflict', 'incompatible',
            'architecture', 'cannot', 'violation'
        ]

        if any(kw in error_msg for kw in fundamental_keywords):
            return FailureType.FUNDAMENTAL

        if any(kw in error_msg for kw in fixable_keywords):
            return FailureType.FIXABLE

        # Default to fixable if under retry limit
        if context['retry_count'] < self.max_retries:
            return FailureType.FIXABLE
        else:
            return FailureType.FUNDAMENTAL

    async def handle_fixable_failure(self, context: Dict) -> bool:
        """
        Handle fixable failure with loop-back or consultation.

        Strategies:
        1. Loop back to prerequisite specialist for clarification
        2. Consult other specialists for solution
        3. Retry with additional context
        """
        print("  Classified as FIXABLE failure")

        retry_count = context['retry_count']

        if retry_count < self.max_retries:
            # Attempt recovery
            recovery_successful = await self.attempt_recovery(context)

            if recovery_successful:
                print("  [OK] Recovery successful, will retry task")
                self.task['retry_count'] = retry_count + 1
                return True
            else:
                print("  [FAILED] Recovery failed, escalating")
                return False
        else:
            print(f"  [FAILED] Max retries ({self.max_retries}) exceeded, escalating")
            return False

    async def attempt_recovery(self, context: Dict) -> bool:
        """
        Attempt to recover from fixable failure.

        Steps:
        1. Identify prerequisite task that needs clarification
        2. Loop back to prerequisite specialist
        3. Get clarification
        4. Update workspace with clarification
        """
        dependencies = context['dependencies']

        if not dependencies:
            print("    No dependencies to loop back to")
            return False

        # Loop back to last dependency (most recent prerequisite)
        prerequisite_task_id = dependencies[-1]
        prerequisite_task = self.plan['tasks'][prerequisite_task_id]
        prerequisite_specialist = prerequisite_task['specialist']

        print(f"    Looping back to {prerequisite_specialist} ({prerequisite_task_id})")

        # Extract question from failure context
        question = self.extract_clarification_question(context)

        print(f"    Question: {question}")

        # Invoke prerequisite specialist for clarification
        clarification = await self.get_clarification(
            prerequisite_specialist,
            question,
            context
        )

        # Update workspace with clarification
        self.update_workspace_with_clarification(
            prerequisite_task_id,
            clarification
        )

        return True

    def extract_clarification_question(self, context: Dict) -> str:
        """Extract specific question from failure context."""
        error_msg = context['error_message']
        # In real implementation, parse error to extract question
        return f"Clarification needed: {error_msg}"

    async def get_clarification(
        self,
        specialist: str,
        question: str,
        context: Dict
    ) -> str:
        """
        Get clarification from prerequisite specialist.

        Invokes specialist with question and context.
        """
        # Placeholder - actual implementation invokes specialist via Task tool
        print(f"    Getting clarification from {specialist}...")
        return f"Clarification: [Response from {specialist}]"

    def update_workspace_with_clarification(
        self,
        prerequisite_task_id: str,
        clarification: str
    ) -> None:
        """Update workspace file with clarification."""
        prerequisite_task = self.plan['tasks'][prerequisite_task_id]
        workspace_file = prerequisite_task.get('output_workspace')

        if workspace_file:
            # Append clarification to workspace file
            print(f"    Updated {workspace_file} with clarification")

    async def handle_fundamental_failure(self, context: Dict) -> bool:
        """
        Handle fundamental failure with user escalation.

        Actions:
        1. Block failed task and all dependents
        2. Continue independent parallel tasks
        3. Present failure report to user with options
        """
        print("  Classified as FUNDAMENTAL failure")

        # Block this task and dependents
        self.block_task_and_dependents()

        # Generate failure report
        report = self.generate_failure_report(context)

        print("\n" + "="*60)
        print("FUNDAMENTAL FAILURE - USER ESCALATION REQUIRED")
        print("="*60)
        print(report)
        print("="*60)

        # In real implementation, present to user and get decision
        # For now, return False (not recovered)
        return False

    def block_task_and_dependents(self) -> None:
        """Block failed task and all downstream dependents."""
        self.task['status'] = 'blocked'

        # Block all tasks that depend on this one
        for task_id, task in self.plan['tasks'].items():
            if self.task_id in task.get('dependencies', []):
                task['status'] = 'blocked'
                print(f"    Blocked dependent task: {task_id}")

    def generate_failure_report(self, context: Dict) -> str:
        """Generate detailed failure report for user."""
        # Find dependent tasks
        dependent_tasks = []
        for task_id, task in self.plan['tasks'].items():
            if self.task_id in task.get('dependencies', []):
                dependent_tasks.append(task_id)

        report = f"""
Task Failed: {self.task['title']}
Specialist: {self.task['specialist']}
Reason: {context['error_message']}

Context:
- Retry attempts: {context['retry_count']}/{self.max_retries}
- Dependencies: {', '.join(context['dependencies']) or 'None'}

Impact:
- This task is blocked
- Dependent tasks are blocked: {', '.join(dependent_tasks) if dependent_tasks else 'None'}

Options:
1. Amend plan to adjust scope
2. Provide additional information/requirements
3. Abandon this feature
4. Continue with independent tasks

Recommendation: [Coordinator's recommendation based on failure type]
"""
        return report

    def get_workspace_files(self) -> list:
        """Get workspace files for this task."""
        # Placeholder
        return []

    def get_kb_state(self) -> dict:
        """Get current KB state."""
        # Placeholder
        return {}


async def handle_task_failure(plan: Dict, task_id: str, error: Exception) -> bool:
    """
    Handle task failure with adaptive recovery.

    Args:
        plan: Current plan state
        task_id: Failed task ID
        error: Exception that caused failure

    Returns:
        True if recovery successful (can retry), False if escalation needed
    """
    recovery = ErrorRecovery(plan, task_id)
    return await recovery.handle_failure(error)
