# utils/dag_parser.py
"""Simple DAG parser for MVP coordinator."""

from datetime import datetime
from typing import Dict, List

def parse_task_list(task_lines: List[str]) -> Dict:
    """
    Parse simple task list into plan JSON.

    Format:
    1. specialist-name: Task description
    2. specialist-name: Task description (depends on: 1)

    Returns plan dict matching task-dag.schema.json
    """
    plan_id = f"plan-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    tasks = {}

    for i, line in enumerate(task_lines, start=1):
        task_id = f"task-{i}"

        # Parse "specialist: description (depends on: X)"
        if ':' in line:
            specialist, rest = line.split(':', 1)
            specialist = specialist.strip().replace(' ', '-')

            # Extract dependencies
            deps = []
            if '(depends on:' in rest:
                desc, dep_str = rest.split('(depends on:')
                dep_str = dep_str.rstrip(')')
                deps = [f"task-{d.strip()}" for d in dep_str.split(',')]
            else:
                desc = rest

            tasks[task_id] = {
                "id": task_id,
                "title": desc.strip(),
                "specialist": specialist.lower(),
                "status": "pending",
                "dependencies": deps
            }

    return {
        "plan_id": plan_id,
        "created_at": datetime.now().isoformat(),
        "tasks": tasks
    }


def get_ready_tasks(plan: Dict) -> List[str]:
    """Return task IDs that are ready to execute (deps satisfied)."""
    ready = []
    for task_id, task in plan["tasks"].items():
        if task["status"] == "pending":
            deps_satisfied = all(
                plan["tasks"][dep_id]["status"] == "completed"
                for dep_id in task["dependencies"]
            )
            if deps_satisfied:
                ready.append(task_id)
    return ready


def update_task_status(plan: Dict, task_id: str, status: str) -> None:
    """Update task status in plan."""
    plan["tasks"][task_id]["status"] = status
    if status == "in-progress":
        plan["tasks"][task_id]["started_at"] = datetime.now().isoformat()
    elif status in ["completed", "failed"]:
        plan["tasks"][task_id]["completed_at"] = datetime.now().isoformat()
