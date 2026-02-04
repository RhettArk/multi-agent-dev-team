# Utils Module

Core utilities for the multi-agent dev team coordinator.

## Files

### dag_parser.py

Parses task lists into DAG structure and manages task dependencies.

**Functions:**
- `parse_task_list(task_lines)` - Parse task list into plan JSON
- `get_ready_tasks(plan)` - Get tasks ready to execute (dependencies satisfied)
- `update_task_status(plan, task_id, status)` - Update task status with timestamps

### kb_manager.py

Knowledge base initialization and management.

**Functions:**
- `initialize_kb()` - Create KB directory structure
- `verify_kb_exists()` - Check if KB is initialized
- `log_decision(specialist, decision, rationale, affects, ref)` - Append decision to KB log

### parallel_executor.py

Parallel task execution engine with DAG orchestration.

**Classes:**
- `ParallelExecutor` - Executes tasks in parallel based on DAG dependencies
  - `execute_plan()` - Main execution loop
  - `execute_task(task_id)` - Execute single task via specialist invocation
  - `invoke_specialist(specialist, task_title, task_id)` - Invoke specialist (placeholder)
  - `run_checkpoint(task_id, result)` - Basic checkpoint validation
  - `is_plan_complete()` - Check if all tasks completed/blocked

**Functions:**
- `execute_plan_parallel(plan)` - Module-level async function for plan execution

**Configuration:**
- `max_parallel = 3` - Maximum concurrent specialist invocations

### checkpoint_validator.py

Advanced checkpoint validation with peer review (Task 17).

**Classes:**
- `CheckpointValidator` - Comprehensive checkpoint validation
  - `run_checkpoint()` - Full checkpoint workflow
  - `automatic_validation()` - Fast validation checks
  - `peer_review()` - Cross-specialist validation
  - `kb_sync()` - Knowledge base synchronization
  - `final_approval()` - Mark task as validated

### error_recovery.py

Adaptive error recovery system with loop-back and escalation (Task 18).

**Classes:**
- `ErrorRecoverySystem` - Handles task failures with recovery strategies
  - `handle_failure(task_id, error)` - Main failure handling
  - `loop_back(task_id)` - Re-invoke prerequisite specialist
  - `escalate(task_id)` - Involve senior specialist
  - `abort(task_id)` - Mark as blocked and stop

## Usage Example

```python
import asyncio
from utils.dag_parser import parse_task_list
from utils.parallel_executor import execute_plan_parallel

# Parse task list
task_lines = [
    'backend-architect: Design API',
    'fastapi-specialist: Implement API (depends on: 1)',
    'code-reviewer: Review code (depends on: 2)'
]
plan = parse_task_list(task_lines)

# Execute in parallel
async def main():
    result = await execute_plan_parallel(plan)
    for task_id, task in result['tasks'].items():
        print(f'{task_id}: {task["status"]}')

asyncio.run(main())
```

## Integration

The coordinator skill (`skills/dev-team/skill.md`) uses these utilities:

1. **Planning:** `dag_parser.parse_task_list()` or auto_planner
2. **Execution:** `parallel_executor.execute_plan_parallel()`
3. **Checkpoints:** `checkpoint_validator.CheckpointValidator`
4. **Recovery:** `error_recovery.ErrorRecoverySystem`
5. **KB:** `kb_manager.initialize_kb()`, `log_decision()`
