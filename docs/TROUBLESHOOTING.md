# Multi-Agent Dev Team - Troubleshooting Guide

## Common Issues

### Import Errors

#### Python Module Not Found

**Issue:**
```
ModuleNotFoundError: No module named 'utils.auto_planner'
```

**Cause:**
- Missing `__init__.py` in utils directory
- Python path not including plugin directory

**Fix:**
```bash
# Verify __init__.py exists
ls ~/.claude/plugins/multi-agent-dev-team/utils/__init__.py

# If missing, create it
touch ~/.claude/plugins/multi-agent-dev-team/utils/__init__.py
```

---

#### Circular Import in Utils

**Issue:**
```
ImportError: cannot import name 'X' from partially initialized module
```

**Cause:**
- Circular dependencies between utils modules

**Fix:**
Move imports inside functions instead of module-level:
```python
# Bad
from utils.parallel_executor import execute_plan

def my_function():
    execute_plan()

# Good
def my_function():
    from utils.parallel_executor import execute_plan
    execute_plan()
```

---

### Specialist Failures

#### Specialist Not Being Assigned

**Issue:**
Auto-planner doesn't assign the expected specialist.

**Cause:**
- Specialist's skill.md has unclear role description
- Feature description doesn't match specialist's domain

**Fix:**
1. Be more specific in your request:
   ```
   /dev-team "Add JWT auth (backend focus)"
   ```

2. Check specialist's skill.md:
   ```bash
   cat ~/.claude/plugins/multi-agent-dev-team/skills/fastapi-specialist/skill.md
   ```

3. Update role description to be clearer

---

#### Specialist Task Fails Repeatedly

**Issue:**
Same task fails even after recovery attempts.

**Cause:**
- Fundamental design issue
- Missing prerequisite information
- KB patterns are contradictory

**Fix:**
1. Check error classification:
   ```python
   # In error_recovery.py logs
   # Look for: "Classified as FUNDAMENTAL"
   ```

2. Manually intervene:
   - Reject the plan
   - Add constraints to clarify requirements
   - Update KB patterns to resolve conflicts

3. Clear KB if patterns are stale:
   ```bash
   rm ~/.claude/plugins/multi-agent-dev-team/kb/*.md
   # Will auto-initialize on next run
   ```

---

#### Specialist Produces Incorrect Output

**Issue:**
Specialist completes task but output doesn't match expectations.

**Cause:**
- KB patterns not followed
- Checkpoint validation too lenient
- Peer review not catching issues

**Fix:**
1. Check what KB patterns exist:
   ```bash
   cat ~/.claude/plugins/multi-agent-dev-team/kb/backend-patterns.md
   ```

2. Manually update patterns:
   ```markdown
   # kb/backend-patterns.md

   ## Endpoint Naming
   - Use snake_case for all endpoints
   - Prefix with API version: /api/v1/resource
   ```

3. Use strict checkpoint mode:
   ```
   /dev-team "Add feature" (strict checkpoints)
   ```

---

### KB Conflicts

#### Conflicting Patterns

**Issue:**
```
Error: KB pattern conflict detected
backend-patterns.md says: "Use Pydantic v1"
api-contracts.md says: "Use Pydantic v2"
```

**Cause:**
- Patterns evolved but files not updated
- Multiple specialists updating same patterns

**Fix:**
1. Manually resolve conflict:
   ```bash
   # Edit both files to use consistent pattern
   vim ~/.claude/plugins/multi-agent-dev-team/kb/backend-patterns.md
   vim ~/.claude/plugins/multi-agent-dev-team/kb/api-contracts.md
   ```

2. Log resolution decision:
   ```bash
   echo "$(date): Resolved Pydantic version conflict - using v2" >> ~/.claude/plugins/multi-agent-dev-team/kb/decisions.log
   ```

---

#### KB Growing Too Large

**Issue:**
KB files become very large and slow to read.

**Cause:**
- Many decisions logged over time
- Patterns not consolidated

**Fix:**
1. Archive old decisions:
   ```bash
   mv kb/decisions.log kb/decisions.archive.$(date +%Y%m%d).log
   touch kb/decisions.log
   ```

2. Consolidate patterns:
   ```bash
   # Manually review and simplify pattern files
   vim kb/backend-patterns.md
   # Remove deprecated patterns
   # Merge similar patterns
   ```

---

### Parallel Execution Issues

#### Tasks Running That Should Be Blocked

**Issue:**
Dependent task starts before prerequisite completes.

**Cause:**
- DAG parser not detecting dependency
- Dependencies not declared in plan

**Fix:**
1. Check plan dependencies:
   ```python
   # Look in workspace/current_plan.json
   {
     "tasks": {
       "t-003": {
         "depends_on": ["t-001", "t-002"]  # Should be here
       }
     }
   }
   ```

2. If missing, auto-planner needs improvement:
   - Add explicit dependency hints in request:
     ```
     /dev-team "Add feature (backend first, then frontend)"
     ```

---

#### Concurrent Task Conflicts

**Issue:**
Two parallel tasks modify the same file causing conflicts.

**Cause:**
- Dependencies not properly inferred
- File-level conflicts not detected

**Fix:**
1. Short-term: Reduce concurrency:
   ```python
   # In parallel_executor.py
   MAX_CONCURRENT_TASKS = 1  # Sequential execution
   ```

2. Long-term: Add file-level dependency tracking:
   ```python
   # In auto_planner.py
   # Track which files each task modifies
   # Infer dependency if tasks touch same files
   ```

---

#### Parallel Execution Slower Than Sequential

**Issue:**
Parallel execution takes longer than expected.

**Cause:**
- Overhead of coordination
- Many dependencies (not truly parallel)
- Task batch sizes too small

**Fix:**
1. Check DAG structure:
   ```bash
   # Look for long dependency chains
   cat workspace/current_plan.json | jq '.tasks[] | select(.depends_on | length > 2)'
   ```

2. Adjust batching strategy:
   ```python
   # In parallel_executor.py
   MAX_CONCURRENT_TASKS = 5  # Increase if tasks are independent
   ```

---

### Checkpoint Issues

#### Checkpoints Too Strict

**Issue:**
Every task requires manual approval even for trivial changes.

**Cause:**
- Checkpoint validation too sensitive
- User approval always required

**Fix:**
1. Use lenient checkpoint mode:
   ```
   /dev-team "Add feature" (lenient checkpoints)
   ```

2. Adjust validation thresholds:
   ```python
   # In checkpoint_validator.py
   def should_pause_for_approval(checkpoint_result):
       # Only pause on failures
       return checkpoint_result['status'] == 'fail'
   ```

---

#### Checkpoints Missing Issues

**Issue:**
Checkpoint passes but output has obvious problems.

**Cause:**
- Validation not comprehensive enough
- Peer review not thorough

**Fix:**
1. Use strict checkpoint mode:
   ```
   /dev-team "Add feature" (strict checkpoints)
   ```

2. Enhance validation:
   ```python
   # In checkpoint_validator.py
   def validate_task_output(task_output):
       # Add more checks
       checks = [
           check_syntax(task_output),
           check_structure(task_output),
           check_imports(task_output),
           check_conventions(task_output),  # Add this
           check_security(task_output)      # Add this
       ]
       return all(checks)
   ```

---

### Error Recovery Issues

#### Recovery Loop Infinite

**Issue:**
System keeps looping back to prerequisite specialist.

**Cause:**
- Prerequisite specialist not providing clear fix
- Recovery attempt limit not working

**Fix:**
1. Check recovery attempts:
   ```python
   # In error_recovery.py
   MAX_RECOVERY_ATTEMPTS = 2  # Ensure this is set
   ```

2. Add escalation after N attempts:
   ```python
   def handle_task_failure(task_id, error, plan, attempt=0):
       if attempt >= MAX_RECOVERY_ATTEMPTS:
           return escalate_to_user(task_id, error)

       # Try recovery
       recovery_result = attempt_recovery(task_id, error)
       if recovery_result['success']:
           return recovery_result

       # Recurse with attempt count
       return handle_task_failure(task_id, error, plan, attempt + 1)
   ```

---

#### Recovery Not Attempted

**Issue:**
Fixable errors are escalated to user immediately.

**Cause:**
- Error classified as FUNDAMENTAL incorrectly
- Recovery disabled

**Fix:**
1. Check classification logic:
   ```python
   # In error_recovery.py
   def classify_failure(error):
       # Review classification rules
       if "design unclear" in error.lower():
           return "FIXABLE"  # Should loop back
       return "FUNDAMENTAL"
   ```

2. Enable recovery:
   ```python
   # In coordinator skill
   ENABLE_ERROR_RECOVERY = True
   ```

---

## Debugging Tips

### Enable Verbose Logging

Add debug logging to track execution:

```python
# In utils/__init__.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

---

### Inspect Workspace State

Check current execution state:

```bash
# View current plan
cat ~/.claude/plugins/multi-agent-dev-team/workspace/current_plan.json | jq

# View task history
cat ~/.claude/plugins/multi-agent-dev-team/workspace/task_history.json | jq

# View checkpoint state
cat ~/.claude/plugins/multi-agent-dev-team/workspace/checkpoint_state.json | jq
```

---

### Trace Specialist Invocations

Add tracing to see specialist calls:

```python
# In coordinator skill
async def invoke_specialist(specialist, task, context):
    print(f"[TRACE] Invoking {specialist} for task: {task['description']}")
    result = await _invoke_specialist_impl(specialist, task, context)
    print(f"[TRACE] {specialist} completed with status: {result['status']}")
    return result
```

---

### Test Individual Specialists

Test specialists in isolation:

```bash
# Test a single specialist
cd ~/.claude/plugins/multi-agent-dev-team
python -m pytest tests/test_specialists.py::test_fastapi_specialist -v
```

---

### Validate KB Structure

Ensure KB files are valid:

```bash
# Check markdown syntax
mdl ~/.claude/plugins/multi-agent-dev-team/kb/*.md

# Check JSON syntax
jq empty ~/.claude/plugins/multi-agent-dev-team/kb/dependencies.json

# Validate decisions.log format
grep -E '^\d{4}-\d{2}-\d{2}:' ~/.claude/plugins/multi-agent-dev-team/kb/decisions.log
```

---

## FAQ

### Q: How do I reset everything?

**A:** Clear workspace and KB:
```bash
rm -rf ~/.claude/plugins/multi-agent-dev-team/workspace/*
rm -rf ~/.claude/plugins/multi-agent-dev-team/kb/*.md
rm ~/.claude/plugins/multi-agent-dev-team/kb/decisions.log
rm ~/.claude/plugins/multi-agent-dev-team/kb/dependencies.json
```

---

### Q: Can I disable auto-planning?

**A:** Yes, but not recommended. To disable:
```python
# In coordinator skill
USE_AUTO_PLANNING = False

# Manually specify plan in request
/dev-team "Add feature" with plan:
- Task 1: Backend Architect - Design
- Task 2: FastAPI Specialist - Implement
```

---

### Q: How do I see what specialists are doing?

**A:** Enable real-time output:
```python
# In coordinator skill
STREAM_SPECIALIST_OUTPUT = True
```

Or check logs:
```bash
tail -f ~/.claude/plugins/multi-agent-dev-team/workspace/execution.log
```

---

### Q: Can I add my own custom specialist?

**A:** Yes! See `docs/SPECIALIST_GUIDE.md` for instructions.

Basic steps:
1. Create `skills/my-specialist/skill.md`
2. Define role, capabilities, KB usage
3. Test with example request
4. Coordinator will auto-discover it

---

### Q: How do I change checkpoint strictness?

**A:** Use hints in request:
```
/dev-team "feature" (strict checkpoints)    # Pause after every task
/dev-team "feature" (normal checkpoints)    # Pause on failures
/dev-team "feature" (lenient checkpoints)   # Only critical failures
```

Or configure default:
```python
# In checkpoint_validator.py
DEFAULT_CHECKPOINT_MODE = "normal"  # strict, normal, lenient
```

---

### Q: Why is parallel execution not working?

**A:** Check:
1. Tasks have dependencies (not truly independent)
2. Concurrency limit too low
3. Specialists are blocking each other

Debug:
```bash
# Check DAG structure
cat workspace/current_plan.json | jq '.tasks[] | {id, depends_on}'

# Increase concurrency
# In parallel_executor.py
MAX_CONCURRENT_TASKS = 5
```

---

### Q: How do I handle sensitive data in KB?

**A:** Don't store sensitive data in KB. Instead:
```python
# Reference environment variables
# kb/backend-patterns.md

## API Keys
- Store in .env file
- Reference via os.getenv('API_KEY')
- Never hardcode in KB or code
```

---

### Q: Can I run multiple projects simultaneously?

**A:** Not currently. KB and workspace are shared. Workaround:
```bash
# Create project-specific directories
mkdir -p kb/project-a
mkdir -p kb/project-b

# Switch context before each request
ln -sf kb/project-a kb/active
/dev-team "work on project A"

ln -sf kb/project-b kb/active
/dev-team "work on project B"
```

---

### Q: How do I report a bug?

**A:** Provide:
1. Full error message
2. Request that triggered it
3. Workspace files (current_plan.json, task_history.json)
4. KB files (patterns, decisions)
5. System info (Python version, OS)

Submit to plugin repository with this info.

---

## Performance Optimization

### Reduce Planning Time

Auto-planning can be slow for complex features. Optimize:

```python
# In auto_planner.py

# Cache specialist responses
specialist_cache = {}

def consult_specialist(specialist, question):
    cache_key = f"{specialist}:{question}"
    if cache_key in specialist_cache:
        return specialist_cache[cache_key]

    result = _consult_specialist_impl(specialist, question)
    specialist_cache[cache_key] = result
    return result
```

---

### Reduce Checkpoint Overhead

Checkpoints add latency. Optimize:

```python
# In checkpoint_validator.py

# Skip validation for low-risk tasks
def should_validate(task):
    low_risk_specialists = ['code-reviewer', 'docker-specialist']
    return task['specialist'] not in low_risk_specialists

# Parallel validation
async def run_checkpoint(task_id, task_output, plan):
    validations = await asyncio.gather(
        validate_syntax(task_output),
        validate_structure(task_output),
        validate_imports(task_output)
    )
    return all(validations)
```

---

### Optimize KB Reads

KB files read on every task. Optimize:

```python
# In kb_manager.py

# Cache KB in memory
kb_cache = {}

def read_kb_file(filename):
    if filename in kb_cache:
        return kb_cache[filename]

    with open(f'kb/{filename}') as f:
        content = f.read()

    kb_cache[filename] = content
    return content

def invalidate_kb_cache():
    kb_cache.clear()
```

---

## Getting More Help

- **User Guide**: `docs/USER_GUIDE.md` - Getting started
- **Specialist Guide**: `docs/SPECIALIST_GUIDE.md` - Specialist details
- **Architecture**: `docs/ARCHITECTURE.md` - System internals
- **Examples**: `docs/EXAMPLES.md` - Real-world scenarios
- **Source Code**: Dive into `utils/` and `skills/` directories
- **Tests**: Review `tests/` for expected behavior
