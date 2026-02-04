# Multi-Agent Dev Team - Architecture

## Overview

The Multi-Agent Dev Team plugin implements a coordinator-specialist pattern with advanced auto-planning, parallel execution, intelligent checkpoints, and adaptive error recovery.

**Key Principles:**
- **Single Coordinator**: One coordinator orchestrates 12 specialized agents
- **Auto-Planning**: Coordinator consults specialists to generate implementation plans
- **Parallel Execution**: Independent tasks run concurrently via DAG
- **Advanced Checkpoints**: Validation, peer review, and KB sync after each task
- **Error Recovery**: Automatic classification and recovery attempts
- **Shared Knowledge Base**: All agents sync patterns, decisions, and dependencies
- **Pre-Planning Cleanup**: Dead code removal before implementation

**Architecture Layers:**
1. **Coordination Layer**: 4-phase coordinator workflow
2. **Planning Layer**: Auto-planning with specialist consultation
3. **Execution Layer**: Parallel DAG execution engine
4. **Validation Layer**: Advanced checkpoint system
5. **Recovery Layer**: Adaptive error recovery
6. **Knowledge Layer**: Shared KB preventing drift

## Components

### 1. Coordinator Agent (4-Phase Workflow)

**Location:** `skills/dev-team/skill.md`

**Responsibilities:**
- Phase 1: Pre-planning cleanup (invoke Code Reviewer)
- Phase 2: Auto-planning (consult specialists)
- Phase 3: Parallel execution (DAG-based)
- Phase 4: Completion (summary + cleanup)

**Phase 1: Pre-Planning Cleanup**
```python
# Invoke code-reviewer for pre-planning cleanup
cleanup_result = await invoke_specialist(
    specialist='code-reviewer',
    task='Pre-planning cleanup: scan for dead/stale code'
)

# Present cleanup findings to user for approval
if cleanup_result['issues_found']:
    present_cleanup_report(cleanup_result)
    await wait_for_user_approval()
```

**Phase 2: Auto-Planning**
```python
from utils.auto_planner import auto_plan_feature

# Auto-generate plan by consulting specialists
plan = await auto_plan_feature(
    feature_description=user_input,
    user_hints=parse_user_hints(user_input)
)

# Present plan to user for approval
present_plan(plan)
user_approved = await wait_for_user_approval()
```

**Phase 3: Parallel Execution**
```python
from utils.parallel_executor import execute_plan_parallel
from utils.checkpoint_validator import run_checkpoint
from utils.error_recovery import handle_task_failure

# Execute plan with parallel orchestration
updated_plan = await execute_plan_parallel(plan)
```

**Phase 4: Completion**
```python
# Show user what was accomplished
summary = {
    'tasks_completed': count_completed_tasks(plan),
    'kb_updates': collect_kb_updates(plan),
    'workspace_files': collect_workspace_files(plan)
}

present_summary(summary)

# Offer workspace cleanup
if await ask_user("Clean up workspace files?"):
    cleanup_workspace()
```

### 2. Specialist Agents (12 Total)

**Location:** `skills/*/skill.md`

**Backend Specialists (5):**
1. **Backend Architect**: System design, architecture patterns
2. **Backend Design**: API schemas, data structures
3. **FastAPI Specialist**: Endpoints, routing, middleware
4. **Database Migration**: Schema changes, migrations
5. **OpenAI Agents SDK**: Agent creation, tool definitions

**Frontend Specialists (5):**
6. **UI/UX Specialist**: Component design, user flows
7. **JavaScript Specialist**: Core JS, async patterns
8. **Code Quality (Frontend)**: Refactoring, simplification
9. **Chat Specialist**: Chat UI, message streaming
10. **Matterport SDK**: 3D viewer integration

**Cross-Cutting (2):**
11. **Code Reviewer**: Dead code detection, pre-planning cleanup
12. **Docker Specialist**: Containerization, deployment

**Specialist Structure:**
Each specialist has:
- Role and capabilities
- Tools and technologies
- Working style
- KB usage patterns
- Coordination guidelines
- Example tasks

**Invocation:**
Specialists are invoked by the Coordinator as sub-agents with full access to:
- KB files (read/write)
- Workspace files (read/write)
- Context from previous tasks
- Peer specialist outputs

### 3. Auto-Planning Module

**Location:** `utils/auto_planner.py`

**Purpose:** Generate implementation plans by consulting specialists.

**How it works:**
1. Parse user's feature description
2. Identify domains involved (backend, frontend, etc.)
3. Consult relevant specialists for their input
4. Synthesize plan with:
   - Task breakdown
   - Dependencies (explicit + inferred)
   - Scope boundaries (what to change, what NOT to change)
   - Success criteria

**Example:**
```python
from utils.auto_planner import auto_plan_feature

plan = await auto_plan_feature(
    feature_description="Add JWT authentication",
    user_hints=["backend focus", "keep existing session system"]
)

# Returns:
# {
#   'tasks': {
#     't-001': {
#       'specialist': 'backend-architect',
#       'description': 'Design JWT auth flow',
#       'depends_on': []
#     },
#     't-002': {
#       'specialist': 'backend-design',
#       'description': 'Design auth API schemas',
#       'depends_on': ['t-001']
#     },
#     ...
#   },
#   'scope': {
#     'change': ['backend/auth/*', 'backend/main.py'],
#     'preserve': ['backend/sessions/*']
#   }
# }
```

**Specialist Consultation:**
The planner asks specialists:
- "What tasks are needed in your domain for this feature?"
- "What dependencies do you have on other domains?"
- "What should be preserved vs changed?"

This ensures plans are:
- Technically sound
- Complete (no missing steps)
- Properly scoped
- Realistically sequenced

---

### 4. Parallel Execution Engine

**Location:** `utils/parallel_executor.py`

**Purpose:** Execute tasks in parallel via DAG.

**How it works:**
1. Parse plan into Directed Acyclic Graph (DAG)
2. Identify ready tasks (no incomplete dependencies)
3. Execute up to 3 tasks concurrently
4. Wait for batch completion
5. Repeat until all tasks done

**Example:**
```python
from utils.parallel_executor import execute_plan_parallel

# Plan with dependencies:
# t-001: no deps
# t-002: depends on t-001
# t-003: depends on t-001
# t-004: depends on t-002, t-003

updated_plan = await execute_plan_parallel(plan)

# Execution:
# Batch 1: [t-001]
# Batch 2: [t-002, t-003] (parallel)
# Batch 3: [t-004]
```

**DAG Parser:**
```python
from utils.dag_parser import parse_task_list, get_ready_tasks

dag = parse_task_list(plan['tasks'])
ready_tasks = get_ready_tasks(dag)  # Tasks with no incomplete deps
```

**Concurrency Control:**
- Max 3 concurrent tasks (configurable)
- Respects dependencies automatically
- Handles task failures gracefully
- Updates DAG after each completion

---

### 5. Advanced Checkpoint System

**Location:** `utils/checkpoint_validator.py`

**Purpose:** Validate tasks with automatic checks and peer review.

**Checkpoint Phases:**
1. **Automatic Validation**: Syntax, structure, imports
2. **Peer Review**: Relevant specialists check the work
3. **KB Sync**: Patterns and decisions saved
4. **User Approval**: Optional intervention

**Example:**
```python
from utils.checkpoint_validator import run_checkpoint

checkpoint_result = await run_checkpoint(
    task_id='t-003',
    task_output=fastapi_output,
    plan=plan
)

# Returns:
# {
#   'validation': {
#     'syntax': 'pass',
#     'structure': 'pass',
#     'imports': 'pass'
#   },
#   'peer_review': {
#     'backend-design': 'Schemas implemented correctly',
#     'code-reviewer': 'Simplified error handling'
#   },
#   'kb_sync': {
#     'patterns_updated': ['backend-patterns.md'],
#     'decisions_logged': ['Used bcrypt cost factor 12']
#   },
#   'status': 'pass'
# }
```

**Validation Types:**
- **Syntax**: Check for Python/JS syntax errors
- **Structure**: Verify expected files/functions exist
- **Imports**: Check for missing dependencies
- **Style**: Ensure conventions followed

**Peer Review:**
The system invokes peer specialists to review:
- Backend Architect reviews FastAPI implementation
- Code Reviewer checks all implementations
- UI/UX reviews frontend work

---

### 6. Error Recovery System

**Location:** `utils/error_recovery.py`

**Purpose:** Classify failures and attempt automatic recovery.

**Failure Classification:**
1. **FIXABLE**: Can be resolved by clarifying with prerequisite specialist
2. **FUNDAMENTAL**: Requires user intervention or plan modification

**Recovery Process:**
```python
from utils.error_recovery import handle_task_failure

recovery_result = await handle_task_failure(
    task_id='t-003',
    error=error,
    plan=plan
)

# For FIXABLE:
# 1. Identify prerequisite task/specialist
# 2. Loop back for clarification
# 3. Update workspace with fix
# 4. Retry failed task

# For FUNDAMENTAL:
# 1. Block dependent tasks
# 2. Escalate to user with context
# 3. Wait for user guidance
# 4. Adjust plan accordingly
```

**Example Recovery:**
```
Task: FastAPI Specialist implements /auth/login
Error: "Design unclear about token storage"

Recovery:
→ Classify as FIXABLE
→ Loop back to Backend Architect
→ Get clarification: "Store tokens in Redis with TTL"
→ Update work/auth-design.md
→ Retry FastAPI task
→ Success
```

**Adaptive Strategies:**
- Fixable errors: Loop back to prerequisite (max 2 attempts)
- Fundamental errors: Escalate immediately
- Unknown errors: Treat as fundamental (safe default)

---

### 7. Knowledge Base

**Location:** `kb/`

**Files:**
- `kb/backend-patterns.md`: Backend conventions
- `kb/frontend-patterns.md`: Frontend conventions
- `kb/api-contracts.md`: API schemas and contracts
- `kb/decisions.log`: Append-only decision history
- `kb/dependencies.json`: Cross-domain dependency graph

**Purpose:**
- Prevent drift across specialist work
- Share patterns and conventions
- Track dependencies between domains
- Log technical decisions with rationale

**Schema Examples:**

```json
// project_context.json
{
  "project_name": "BlackBox",
  "tech_stack": {
    "backend": ["Python", "FastAPI", "Supabase"],
    "frontend": ["JavaScript", "esbuild"]
  },
  "current_focus": "Multi-agent refactoring",
  "constraints": ["No new dependencies without approval"]
}

// decisions.json
{
  "decisions": [
    {
      "id": "d-001",
      "decision": "Use coordinator-specialist pattern",
      "rationale": "Clearer separation of concerns",
      "date": "2026-02-03",
      "author": "Architect"
    }
  ]
}

// learnings.json
{
  "learnings": [
    {
      "id": "l-001",
      "pattern": "Checkpoint approval",
      "description": "Users want visibility at major milestones",
      "example": "Show summary and ask to continue",
      "date": "2026-02-03"
    }
  ]
}
```

### 4. Workspace

**Location:** `workspace/`

**Files:**
- `current_plan.json`: Active execution plan
- `task_history.json`: Completed tasks and outcomes
- `checkpoint_state.json`: Current checkpoint status

**Purpose:**
- Track active work
- Enable resume after interruption
- Provide audit trail
- Debug execution issues

**Schema Examples:**

```json
// current_plan.json
{
  "request": "Refactor authentication module",
  "created_at": "2026-02-03T10:00:00Z",
  "tasks": [
    {
      "id": "t-001",
      "description": "Design new auth architecture",
      "specialist": "Architect",
      "status": "completed"
    },
    {
      "id": "t-002",
      "description": "Implement JWT service",
      "specialist": "Backend",
      "status": "in_progress"
    }
  ],
  "checkpoints": [
    {
      "after_task": "t-002",
      "description": "Core implementation complete",
      "status": "pending"
    }
  ]
}

// task_history.json
{
  "tasks": [
    {
      "id": "t-001",
      "description": "Design new auth architecture",
      "specialist": "Architect",
      "status": "completed",
      "started_at": "2026-02-03T10:05:00Z",
      "completed_at": "2026-02-03T10:15:00Z",
      "outcome": "Created architecture document in docs/auth-design.md"
    }
  ]
}

// checkpoint_state.json
{
  "current_checkpoint": 1,
  "total_checkpoints": 2,
  "last_checkpoint_at": "2026-02-03T10:30:00Z",
  "user_approved": true,
  "summary": "Completed architecture design and backend implementation"
}
```

### 5. Utilities

**Location:** `utils/`

**Planned utilities:**
- `kb.js`: Knowledge base read/write operations
- `workspace.js`: Workspace file management
- `validation.js`: Plan and task validation
- `logging.js`: Structured logging

**Purpose:**
- Provide common functionality to specialists
- Ensure consistent file formats
- Handle error cases gracefully
- Enable testing and debugging

## Data Flow

### Complete Request Flow (4 Phases)

```
User: /dev-team "Add JWT authentication"
  ↓
Phase 1: Pre-Planning Cleanup
  ↓
1. Coordinator invokes Code Reviewer specialist
2. Code Reviewer scans for dead code
3. Present findings to user
4. User approves cleanup
  ↓
Phase 2: Auto-Planning
  ↓
5. Coordinator calls auto_plan_feature()
6. Auto-planner identifies domains (backend, frontend)
7. Auto-planner consults specialists:
   - Backend Architect: "Design auth flow"
   - Backend Design: "Design auth schemas"
   - FastAPI Specialist: "Implement endpoints"
   - Code Reviewer: "Review implementation"
8. Synthesize plan with dependencies
9. Present plan to user
10. User approves plan
  ↓
Phase 3: Parallel Execution
  ↓
11. parallel_executor.execute_plan_parallel(plan)
12. Loop:
    a. dag_parser.get_ready_tasks(plan)
    b. Execute batch (up to 3 concurrent):
       - Invoke specialist
       - Specialist completes task
       - Run checkpoint:
         * Automatic validation
         * Peer review
         * KB sync
         * User approval (optional)
    c. Update DAG with completions
    d. If task fails:
       * error_recovery.handle_task_failure()
       * Classify failure (FIXABLE vs FUNDAMENTAL)
       * Attempt recovery if FIXABLE
       * Escalate if FUNDAMENTAL
    e. Repeat until all tasks complete
  ↓
Phase 4: Completion
  ↓
13. Collect summary data:
    - Tasks completed
    - KB updates made
    - Workspace files created
14. Present summary to user
15. Offer workspace cleanup
16. Log session to KB
17. Done
```

### Knowledge Base Flow
```
Specialist needs information
  ↓
Read knowledge-base/project_context.json
  ↓
Use information in decision making
  ↓
Make technical decision
  ↓
Write to knowledge-base/decisions.json
  ↓
Complete task
  ↓
Discover pattern or learning
  ↓
Write to knowledge-base/learnings.json
```

### Workspace Flow
```
Coordinator creates plan
  ↓
Write workspace/current_plan.json
  ↓
Start executing task
  ↓
Update task status to in_progress
  ↓
Task completes
  ↓
Append to workspace/task_history.json
Update task status to completed
  ↓
Check if checkpoint reached
  ↓
Update workspace/checkpoint_state.json
  ↓
Get user approval
  ↓
Continue or stop based on approval
```

## Key Features Implemented

### Auto-Planning
- ✅ Specialist consultation during planning
- ✅ Automatic dependency inference
- ✅ Scope boundary detection
- ✅ User hint parsing for guidance

### Parallel Execution
- ✅ DAG-based task orchestration
- ✅ Up to 3 concurrent tasks
- ✅ Automatic dependency management
- ✅ Dynamic batch execution

### Advanced Checkpoints
- ✅ Automatic validation (syntax, structure, imports)
- ✅ Peer review by specialists
- ✅ KB sync after each task
- ✅ Optional user intervention

### Error Recovery
- ✅ Failure classification (FIXABLE vs FUNDAMENTAL)
- ✅ Automatic recovery attempts
- ✅ Loop back to prerequisite specialists
- ✅ User escalation when needed

### Knowledge Base
- ✅ Pattern files (backend, frontend, API contracts)
- ✅ Decision logging with rationale
- ✅ Dependency tracking across domains
- ✅ Automatic initialization

### Pre-Planning Cleanup
- ✅ Dead code detection
- ✅ Unused import scanning
- ✅ Deprecated pattern identification
- ✅ User approval before planning

## Future Enhancements

### Phase 2: Intelligence
- **Learning specialists**: Specialists improve from past work
- **Pattern recognition**: Auto-detect common task patterns
- **Proactive suggestions**: "I noticed X, should I also do Y?"
- **Quality metrics**: Track and report on code quality improvements

### Phase 3: Collaboration
- **Multi-user support**: Multiple users working on same project
- **Team memory**: Shared knowledge across user sessions
- **Cross-project insights**: Apply learnings from one project to another
- **Human specialist integration**: Allow human experts as specialists

### Phase 4: Ecosystem
- **Plugin marketplace**: Share custom specialists
- **Integration APIs**: Connect with external tools (Jira, GitHub, etc.)
- **Visual workflow editor**: Design custom coordination patterns
- **Analytics dashboard**: Insights into team productivity

### Phase 5: Advanced Planning
- **Multi-path planning**: Generate alternative plans
- **Cost estimation**: Predict time and effort
- **Risk analysis**: Identify high-risk tasks
- **Rollback planning**: Automatic undo strategies

## Design Decisions

### Why Coordinator-Specialist Pattern?
**Decision:** Use one coordinator with multiple specialists instead of peer-to-peer agents.

**Rationale:**
- Simpler to reason about and debug
- Clear authority and responsibility
- Easier to extend with new specialists
- Natural fit for hierarchical planning

**Trade-offs:**
- Coordinator is a single point of failure
- May be less flexible than peer-to-peer
- Coordinator complexity grows with specialists

### Why File-Based Storage?
**Decision:** Use JSON files instead of a database.

**Rationale:**
- Simpler to implement for MVP
- Easy to inspect and debug
- No external dependencies
- Version-controllable

**Trade-offs:**
- Not suitable for high concurrency
- No advanced querying
- Manual schema management
- Potential for file corruption

### Why Sequential Execution?
**Decision:** Run tasks one at a time instead of in parallel.

**Rationale:**
- Simpler coordination logic
- Easier to show progress to user
- Reduces potential for conflicts
- MVP scope management

**Trade-offs:**
- Slower overall execution
- Inefficient for independent tasks
- May frustrate users on long workflows

### Why Manual Checkpoints?
**Decision:** Require user approval at predefined checkpoints.

**Rationale:**
- Gives user control and visibility
- Prevents runaway execution
- Allows course correction
- Builds user trust

**Trade-offs:**
- Interrupts flow
- Requires user availability
- May be annoying for trusted workflows

## Testing Strategy

### Unit Tests
- Coordinator plan generation
- Specialist task execution
- Knowledge base operations
- Workspace file handling

### Integration Tests
- Full request-to-completion flow
- Checkpoint approval workflow
- Multi-specialist coordination
- Error handling and recovery

### Manual Tests
- User experience with real tasks
- Plan quality and accuracy
- Specialist assignment correctness
- Checkpoint timing and content

### Test Scenarios
1. Simple single-specialist task
2. Multi-specialist coordinated task
3. Task with checkpoint approval
4. Task with checkpoint rejection
5. Error during task execution
6. Incomplete plan handling

## Security Considerations

### File System Access
- Restrict to plugin directory
- Validate all file paths
- Sanitize user input in filenames

### Knowledge Base
- No sensitive data in knowledge base
- Clear knowledge base on request
- User control over what's stored

### Specialist Execution
- Sandboxed specialist operations
- No arbitrary code execution
- Validate specialist outputs

### User Data
- No external data transmission
- Local-only storage
- User-controlled data lifecycle

## Performance Considerations

### Coordinator Efficiency
- Minimize plan generation time
- Cache specialist capabilities
- Optimize knowledge base reads

### Specialist Efficiency
- Keep specialist prompts focused
- Avoid redundant context loading
- Stream progress updates

### Workspace Efficiency
- Batch file writes
- Lazy load task history
- Clean up completed tasks

## Extending the Architecture

### Adding a New Specialist
1. Create `specialists/your-specialist/skill.md`
2. Define role, capabilities, and coordination
3. Update Coordinator's team roster
4. Test with example tasks

### Adding a New Knowledge Type
1. Define schema for new knowledge
2. Create file in `knowledge-base/`
3. Add read/write utilities
4. Document usage for specialists

### Adding a New Workspace Feature
1. Define workspace file schema
2. Implement in `workspace/`
3. Update Coordinator to use it
4. Add to cleanup process

### Modifying Checkpoint Logic
1. Update Coordinator's checkpoint detection
2. Add new checkpoint criteria
3. Update checkpoint_state.json schema
4. Test with various workflows

## Troubleshooting

### Coordinator Issues
- Check `workspace/current_plan.json` for plan structure
- Review Coordinator skill.md for prompt issues
- Verify specialist discovery is working

### Specialist Issues
- Check specialist skill.md exists and is valid
- Verify specialist is in Coordinator's roster
- Review task assignment logic

### Knowledge Base Issues
- Validate JSON syntax in knowledge files
- Check file permissions
- Verify read/write utilities work

### Workspace Issues
- Check workspace directory exists
- Validate file formats
- Review task history for errors

## Conclusion

The Multi-Agent Dev Team plugin architecture is designed for:
- **Simplicity**: Easy to understand and extend
- **Reliability**: Robust error handling and state management
- **Extensibility**: Add new specialists and features easily
- **User Control**: Checkpoints and transparency throughout

The MVP focuses on core functionality while laying groundwork for advanced features in future phases.
