# Multi-Agent Dev Team Plugin - MVP Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build MVP of multi-agent coordination plugin with 4 specialists (Backend Architect, FastAPI, Code Reviewer, Coordinator) that can execute a simple task with DAG orchestration and knowledge base tracking.

**Architecture:** Claude Code plugin structure with skill-based invocation. Coordinator orchestrates specialists via Task tool, KB stored in file system (markdown + JSON), workspace/ for task handoffs. MVP validates core coordination patterns before scaling to full specialist roster.

**Tech Stack:**
- Python for plugin infrastructure
- JSON for structured data (task DAG, dependencies, KB graph)
- Markdown for documentation (KB patterns, decisions, workspace notes)
- Claude Code plugin API (skills directory, plugin.json manifest)

---

## Phase 1: Plugin Foundation

### Task 1: Plugin Structure Setup

**Files:**
- Create: `plugin.json`
- Create: `README.md`
- Create: `.gitignore`
- Create: `skills/README.md`

**Step 1: Create plugin manifest**

```json
{
  "name": "multi-agent-dev-team",
  "version": "0.1.0",
  "description": "Domain specialist agents that collaborate through shared knowledge to prevent codebase drift",
  "author": "Rhett",
  "skills": [
    "dev-team",
    "backend-architect",
    "fastapi-specialist",
    "code-reviewer"
  ],
  "requires": {
    "claude-code": ">=1.0.0"
  }
}
```

**Step 2: Create README**

```markdown
# Multi-Agent Dev Team Plugin

Domain specialist agents that coordinate through shared knowledge to prevent drift.

## Skills

- `/dev-team` - Coordinator for complex multi-domain tasks
- `/backend-architect` - System design and architectural patterns
- `/fastapi-specialist` - FastAPI endpoint implementation
- `/code-reviewer` - Code simplification and dead code removal

## MVP Scope

Limited to 4 specialists for validation. See docs/plans/2026-02-03-mvp-implementation.md.
```

**Step 3: Create .gitignore**

```.gitignore
__pycache__/
*.pyc
.pytest_cache/
.vscode/
*.swp
*.swo
*~
.DS_Store
work/
test_codebase/
```

**Step 4: Create skills directory README**

```markdown
# Skills Directory

Each subdirectory defines a skill (specialist or coordinator).

Structure:
- `skill-name/skill.md` - Skill definition and prompt
- `skill-name/config.json` - Skill configuration (optional)
```

**Step 5: Commit foundation**

```bash
cd "C:\Users\rhett\.claude\plugins\multi-agent-dev-team"
git add .
git commit -m "feat: initialize plugin structure with manifest and README"
```

---

### Task 2: Knowledge Base Schema

**Files:**
- Create: `kb/README.md`
- Create: `kb/.gitkeep`
- Create: `schemas/kb-pattern.schema.json`
- Create: `schemas/dependencies.schema.json`
- Create: `schemas/task-dag.schema.json`

**Step 1: Create KB directory README**

```markdown
# Knowledge Base

Shared memory that prevents drift across all specialist work.

## Structure

- `kb/backend-patterns.md` - Backend conventions
- `kb/frontend-patterns.md` - Frontend conventions
- `kb/api-contracts.md` - API schemas and contracts
- `kb/decisions.log` - Append-only decision history
- `kb/dependencies.json` - Cross-domain dependency graph

## Usage

**Before work (pre-flight):**
- Read relevant pattern files
- Check decision log for precedent

**During work (monitoring):**
- Reference patterns for consistency
- Update patterns if establishing new conventions

**After work (validation):**
- Log decisions with rationale
- Update dependencies if contracts changed
```

**Step 2: Create pattern file schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KB Pattern File Schema",
  "description": "Structure for domain pattern markdown files",
  "type": "object",
  "properties": {
    "domain": {
      "type": "string",
      "enum": ["backend", "frontend", "api-contracts", "docker", "matterport", "openai-agents"]
    },
    "patterns": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "description": {"type": "string"},
          "rationale": {"type": "string"},
          "example": {"type": "string"},
          "reference": {"type": "string"}
        },
        "required": ["name", "description"]
      }
    }
  }
}
```

**Step 3: Create dependencies schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KB Dependencies Schema",
  "description": "Cross-domain dependency graph",
  "type": "object",
  "patternProperties": {
    "^[a-z-]+$": {
      "type": "object",
      "properties": {
        "depends_on": {
          "type": "array",
          "items": {"type": "string"}
        },
        "used_by": {
          "type": "array",
          "items": {"type": "string"}
        },
        "contracts": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "type": {"type": "string"},
              "schema_ref": {"type": "string"}
            }
          }
        }
      }
    }
  }
}
```

**Step 4: Create task DAG schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Task DAG Schema",
  "description": "Coordinator task orchestration graph",
  "type": "object",
  "properties": {
    "plan_id": {"type": "string"},
    "created_at": {"type": "string", "format": "date-time"},
    "tasks": {
      "type": "object",
      "patternProperties": {
        "^task-[0-9]+$": {
          "type": "object",
          "properties": {
            "id": {"type": "string"},
            "title": {"type": "string"},
            "specialist": {"type": "string"},
            "status": {
              "type": "string",
              "enum": ["pending", "ready", "in-progress", "completed", "validated", "failed", "blocked"]
            },
            "dependencies": {
              "type": "array",
              "items": {"type": "string"}
            },
            "output_workspace": {"type": "string"},
            "kb_updates": {
              "type": "array",
              "items": {"type": "string"}
            },
            "started_at": {"type": "string", "format": "date-time"},
            "completed_at": {"type": "string", "format": "date-time"}
          },
          "required": ["id", "title", "specialist", "status"]
        }
      }
    }
  },
  "required": ["plan_id", "tasks"]
}
```

**Step 5: Commit schemas**

```bash
git add kb/ schemas/
git commit -m "feat: add KB structure and JSON schemas for DAG and dependencies"
```

---

## Phase 2: Specialist Skills

### Task 3: Backend Architect Specialist

**Files:**
- Create: `skills/backend-architect/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# Backend Architect Specialist

**Domain Expertise:**
- System design and service organization
- Architectural patterns and layer separation
- Design trade-offs and scalability
- Backend technology stack decisions

**Responsibilities:**
1. Design high-level architecture for backend features
2. Define service boundaries and data flow
3. Establish architectural patterns
4. Update `kb/backend-patterns.md` with design decisions

**Pre-flight Checks:**
```bash
# Read current backend patterns
cat kb/backend-patterns.md 2>/dev/null || echo "No patterns yet"

# Check decision log for precedent
grep "backend-architect" kb/decisions.log 2>/dev/null || echo "No prior decisions"

# Review workspace from coordinator
cat work/task-*.md 2>/dev/null || echo "No task context"
```

**Task Execution:**
1. Read task requirements from workspace file
2. Analyze current architecture patterns in KB
3. Design solution following established patterns
4. Document design in workspace for next specialist
5. Update KB patterns if introducing new conventions
6. Log decisions with rationale

**Post-work Updates:**
```bash
# Log decision (append to decisions.log)
echo "[$(date +%Y-%m-%d\ %H:%M)] [backend-architect] Decision: <what>" >> kb/decisions.log
echo "Rationale: <why>" >> kb/decisions.log
echo "Affects: <domains>" >> kb/decisions.log
echo "Ref: kb/backend-patterns.md#<section>" >> kb/decisions.log
echo "" >> kb/decisions.log
```

**Example Task:**
Given: "Design API endpoint for user authentication"

Output to `work/auth-design.md`:
```markdown
# Authentication Endpoint Design

## Architecture
- RESTful endpoint: POST /api/v1/auth/login
- Request: {email, password}
- Response: {access_token, refresh_token, user_id}

## Security
- Passwords hashed with bcrypt
- JWT tokens with 15min expiry
- Refresh tokens in HTTP-only cookies

## Data Flow
1. Validate credentials against database
2. Generate JWT access token
3. Generate refresh token, store in Redis
4. Return tokens to client

## Dependencies
- Depends on: database-session, redis-cache
- Used by: frontend-auth
```

**KB Update to `kb/backend-patterns.md`:**
```markdown
## Authentication Pattern

**Current Standard**: JWT with refresh tokens

- Access token: 15 minute expiry
- Refresh token: 7 day expiry in Redis
- Storage: HTTP-only cookies
- Validation: FastAPI Depends() with `get_current_user`

**Rationale**: See decisions.log 2026-02-03
```

---

**System Prompt for Backend Architect:**

You are the Backend Architect specialist for a multi-agent dev team.

**Your expertise:**
- System design, service organization, architectural patterns
- Backend technology stack (Python, FastAPI, databases, caching)
- Design trade-offs and scalability considerations

**Your workflow:**

1. **Pre-flight (before work):**
   - Read `kb/backend-patterns.md` for current conventions
   - Check `kb/decisions.log` for precedent
   - Read workspace file from coordinator for task context

2. **Execute task:**
   - Design solution following established patterns
   - Document design in workspace file for next specialist
   - Make architectural decisions with clear rationale

3. **Post-work (update KB):**
   - Update `kb/backend-patterns.md` if introducing new conventions
   - Log decisions to `kb/decisions.log` with format:
     ```
     [YYYY-MM-DD HH:MM] [backend-architect] Decision: <what>
     Rationale: <why>
     Affects: <domains>
     Ref: kb/backend-patterns.md#<section>
     ```
   - Update `kb/dependencies.json` if design creates new cross-domain contracts

**Output format:**
- Detailed design document to `work/<feature>-design.md`
- KB pattern updates if establishing new conventions
- Decision log entries for significant choices

**Example:**
Task: "Design OAuth authentication flow"
→ Output: `work/oauth-design.md` with endpoint specs, token flow, security model
→ Update: `kb/backend-patterns.md` with JWT pattern
→ Log: Decision about token expiry with rationale
```

**Step 2: Commit backend architect skill**

```bash
git add skills/backend-architect/
git commit -m "feat: add backend architect specialist skill"
```

---

### Task 4: FastAPI Specialist

**Files:**
- Create: `skills/fastapi-specialist/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# FastAPI Specialist

**Domain Expertise:**
- FastAPI framework internals and best practices
- Endpoint implementation, routing, middleware
- Pydantic validation patterns
- Dependency injection with Depends()

**Responsibilities:**
1. Implement FastAPI endpoints following KB patterns
2. Ensure type safety with Pydantic models
3. Follow async/await patterns consistently
4. Update `kb/api-contracts.md` with endpoint schemas

**Pre-flight Checks:**
```bash
# Read backend patterns
cat kb/backend-patterns.md

# Read design from backend architect
cat work/*-design.md

# Check API contracts
cat kb/api-contracts.md 2>/dev/null || echo "No contracts yet"
```

**Task Execution:**
1. Read design document from workspace
2. Implement endpoints following FastAPI best practices
3. Add Pydantic models for request/response validation
4. Write tests for endpoints
5. Document API contract in KB

**Post-work Updates:**
```bash
# Update API contracts
echo "## POST /api/v1/endpoint" >> kb/api-contracts.md
echo "Request: {schema}" >> kb/api-contracts.md
echo "Response: {schema}" >> kb/api-contracts.md
echo "" >> kb/api-contracts.md
```

---

**System Prompt for FastAPI Specialist:**

You are the FastAPI Specialist for a multi-agent dev team.

**Your expertise:**
- FastAPI framework, routing, middleware, dependency injection
- Pydantic validation and type safety
- Async/await patterns
- RESTful API design

**Your workflow:**

1. **Pre-flight:**
   - Read `kb/backend-patterns.md` for conventions
   - Read design document from `work/*-design.md` (from backend-architect)
   - Check `kb/api-contracts.md` for existing endpoints

2. **Execute task:**
   - Implement endpoints following design
   - Use Pydantic models for validation
   - Follow async/await patterns from KB
   - Write implementation notes to `work/*-implementation-notes.md`

3. **Post-work:**
   - Update `kb/api-contracts.md` with endpoint schemas
   - Log decisions if deviating from design (with rationale)

**Implementation pattern (from KB):**
```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()

class RequestModel(BaseModel):
    field: str

class ResponseModel(BaseModel):
    result: str

@router.post("/endpoint", response_model=ResponseModel)
async def endpoint(
    request: RequestModel,
    user = Depends(get_current_user)
):
    # Implementation
    return ResponseModel(result="success")
```

**Output:**
- Code files: `backend/routers/<feature>.py`, `backend/models/<feature>.py`
- Implementation notes: `work/<feature>-implementation-notes.md`
- KB updates: `kb/api-contracts.md` with schemas
```

**Step 2: Commit FastAPI specialist skill**

```bash
git add skills/fastapi-specialist/
git commit -m "feat: add FastAPI specialist skill"
```

---

### Task 5: Code Reviewer Specialist

**Files:**
- Create: `skills/code-reviewer/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# Code Reviewer Specialist

**Domain Expertise:**
- Code simplification and refactoring
- Dead code detection and removal
- Anti-pattern identification
- Code quality best practices

**Responsibilities:**
1. Review code for simplification opportunities
2. Detect and remove dead/unused code
3. Flag anti-patterns and suggest improvements
4. Ensure KB pattern compliance

**Pre-flight Checks:**
```bash
# Read implementation notes
cat work/*-implementation-notes.md

# Read relevant KB patterns
cat kb/backend-patterns.md
cat kb/frontend-patterns.md 2>/dev/null || true
```

**Task Execution:**
1. Read code written by implementation specialist
2. Check compliance with KB patterns
3. Identify simplification opportunities
4. Remove dead code
5. Suggest refactoring if anti-patterns found

**Review Checklist:**
- ✅ Follows KB patterns?
- ✅ No dead/unused imports or functions?
- ✅ No code duplication?
- ✅ Proper error handling?
- ✅ Type safety (Pydantic models, type hints)?
- ✅ Async/await used consistently?

---

**System Prompt for Code Reviewer:**

You are the Code Reviewer specialist for a multi-agent dev team.

**Your expertise:**
- Code simplification and clarity
- Dead code detection
- Anti-pattern identification
- Refactoring best practices

**Your workflow:**

1. **Pre-flight:**
   - Read implementation notes from `work/*-implementation-notes.md`
   - Read relevant KB patterns to understand conventions

2. **Execute review:**
   - Read code files
   - Check pattern compliance against KB
   - Identify simplification opportunities
   - Detect dead code (unused imports, functions, variables)
   - Flag anti-patterns

3. **Apply fixes:**
   - Use Edit tool to simplify code
   - Remove dead code
   - Refactor duplicated logic into helpers

4. **Post-review:**
   - Write review summary to `work/<feature>-review.md`
   - Log significant refactoring decisions

**Review criteria:**
- KB pattern compliance
- No dead code
- No duplication
- Proper error handling
- Type safety
- Async/await consistency

**Example review finding:**
```markdown
# Review: OAuth Implementation

## Simplifications Applied
1. Removed unused `datetime` import
2. Extracted duplicate password validation to `validate_password()` helper
3. Simplified error handling with early returns

## Pattern Compliance
✅ Follows JWT pattern from kb/backend-patterns.md
✅ Uses Pydantic validation
✅ Async/await consistent

## Suggestions for Future
- Consider adding rate limiting to login endpoint
```
```

**Step 2: Commit code reviewer skill**

```bash
git add skills/code-reviewer/
git commit -m "feat: add code reviewer specialist skill"
```

---

## Phase 3: Coordinator

### Task 6: Coordinator Skill (MVP)

**Files:**
- Create: `skills/dev-team/skill.md`
- Create: `utils/dag_parser.py`
- Create: `utils/kb_manager.py`

**Step 1: Write simplified coordinator skill**

```markdown
# Dev Team Coordinator (MVP)

**Purpose:** Orchestrate multiple specialists to complete complex multi-domain tasks.

**MVP Scope:**
- Simplified planning (user provides task breakdown manually)
- Basic DAG execution (sequential for MVP, parallelization later)
- KB initialization and tracking
- Checkpoint workflow (simplified)

**Workflow:**

## Phase 1: Planning

**Input:** User provides task with breakdown

Example:
```
/dev-team "Add authenticated API endpoint for user profile

Tasks:
1. backend-architect: Design profile endpoint
2. fastapi-specialist: Implement endpoint with Pydantic models
3. code-reviewer: Review and simplify implementation
```

**Coordinator actions:**
1. Parse task breakdown into DAG
2. Create plan JSON in `work/plan.json`
3. Initialize KB if needed
4. Present plan to user for approval

## Phase 2: Execution

**For each task in DAG:**
1. Check dependencies satisfied
2. Invoke specialist via Task tool
3. Wait for completion
4. Run checkpoint validation
5. Update task status

**Checkpoint (after each task):**
1. Verify specialist updated KB if needed
2. Check workspace files created for next specialist
3. Validate pattern compliance

## Phase 3: Completion

1. Verify all tasks completed
2. Present summary to user
3. Offer workspace cleanup

---

**System Prompt for Coordinator (MVP):**

You are the Coordinator for a multi-agent dev team (MVP version).

**Your role:**
- Parse user task into specialist assignments
- Execute tasks via Task tool invocations
- Validate KB updates and pattern compliance
- Manage checkpoints between tasks

**MVP Limitations:**
- User provides task breakdown (no auto-planning yet)
- Sequential execution (no parallelization yet)
- Simplified checkpoints (basic validation only)

**Workflow:**

1. **Parse user input:**
   Extract task list with specialist assignments

2. **Create plan:**
   ```json
   {
     "plan_id": "feature-YYYY-MM-DD-HH-MM",
     "tasks": {
       "task-1": {
         "id": "task-1",
         "title": "Design X",
         "specialist": "backend-architect",
         "status": "pending",
         "dependencies": []
       },
       "task-2": {
         "id": "task-2",
         "title": "Implement X",
         "specialist": "fastapi-specialist",
         "status": "pending",
         "dependencies": ["task-1"]
       }
     }
   }
   ```

3. **Execute tasks sequentially:**
   ```python
   for task in tasks:
       if dependencies_satisfied(task):
           invoke_specialist(task.specialist, task.title)
           run_checkpoint(task)
           update_status(task, "completed")
   ```

4. **Checkpoint after each task:**
   - Verify workspace file created (e.g., `work/design.md`)
   - Check KB updated if new patterns introduced
   - Validate next task has required inputs

5. **Present completion summary:**
   - List completed tasks
   - Show KB updates made
   - Offer workspace cleanup

**Example invocation:**
```
User: /dev-team "Add login endpoint
Tasks:
1. backend-architect: Design login flow
2. fastapi-specialist: Implement /api/v1/auth/login
3. code-reviewer: Review and simplify"

Coordinator:
→ Creates plan.json with 3 tasks
→ Invokes backend-architect via Task tool
→ Waits for completion, runs checkpoint
→ Invokes fastapi-specialist with work/login-design.md context
→ Waits for completion, runs checkpoint
→ Invokes code-reviewer with implementation files
→ Waits for completion, runs final checkpoint
→ Presents summary with KB updates
```
```

**Step 2: Create DAG parser utility (simplified)**

```python
# utils/dag_parser.py
"""Simple DAG parser for MVP coordinator."""

import json
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
```

**Step 3: Create KB manager utility**

```python
# utils/kb_manager.py
"""Knowledge base initialization and management."""

import os
import json
from pathlib import Path

KB_DIR = Path("kb")

def initialize_kb():
    """Create KB directory structure if it doesn't exist."""
    KB_DIR.mkdir(exist_ok=True)

    # Create empty pattern files if they don't exist
    patterns = ["backend-patterns.md", "frontend-patterns.md", "api-contracts.md"]
    for pattern in patterns:
        path = KB_DIR / pattern
        if not path.exists():
            path.write_text(f"# {pattern.replace('-', ' ').title()}\n\n")

    # Create empty decisions log
    log_path = KB_DIR / "decisions.log"
    if not log_path.exists():
        log_path.write_text("# Decision Log\n\n")

    # Create empty dependencies graph
    deps_path = KB_DIR / "dependencies.json"
    if not deps_path.exists():
        deps_path.write_text(json.dumps({}, indent=2))


def verify_kb_exists() -> bool:
    """Check if KB is initialized."""
    return KB_DIR.exists() and (KB_DIR / "decisions.log").exists()


def log_decision(specialist: str, decision: str, rationale: str, affects: List[str], ref: str = ""):
    """Append decision to KB log."""
    from datetime import datetime

    log_path = KB_DIR / "decisions.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    entry = f"[{timestamp}] [{specialist}] Decision: {decision}\n"
    entry += f"Rationale: {rationale}\n"
    entry += f"Affects: {', '.join(affects)}\n"
    if ref:
        entry += f"Ref: {ref}\n"
    entry += "\n"

    with log_path.open('a') as f:
        f.write(entry)
```

**Step 4: Commit coordinator and utilities**

```bash
git add skills/dev-team/ utils/
git commit -m "feat: add MVP coordinator skill with DAG parser and KB manager"
```

---

## Phase 4: Testing & Validation

### Task 7: Integration Test

**Files:**
- Create: `tests/test_mvp_flow.py`
- Create: `test_codebase/backend/routers/.gitkeep`
- Create: `test_codebase/kb/.gitkeep`

**Step 1: Create test codebase structure**

```bash
mkdir -p test_codebase/backend/routers
mkdir -p test_codebase/backend/models
mkdir -p test_codebase/kb
mkdir -p test_codebase/work
touch test_codebase/backend/__init__.py
touch test_codebase/backend/routers/__init__.py
touch test_codebase/backend/models/__init__.py
```

**Step 2: Write integration test**

```python
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
```

**Step 3: Run tests**

```bash
cd "C:\Users\rhett\.claude\plugins\multi-agent-dev-team"
python -m pytest tests/test_mvp_flow.py -v
```

Expected output:
```
tests/test_mvp_flow.py::test_dag_parser PASSED
tests/test_mvp_flow.py::test_ready_tasks PASSED
tests/test_mvp_flow.py::test_kb_initialization PASSED
tests/test_mvp_flow.py::test_decision_logging PASSED
```

**Step 4: Commit tests**

```bash
git add tests/ test_codebase/
git commit -m "test: add integration tests for DAG parser and KB manager"
```

---

### Task 8: End-to-End Validation

**Goal:** Manually test full MVP flow with coordinator orchestrating specialists.

**Test scenario:** "Add authenticated user profile endpoint"

**Step 1: Create test plan file**

```markdown
# Test Plan: Add User Profile Endpoint

## Tasks
1. backend-architect: Design GET /api/v1/users/{id} endpoint
2. fastapi-specialist: Implement endpoint with Pydantic models (depends on: 1)
3. code-reviewer: Review and simplify (depends on: 2)

## Expected Flow

**Task 1 (backend-architect):**
- Input: Task description
- Output: `work/user-profile-design.md` with endpoint spec
- KB update: `kb/backend-patterns.md` (if new pattern)
- Decision log: If significant design choice made

**Task 2 (fastapi-specialist):**
- Input: `work/user-profile-design.md`
- Output: `backend/routers/users.py`, `backend/models/user.py`
- KB update: `kb/api-contracts.md` with endpoint schema
- Notes: `work/user-profile-implementation-notes.md`

**Task 3 (code-reviewer):**
- Input: `work/user-profile-implementation-notes.md`, code files
- Output: Simplified code (via Edit tool)
- KB check: Verify pattern compliance
- Summary: `work/user-profile-review.md`

## Success Criteria
- All 3 tasks complete successfully
- KB updated with new patterns and decisions
- Code follows KB conventions
- No dead code in final implementation
```

**Step 2: Invoke coordinator skill manually**

```
/dev-team "Add authenticated user profile endpoint

Tasks:
1. backend-architect: Design GET /api/v1/users/{id} endpoint
2. fastapi-specialist: Implement endpoint with Pydantic models (depends on: 1)
3. code-reviewer: Review and simplify (depends on: 2)"
```

**Step 3: Verify outputs**

Check files created:
- `work/plan.json` - Task DAG
- `work/user-profile-design.md` - Design from backend-architect
- `work/user-profile-implementation-notes.md` - Notes from fastapi-specialist
- `work/user-profile-review.md` - Review summary
- `backend/routers/users.py` - Implementation
- `kb/backend-patterns.md` - Updated patterns
- `kb/api-contracts.md` - New endpoint schema
- `kb/decisions.log` - Design decisions

**Step 4: Validate KB consistency**

```bash
# Check all decisions reference KB sections
grep "Ref: kb/" kb/decisions.log

# Check API contracts match implementation
# (Manual review of endpoint in users.py vs kb/api-contracts.md)
```

**Step 5: Document validation results**

Create `docs/mvp-validation-results.md` with:
- Test scenario executed
- Files created (screenshots or file tree)
- KB updates made
- Issues encountered
- Next steps for full implementation

**Step 6: Commit validation**

```bash
git add docs/mvp-validation-results.md
git commit -m "docs: add MVP validation results"
```

---

## Phase 5: Documentation & Handoff

### Task 9: Plugin Documentation

**Files:**
- Create: `docs/USER_GUIDE.md`
- Create: `docs/SPECIALIST_GUIDE.md`
- Create: `docs/ARCHITECTURE.md`

**Step 1: Write user guide**

```markdown
# User Guide: Multi-Agent Dev Team

## Quick Start

### Setup
1. Plugin auto-loaded from `~/.claude/plugins/multi-agent-dev-team/`
2. Invoke via `/dev-team` skill

### Basic Usage

**Format:**
```
/dev-team "Feature description

Tasks:
1. specialist-name: Task description
2. specialist-name: Task description (depends on: 1)
3. specialist-name: Task description (depends on: 2)"
```

**Example:**
```
/dev-team "Add login endpoint

Tasks:
1. backend-architect: Design POST /api/v1/auth/login
2. fastapi-specialist: Implement with JWT tokens (depends on: 1)
3. code-reviewer: Review and simplify (depends on: 2)"
```

## Available Specialists (MVP)

| Specialist | Use For |
|------------|---------|
| `backend-architect` | System design, architecture |
| `fastapi-specialist` | FastAPI endpoint implementation |
| `code-reviewer` | Code simplification, dead code removal |

## How It Works

1. **Planning:** Coordinator parses task list into DAG
2. **Execution:** Specialists invoked sequentially via Task tool
3. **Checkpoints:** After each task, KB validated and next task prepared
4. **Completion:** Summary presented with KB updates

## Knowledge Base

The KB prevents drift by tracking:
- **Patterns** (`kb/*-patterns.md`) - Current conventions per domain
- **Decisions** (`kb/decisions.log`) - Historical record with rationale
- **Contracts** (`kb/api-contracts.md`) - Cross-domain interfaces

Specialists read KB before work, update KB after work.

## Workspace Files

Temporary handoff files in `work/`:
- Design documents from architects
- Implementation notes from implementers
- Review summaries from reviewers

Cleaned up after plan completion.
```

**Step 2: Write specialist guide**

```markdown
# Specialist Guide

## Creating a New Specialist

### Directory Structure
```
skills/
  specialist-name/
    skill.md          # Skill definition and system prompt
    config.json       # Optional configuration
```

### Skill Template

```markdown
# Specialist Name

**Domain Expertise:**
- Area 1
- Area 2

**Responsibilities:**
1. What this specialist does
2. What KB files it updates

**Pre-flight Checks:**
```bash
# Commands to read KB and workspace before starting
```

**Task Execution:**
1. Steps the specialist follows

**Post-work Updates:**
```bash
# Commands to update KB after completing work
```

---

**System Prompt:**

You are the [Name] specialist.

[Detailed prompt with workflow, KB usage, output format]
```
```

### Integration with Coordinator

Add specialist to `plugin.json`:
```json
{
  "skills": ["dev-team", "your-specialist"]
}
```

Update coordinator to recognize specialist name in task parsing.
```

**Step 3: Write architecture doc**

```markdown
# Architecture: Multi-Agent Dev Team Plugin

## Overview

Claude Code plugin with coordinator-specialist pattern. Coordinator orchestrates specialists via Task tool, KB prevents drift, workspace enables handoffs.

## Components

### Coordinator (`skills/dev-team/`)
- Parses user task into DAG
- Invokes specialists sequentially (MVP) or parallel (future)
- Validates checkpoints
- Manages KB and workspace

### Specialists (`skills/*/`)
- Domain experts (backend-architect, fastapi-specialist, code-reviewer, etc.)
- Read KB for patterns, write KB for decisions
- Consume workspace from predecessors, produce workspace for successors

### Knowledge Base (`kb/`)
- `*-patterns.md` - Current conventions per domain
- `decisions.log` - Append-only decision history
- `dependencies.json` - Cross-domain contracts (future)

### Workspace (`work/`)
- Ephemeral task handoff files
- Design docs, implementation notes, review summaries
- Cleaned up after plan completion

### Utilities (`utils/`)
- `dag_parser.py` - Parse task list into JSON DAG
- `kb_manager.py` - KB initialization and logging

## Data Flow

```
User → Coordinator → Parse DAG → Initialize KB
  ↓
For each task:
  ↓
  Invoke Specialist → Read KB + Workspace
    ↓
    Execute Task → Write Code + Workspace + KB
    ↓
  Checkpoint → Validate KB updates
  ↓
Next task (with predecessor's workspace)
  ↓
Completion → Present summary
```

## MVP Limitations

- Sequential execution (no parallelization)
- Manual task breakdown (no auto-planning)
- Simplified checkpoints (basic validation)
- 4 specialists only

## Future Enhancements

1. Auto-planning phase (coordinator consults specialists for task breakdown)
2. Parallel execution (DAG parallelization)
3. Advanced checkpoints (peer review, cross-domain validation)
4. Full specialist roster (11 specialists)
5. Adaptive error recovery
6. Intent analysis for implicit dependencies
```

**Step 4: Commit documentation**

```bash
git add docs/
git commit -m "docs: add user guide, specialist guide, and architecture"
```

---

## Phase 6: Packaging & Deployment

### Task 10: Plugin Packaging

**Step 1: Verify plugin structure**

```bash
cd "C:\Users\rhett\.claude\plugins\multi-agent-dev-team"

# Expected structure:
# plugin.json
# README.md
# skills/
#   dev-team/skill.md
#   backend-architect/skill.md
#   fastapi-specialist/skill.md
#   code-reviewer/skill.md
# utils/
#   dag_parser.py
#   kb_manager.py
# kb/ (template, copied to user codebase)
# schemas/
# docs/
# tests/

tree /F
```

**Step 2: Add plugin activation test**

```bash
# Test that Claude Code recognizes the plugin
claude --list-skills | grep "dev-team"
```

Expected: `dev-team` appears in skill list

**Step 3: Create CHANGELOG**

```markdown
# Changelog

## [0.1.0] - 2026-02-03

### Added
- MVP coordinator skill (`/dev-team`)
- Backend Architect specialist
- FastAPI Specialist
- Code Reviewer specialist
- DAG parser for task orchestration
- KB manager for drift prevention
- Integration tests
- Documentation (user guide, specialist guide, architecture)

### Scope
- 4 specialists (MVP)
- Sequential task execution
- Basic checkpoint validation
- File-based KB (markdown + JSON)

### Limitations
- No auto-planning (user provides task breakdown)
- No parallel execution
- No adaptive error recovery
- No intent analysis

## [Future]

### Planned
- Full specialist roster (11 specialists)
- Auto-planning phase
- DAG parallelization
- Advanced checkpoints with peer review
- Adaptive error recovery
- Intent analysis for implicit dependencies
```

**Step 4: Final commit and tag**

```bash
git add CHANGELOG.md
git commit -m "chore: add CHANGELOG for MVP release"
git tag -a v0.1.0 -m "MVP release: 4 specialists with basic DAG orchestration"
git log --oneline --graph
```

---

## Success Criteria

MVP is complete when:

✅ Plugin structure follows Claude Code standards
✅ 4 specialist skills defined with system prompts
✅ Coordinator skill can parse task DAG
✅ KB manager initializes KB directory
✅ Integration tests pass
✅ End-to-end validation succeeds with test scenario
✅ Documentation complete (user guide, specialist guide, architecture)
✅ Plugin recognized by Claude Code (`/dev-team` skill available)

---

## Next Steps After MVP

1. **Gather feedback** - Use MVP on real tasks, identify pain points
2. **Add auto-planning** - Coordinator consults specialists for task breakdown
3. **Implement parallelization** - DAG parallel execution for independent tasks
4. **Expand specialist roster** - Add remaining 7 specialists (Docker, OpenAI Agents, UI/UX, etc.)
5. **Advanced checkpoints** - Peer review by specialists, cross-domain validation
6. **Error recovery** - Adaptive recovery with loop-back to prerequisite specialists
7. **Intent analysis** - AI-powered impact detection for implicit dependencies

---

## Appendix: File Tree

```
multi-agent-dev-team/
├── plugin.json
├── README.md
├── CHANGELOG.md
├── .gitignore
├── docs/
│   ├── plans/
│   │   └── 2026-02-03-mvp-implementation.md
│   ├── USER_GUIDE.md
│   ├── SPECIALIST_GUIDE.md
│   ├── ARCHITECTURE.md
│   └── mvp-validation-results.md
├── skills/
│   ├── README.md
│   ├── dev-team/
│   │   └── skill.md
│   ├── backend-architect/
│   │   └── skill.md
│   ├── fastapi-specialist/
│   │   └── skill.md
│   └── code-reviewer/
│       └── skill.md
├── utils/
│   ├── dag_parser.py
│   └── kb_manager.py
├── schemas/
│   ├── kb-pattern.schema.json
│   ├── dependencies.schema.json
│   └── task-dag.schema.json
├── kb/
│   └── README.md
├── tests/
│   └── test_mvp_flow.py
└── test_codebase/
    ├── backend/
    ├── kb/
    └── work/
```
