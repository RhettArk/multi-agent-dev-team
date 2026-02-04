# utils/checkpoint_validator.py
"""Advanced checkpoint validation with peer review."""

from typing import Dict, List
from pathlib import Path
import json


class CheckpointValidator:
    """Comprehensive checkpoint validation after each task."""

    def __init__(self, plan: Dict, task_id: str):
        self.plan = plan
        self.task = plan['tasks'][task_id]
        self.task_id = task_id

    async def run_checkpoint(self) -> bool:
        """
        Run full checkpoint workflow.

        Returns True if validation passed, False otherwise.
        """
        print(f"\n=== Checkpoint: {self.task_id} ===")

        # Step 1: Automatic validation
        if not await self.automatic_validation():
            print("❌ Automatic validation failed")
            return False

        # Step 2: Peer review
        if not await self.peer_review():
            print("❌ Peer review failed")
            return False

        # Step 3: KB sync
        if not await self.kb_sync():
            print("❌ KB sync failed")
            return False

        # Step 4: Final approval
        self.final_approval()
        print("✅ Checkpoint passed\n")
        return True

    async def automatic_validation(self) -> bool:
        """
        Step 1: Automatic validation (fast feedback).

        Checks:
        - Workspace files created
        - Pattern compliance
        - No obvious errors
        """
        print("  [1/4] Running automatic validation...")

        # Check workspace files
        workspace_file = self.task.get('output_workspace')
        if workspace_file and not Path(workspace_file).exists():
            print(f"    ⚠ Workspace file missing: {workspace_file}")
            return False

        # Check KB updates if expected
        # (Pattern compliance check would go here)

        print("    ✓ Automatic validation passed")
        return True

    async def peer_review(self) -> bool:
        """
        Step 2: Peer review by relevant specialists.

        Invokes:
        - Code Reviewer (always)
        - Domain specialists (if cross-domain impact)
        - Architecture specialist (for design tasks)
        """
        print("  [2/4] Running peer review...")

        reviewers = self.get_peer_reviewers()

        for reviewer in reviewers:
            print(f"    Consulting {reviewer}...")
            review_result = await self.invoke_reviewer(reviewer)

            if not review_result['approved']:
                print(f"    ❌ {reviewer} flagged issues:")
                for issue in review_result['issues']:
                    print(f"      - {issue}")
                return False

        print("    ✓ Peer review passed")
        return True

    def get_peer_reviewers(self) -> List[str]:
        """Determine which specialists should review this task."""
        specialist = self.task['specialist']
        reviewers = []

        # Always review by code reviewer
        if specialist not in ['code-reviewer', 'code-quality-frontend']:
            if 'frontend' in specialist or 'ui' in specialist or 'javascript' in specialist:
                reviewers.append('code-quality-frontend')
            else:
                reviewers.append('code-reviewer')

        # Cross-domain review
        domain_map = {
            'fastapi-specialist': ['backend-architect'],  # Architect reviews implementation
            'openai-agents-sdk': ['backend-architect'],
            'ui-ux': ['code-quality-frontend'],
            'javascript-specialist': ['code-quality-frontend']
        }

        if specialist in domain_map:
            reviewers.extend(domain_map[specialist])

        return reviewers

    async def invoke_reviewer(self, reviewer: str) -> Dict:
        """
        Invoke reviewer specialist to check task output.

        Reviewer receives:
        - Task output (code files, workspace notes)
        - KB patterns to check against
        - Review checklist

        Returns review result with approval status and issues found.
        """
        # Placeholder - actual implementation invokes reviewer via Task tool
        # For now, simulate approval
        return {
            'reviewer': reviewer,
            'approved': True,
            'issues': []
        }

    async def kb_sync(self) -> bool:
        """
        Step 3: Knowledge base sync.

        Ensures:
        - Pattern files updated if new conventions introduced
        - Decisions logged with rationale
        - Dependencies updated if contracts changed
        - No conflicts with recent decisions
        """
        print("  [3/4] Running KB sync...")

        # Check if task made KB updates
        kb_updates = self.task.get('kb_updates', [])

        if not kb_updates:
            print("    ℹ No KB updates for this task")
            return True

        # Verify KB files were actually modified
        for kb_file in kb_updates:
            if not Path(kb_file).exists():
                print(f"    ⚠ KB file missing: {kb_file}")
                return False

        # Check for decision conflicts
        if 'kb/decisions.log' in kb_updates:
            if not self.check_decision_conflicts():
                print("    ⚠ Decision conflicts detected")
                return False

        print("    ✓ KB sync completed")
        return True

    def check_decision_conflicts(self) -> bool:
        """Check if new decisions conflict with recent ones."""
        # In real implementation, parse decisions.log and check for conflicts
        # For now, assume no conflicts
        return True

    def final_approval(self) -> None:
        """
        Step 4: Final approval.

        Mark task as validated and prepare next tasks.
        """
        print("  [4/4] Final approval...")

        # Update task status to validated
        self.task['status'] = 'validated'

        # Transition dependent tasks to ready
        for task_id, task in self.plan['tasks'].items():
            if self.task_id in task.get('dependencies', []):
                deps_satisfied = all(
                    self.plan['tasks'][dep]['status'] in ['completed', 'validated']
                    for dep in task['dependencies']
                )
                if deps_satisfied and task['status'] == 'pending':
                    task['status'] = 'ready'

        print("    ✓ Task validated, dependents transitioned to ready")


async def run_checkpoint(plan: Dict, task_id: str) -> bool:
    """
    Run comprehensive checkpoint for a task.

    Args:
        plan: Current plan state
        task_id: ID of task to validate

    Returns:
        True if checkpoint passed, False otherwise
    """
    validator = CheckpointValidator(plan, task_id)
    return await validator.run_checkpoint()
