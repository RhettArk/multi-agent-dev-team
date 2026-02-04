# Multi-Agent Dev Team - User Guide

## Quick Start

### Installation

The Multi-Agent Dev Team plugin is installed in your Claude Code plugins directory:
```
~/.claude/plugins/multi-agent-dev-team/
```

### Basic Usage

1. **Invoke the plugin:**
   ```
   /dev-team <your request>
   ```
   Example: `/dev-team add user authentication with JWT`

2. **The plugin will:**
   - Run pre-planning cleanup (scan for dead code)
   - Auto-generate an implementation plan
   - Ask you to confirm the plan
   - Execute tasks in parallel where possible
   - Run advanced checkpoints with validation
   - Handle errors automatically when possible
   - Complete the work and provide a summary

### Available Specialists (12 Total)

**Backend Specialists:**
- **Backend Architect**: System design, architecture patterns, multi-agent coordination
- **Backend Design**: API schemas, data structures, contract design
- **FastAPI Specialist**: FastAPI endpoints, routing, middleware
- **Database Migration**: Schema changes, migrations, data integrity
- **OpenAI Agents SDK**: Agent creation, tool definitions, streaming

**Frontend Specialists:**
- **UI/UX Specialist**: Component design, user flows, accessibility
- **JavaScript Specialist**: Core JavaScript, async patterns, module organization
- **Code Quality (Frontend)**: Refactoring, simplification, best practices
- **Chat Specialist**: Chat UI, message streaming, real-time features
- **Matterport SDK**: 3D viewer integration, camera positioning, scene interaction

**Cross-Cutting Specialists:**
- **Code Reviewer**: Dead code detection, simplification, anti-pattern identification
- **Docker Specialist**: Containerization, environment config, deployment

## How It Works (4-Phase Architecture)

### Phase 1: Pre-Planning Cleanup

Before creating a plan, the **Code Reviewer** specialist:
- Scans your codebase for dead/stale code
- Finds unused imports, functions, classes
- Identifies deprecated patterns
- Presents findings for your approval

**Why cleanup first?**
- Ensures specialists work with clean code
- Prevents building on deprecated patterns
- Reduces cognitive load during implementation
- Makes code review easier

**Example:**
```
Code Reviewer found:
- 3 unused imports in auth.py
- 1 deprecated function in utils.py
- 2 dead code paths in handlers.py

[Approve cleanup?]
```

### Phase 2: Auto-Planning

The **Coordinator** generates a plan by:
1. Analyzing your feature description
2. Consulting relevant specialists for input
3. Synthesizing a comprehensive plan with:
   - Task breakdown
   - Dependencies (explicit + inferred)
   - Scope boundaries (what to change, what NOT to change)
   - Success criteria
4. Presenting the plan for your approval

**Example Auto-Generated Plan:**
```
Task 1: Design auth flow [Backend Architect]
Task 2: Design API schemas [Backend Design]
Task 3: Implement /auth/login [FastAPI Specialist]
  → Depends on: Task 1, Task 2
Task 4: Review and simplify [Code Reviewer]
  → Depends on: Task 3
Task 5: Update container config [Docker Specialist]
  → Depends on: Task 4

[Approve plan?]
```

### Phase 3: Parallel Execution

Tasks are executed via a Directed Acyclic Graph (DAG):
- **Parallel tasks**: Independent tasks run concurrently (up to 3 at once)
- **Sequential tasks**: Dependent tasks wait for prerequisites
- **Advanced checkpoints**: Run after each task with:
  - Automatic validation (syntax, structure)
  - Peer review by specialists
  - KB sync (patterns, decisions, dependencies)
  - Final approval option

**Parallel Execution Example:**
```
✓ Task 1 completed [Backend Architect]
↓
Tasks 2 & 3 running in parallel...
  ✓ Task 2 completed [Backend Design]
  ✓ Task 3 completed [FastAPI Specialist]
↓
✓ Task 4 completed [Code Reviewer]
↓
✓ Task 5 completed [Docker Specialist]
```

**Checkpoint Validation:**
After each task, the system:
- Validates syntax and structure
- Invokes peer specialists for review
- Syncs knowledge to KB
- Gives you the option to intervene

### Phase 4: Completion

When all tasks finish:
- Comprehensive summary of changes
- KB updates (patterns, decisions, dependencies)
- Workspace files created
- Optional workspace cleanup
- Session logged to KB

## Knowledge Base Structure

The plugin maintains a shared knowledge base at `kb/` to prevent drift across specialist work:

**Pattern Files:**
- `kb/backend-patterns.md` - Backend conventions and patterns
- `kb/frontend-patterns.md` - Frontend conventions and patterns
- `kb/api-contracts.md` - API schemas and contracts

**Tracking Files:**
- `kb/decisions.log` - Append-only decision history
- `kb/dependencies.json` - Cross-domain dependency graph

### How Specialists Use KB

**Before work (pre-flight):**
- Read relevant pattern files
- Check decision log for precedent
- Verify dependencies won't conflict

**During work (monitoring):**
- Reference patterns for consistency
- Update patterns if establishing new conventions
- Log decisions with rationale

**After work (validation):**
- Sync patterns to KB
- Log decisions with rationale
- Update dependencies if contracts changed

**Example KB Usage:**

```
FastAPI Specialist starts Task 3:
1. Reads kb/backend-patterns.md
   → Sees: "All endpoints use snake_case"
2. Reads kb/api-contracts.md
   → Sees: "Auth endpoints return {token, expires_at}"
3. Implements /auth/login following conventions
4. Updates kb/decisions.log:
   "Used bcrypt for password hashing (industry standard)"
5. Updates kb/dependencies.json:
   "/auth/login → frontend/auth.js (new dependency)"
```

### KB Management

**Initialization:**
The KB is automatically initialized on first use with:
- Empty pattern files with templates
- Empty decision log
- Empty dependency graph

**Cleanup:**
You can reset the KB at any time to start fresh. Useful when:
- Switching projects
- Major refactoring complete
- Patterns have evolved significantly

## Advanced Features

### Auto-Planning

The Coordinator consults specialists during planning to:
- Determine the correct task breakdown
- Identify dependencies automatically
- Set appropriate scope boundaries
- Define success criteria

**No more manual task lists!** The plugin figures out what needs to be done.

### Parallel Execution

The system uses a DAG (Directed Acyclic Graph) to:
- Identify independent tasks
- Run up to 3 tasks concurrently
- Respect dependencies automatically
- Maximize throughput

**Example:**
```
Sequential execution: 5 tasks × 5 min = 25 min
Parallel execution: 3 parallel batches = ~12 min
```

### Advanced Checkpoints

Every task completion triggers:
1. **Automatic validation**: Syntax, structure, imports
2. **Peer review**: Relevant specialists check the work
3. **KB sync**: Patterns and decisions saved
4. **User approval**: Optional intervention point

**You control checkpoint strictness:**
- Strict: Pause after every task
- Normal: Pause only on validation failures
- Lenient: Only pause on critical issues

### Error Recovery

When a task fails, the system:
1. **Classifies the failure**:
   - Fixable: Loop back to prerequisite specialist
   - Fundamental: Block dependents, escalate to user

2. **Attempts recovery**:
   - Get clarification from prerequisite specialist
   - Update workspace with fix
   - Retry failed task

3. **Escalates if needed**:
   - Present issue to user
   - Ask for guidance
   - Adjust plan accordingly

**Example Recovery:**
```
Task 3 fails: "Design unclear about token storage"
→ Classified as FIXABLE
→ Loop back to Task 1 (Backend Architect)
→ Get clarification: "Store tokens in Redis with TTL"
→ Update work/auth-design.md
→ Retry Task 3
→ Task 3 succeeds
→ Continue execution
```

## Tips for Best Results

### Be Specific
- ❌ "Make the app better"
- ✅ "Add error handling to the API endpoints with user-friendly messages"

### Provide Context
- Mention relevant files or modules
- Describe the current problem
- Explain the desired outcome
- Note any constraints (e.g., "don't change the database schema")

### Use User Hints in Requests
You can guide auto-planning with hints:
```
/dev-team "Add JWT auth"
  → Auto-plans with backend specialists

/dev-team "Add JWT auth (also update frontend)"
  → Auto-plans with backend + frontend specialists

/dev-team "Add JWT auth (keep existing session system)"
  → Auto-plans with constraint to preserve sessions
```

### Trust the Auto-Planner
- The Coordinator consults specialists during planning
- Dependencies are inferred automatically
- Scope boundaries are set intelligently
- You can always modify the plan before approval

### Review Plans Before Approving
- Check that all relevant specialists are included
- Verify dependencies make sense
- Ensure scope aligns with your intentions
- Add constraints if needed

### Use Checkpoints Wisely
- Strict mode: Best for critical changes
- Normal mode: Good for most work
- Lenient mode: Fast iteration on non-critical features

### Let Error Recovery Work
- The system can fix many issues automatically
- Only intervene when escalated
- Provide clear guidance when asked

## Common Workflows

### Adding a New Feature
```
/dev-team add user profile page with avatar upload
```

**What happens:**
1. Pre-cleanup: Code Reviewer scans for dead code
2. Auto-planning:
   - Backend Architect: Design profile data model
   - Backend Design: Design profile API schemas
   - FastAPI Specialist: Implement profile endpoints
   - UI/UX Specialist: Design profile page layout
   - JavaScript Specialist: Implement profile UI
   - Docker Specialist: Update env config for uploads
3. Parallel execution: Backend tasks run first, then frontend
4. Checkpoints validate each step
5. Complete with summary

### Refactoring Code
```
/dev-team refactor auth module to use service layer
```

**What happens:**
1. Pre-cleanup: Remove old auth patterns
2. Auto-planning:
   - Backend Architect: Design service layer pattern
   - Code Quality (Frontend): Refactor auth UI calls
   - Code Reviewer: Simplify and review changes
3. Execution with error recovery if refactor breaks tests
4. KB updated with new patterns

### Fixing Bugs
```
/dev-team fix the session timeout bug in auth flow
```

**What happens:**
1. Code Reviewer identifies root cause
2. Auto-planning:
   - FastAPI Specialist: Fix session handling
   - Code Reviewer: Verify fix doesn't introduce new issues
3. Fast execution (small scope)
4. Checkpoint validates fix

### Deployment Setup
```
/dev-team containerize the app for production
```

**What happens:**
1. Docker Specialist creates Dockerfile
2. Backend specialists review env config
3. FastAPI Specialist updates for containerization
4. Parallel execution where possible
5. Complete with deployment instructions

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for detailed troubleshooting guide.

**Quick fixes:**

### Auto-planning chose wrong specialists
- Reject the plan
- Add hints to your request: "(focus on backend)"
- Be more specific about the scope

### Parallel execution causing conflicts
- The system should prevent this via dependencies
- If it happens, report as a bug
- Manually specify task order in plan approval

### Error recovery not working
- Check if failure classification is correct
- Provide additional context when escalated
- Use strict checkpoint mode for better visibility

### KB becoming stale
- Reset KB when switching projects
- Manually review and update pattern files
- Run cleanup periodically

## Getting Help

- **User Guide**: This document (getting started)
- **Specialist Guide**: `docs/SPECIALIST_GUIDE.md` (specialist capabilities)
- **Architecture**: `docs/ARCHITECTURE.md` (system internals)
- **Troubleshooting**: `docs/TROUBLESHOOTING.md` (common issues)
- **Examples**: `docs/EXAMPLES.md` (real-world scenarios)
