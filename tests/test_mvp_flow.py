# tests/test_mvp_flow.py
"""Integration test for MVP coordinator flow."""

import json
import pytest
from pathlib import Path
from utils.dag_parser import parse_task_list, get_ready_tasks, update_task_status
from utils.kb_manager import initialize_kb, verify_kb_exists, log_decision

TEST_DIR = Path("test_codebase")

def test_dag_parser():
    """Test parsing task list into plan JSON."""
    task_lines = [
        "backend-architect: Design login endpoint",
        "fastapi-specialist: Implement /api/v1/auth/login (depends on: 1)",
        "code-reviewer: Review and simplify (depends on: 2)"
    ]

    plan = parse_task_list(task_lines)

    assert plan["plan_id"].startswith("plan-")
    assert len(plan["tasks"]) == 3
    assert plan["tasks"]["task-1"]["specialist"] == "backend-architect"
    assert plan["tasks"]["task-2"]["dependencies"] == ["task-1"]
    assert plan["tasks"]["task-3"]["dependencies"] == ["task-2"]


def test_ready_tasks():
    """Test identifying ready tasks in DAG."""
    plan = {
        "plan_id": "test",
        "tasks": {
            "task-1": {"status": "pending", "dependencies": []},
            "task-2": {"status": "pending", "dependencies": ["task-1"]},
            "task-3": {"status": "pending", "dependencies": ["task-1"]}
        }
    }

    # Initially only task-1 is ready
    ready = get_ready_tasks(plan)
    assert ready == ["task-1"]

    # Complete task-1, now task-2 and task-3 are ready
    update_task_status(plan, "task-1", "completed")
    ready = get_ready_tasks(plan)
    assert set(ready) == {"task-2", "task-3"}


def test_kb_initialization():
    """Test KB directory structure creation."""
    kb_dir = TEST_DIR / "kb"
    kb_dir.mkdir(parents=True, exist_ok=True)

    # Change to test directory
    import os
    original_dir = os.getcwd()
    os.chdir(TEST_DIR)

    try:
        initialize_kb()

        assert verify_kb_exists()
        assert (Path("kb") / "backend-patterns.md").exists()
        assert (Path("kb") / "decisions.log").exists()
        assert (Path("kb") / "dependencies.json").exists()
    finally:
        os.chdir(original_dir)


def test_decision_logging():
    """Test logging decisions to KB."""
    kb_dir = TEST_DIR / "kb"
    kb_dir.mkdir(parents=True, exist_ok=True)

    import os
    original_dir = os.getcwd()
    os.chdir(TEST_DIR)

    try:
        initialize_kb()

        log_decision(
            specialist="backend-architect",
            decision="Use JWT for authentication",
            rationale="Industry standard, stateless, scalable",
            affects=["backend-api", "frontend-auth"],
            ref="kb/backend-patterns.md#auth"
        )

        log_content = (Path("kb") / "decisions.log").read_text()
        assert "backend-architect" in log_content
        assert "Use JWT for authentication" in log_content
        assert "Industry standard" in log_content
    finally:
        os.chdir(original_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
