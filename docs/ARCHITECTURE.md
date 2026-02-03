# Multi-Agent Dev Team - Architecture

## Overview

The Multi-Agent Dev Team plugin implements a coordinator-specialist pattern where a central coordinator agent manages a team of specialized agents to complete complex development tasks.

**Key Principles:**
- **Single Coordinator**: One agent (Coordinator) manages all planning and task assignment
- **Specialized Agents**: Each specialist has a focused domain (Backend, Frontend, QA, etc.)
- **Shared Knowledge**: All agents access a common knowledge base
- **Checkpoint System**: User approval at major milestones
- **Workspace Tracking**: All work is logged and trackable

## Components

### 1. Coordinator Agent

**Location:** `specialists/coordinator/skill.md`

**Responsibilities:**
- Analyze user requests
- Create execution plans
- Assign tasks to specialists
- Track progress and state
- Handle checkpoints and user approval
- Coordinate between specialists

**Key Features:**
- Reads specialist capabilities from `specialists/` directory
- Maintains task queue and execution state
- Manages knowledge base updates
- Handles errors and retries

**Planning Process:**
```
User Request → Analyze → Break into tasks → Assign specialists → Create checkpoints → Get approval
```

### 2. Specialist Agents

**Location:** `specialists/*/skill.md`

**Active Specialists:**
- **Architect**: System design, code structure, refactoring
- **Backend**: Server-side development, APIs, databases
- **Frontend**: UI/UX, components, styling
- **QA**: Testing, validation, bug detection
- **DevOps**: Deployment, CI/CD, infrastructure

**Specialist Structure:**
Each specialist has:
- Role and capabilities
- Tools and technologies
- Working style
- Coordination guidelines
- Example tasks

**Invocation:**
Specialists are invoked by the Coordinator as tools/sub-agents to complete assigned tasks.

### 3. Knowledge Base

**Location:** `knowledge-base/`

**Files:**
- `project_context.json`: Current project state and details
- `decisions.json`: Technical decisions made during work
- `learnings.json`: Patterns and solutions discovered

**Purpose:**
- Persist understanding across conversations
- Enable specialists to make informed decisions
- Track project evolution over time
- Share knowledge between specialists

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

### Request Flow
```
User: /devteam <request>
  ↓
Plugin Entry Point (index.js)
  ↓
Coordinator Agent Invoked
  ↓
1. Load knowledge base
2. Analyze request
3. Create plan with tasks and checkpoints
4. Show plan to user
  ↓
User Approves Plan
  ↓
5. For each task:
   a. Update workspace (task status = in_progress)
   b. Invoke specialist agent as tool
   c. Specialist executes task
   d. Update workspace (task status = completed)
   e. Log to task_history.json
   f. Check for checkpoint
  ↓
6. If checkpoint:
   a. Pause execution
   b. Show progress summary
   c. Ask user to approve continuation
   d. If approved, continue; else stop
  ↓
7. All tasks complete:
   a. Update knowledge base with learnings
   b. Show completion summary
   c. Clean up workspace
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

## MVP Limitations

### Current Scope (MVP)
- **5 specialists**: Architect, Backend, Frontend, QA, DevOps
- **Sequential execution**: Tasks run one at a time
- **File-based storage**: JSON files in workspace and knowledge base
- **Manual checkpoints**: Defined in plan, user approval required
- **Single user**: No multi-user coordination

### What's NOT in MVP
- ❌ Parallel task execution
- ❌ Dynamic specialist creation
- ❌ Advanced conflict resolution
- ❌ Persistent database storage
- ❌ Multi-project support
- ❌ Progress visualization UI
- ❌ Automatic rollback on errors
- ❌ Specialist learning/improvement

### Known Limitations
1. **No state persistence across Claude restarts**: Workspace is in-memory unless explicitly saved
2. **Limited error handling**: Failures may require manual intervention
3. **No task dependencies**: Coordinator must sequence tasks correctly
4. **Fixed checkpoint logic**: Cannot dynamically adjust checkpoints
5. **No resource estimation**: No time/complexity predictions

## Future Enhancements

### Phase 2: Enhanced Execution
- **Parallel tasks**: Run independent tasks simultaneously
- **Task dependencies**: Define explicit dependencies between tasks
- **Smart checkpoints**: Automatically insert checkpoints based on complexity
- **Error recovery**: Automatic retry with different approaches
- **Progress estimation**: Predict time and effort for tasks

### Phase 3: Intelligence
- **Learning specialists**: Specialists improve from past work
- **Pattern recognition**: Auto-detect common task patterns
- **Proactive suggestions**: "I noticed X, should I also do Y?"
- **Quality metrics**: Track and report on code quality improvements

### Phase 4: Collaboration
- **Multi-user support**: Multiple users working on same project
- **Team memory**: Shared knowledge across user sessions
- **Cross-project insights**: Apply learnings from one project to another
- **Human specialist integration**: Allow human experts as specialists

### Phase 5: Ecosystem
- **Plugin marketplace**: Share custom specialists
- **Integration APIs**: Connect with external tools (Jira, GitHub, etc.)
- **Visual workflow editor**: Design custom coordination patterns
- **Analytics dashboard**: Insights into team productivity

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
