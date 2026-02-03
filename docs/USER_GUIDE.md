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
   /devteam <your request>
   ```
   Example: `/devteam refactor the authentication module to use JWT tokens`

2. **The plugin will:**
   - Analyze your request and create a plan
   - Ask you to confirm the plan
   - Execute tasks with specialized agents
   - Show checkpoints for major milestones
   - Ask for your approval at checkpoints
   - Complete the work and provide a summary

### Available Specialists

| Specialist | Purpose | Key Skills |
|------------|---------|------------|
| **Architect** | System design, code structure, patterns | Architecture design, refactoring, module organization |
| **Backend** | Server-side development | API development, database design, business logic |
| **Frontend** | UI/UX implementation | Component development, styling, user interactions |
| **QA** | Testing and quality assurance | Test writing, bug detection, validation |
| **DevOps** | Deployment and infrastructure | CI/CD, Docker, deployment scripts |

## How It Works

### 1. Planning Phase

When you invoke the plugin, the **Coordinator** agent:
- Analyzes your request
- Breaks it down into tasks
- Assigns specialists to each task
- Creates checkpoints for major milestones
- Shows you the plan for approval

**Example Plan:**
```
Task 1: Design new auth architecture [Architect]
Task 2: Implement JWT service [Backend]
Task 3: Update login UI [Frontend]
--- CHECKPOINT: Core implementation complete ---
Task 4: Add integration tests [QA]
Task 5: Update deployment config [DevOps]
```

### 2. Execution Phase

Once you approve the plan:
- Tasks are executed sequentially
- Each specialist works in their domain
- Progress is tracked in the workspace
- You can see what's happening in real-time

### 3. Checkpoints

At major milestones, the plugin:
- Pauses execution
- Shows you what's been completed
- Asks if you want to continue
- Allows you to adjust the plan if needed

**Why checkpoints?**
- Give you visibility into progress
- Allow course correction
- Ensure work meets your expectations

### 4. Completion

When all tasks are done:
- You receive a summary of changes
- All work is tracked in workspace files
- The knowledge base is updated with learnings

## Knowledge Base

The plugin maintains a knowledge base at `knowledge-base/`:

- **project_context.json**: Current state of your project
- **decisions.json**: Technical decisions made during work
- **learnings.json**: Patterns and solutions discovered

This knowledge helps specialists:
- Understand your codebase
- Make consistent decisions
- Avoid repeating mistakes
- Build on past work

**Example decisions.json:**
```json
{
  "decisions": [
    {
      "id": "d-001",
      "decision": "Use JWT for authentication",
      "rationale": "More scalable than session-based auth",
      "date": "2026-02-03",
      "author": "Backend"
    }
  ]
}
```

## Workspace Files

The plugin tracks work in `workspace/`:

- **current_plan.json**: Active plan being executed
- **task_history.json**: Completed tasks and outcomes
- **checkpoint_state.json**: Progress tracking

You can review these files to:
- See what's been done
- Understand the current state
- Debug if something goes wrong

## Tips for Best Results

### Be Specific
- ❌ "Make the app better"
- ✅ "Add error handling to the API endpoints and show user-friendly messages"

### Provide Context
- Mention relevant files or modules
- Describe the current problem
- Explain the desired outcome

### Use Checkpoints
- Review progress at checkpoints
- Ask questions if something's unclear
- Provide feedback to guide the team

### Trust the Specialists
- Each specialist knows their domain
- They'll make appropriate technical decisions
- They coordinate to ensure consistency

## Common Workflows

### Adding a New Feature
```
/devteam add user profile page with avatar upload
```
- Architect designs the feature
- Backend creates the API
- Frontend builds the UI
- QA adds tests

### Refactoring Code
```
/devteam refactor the payment module to use a service layer
```
- Architect plans the new structure
- Backend implements the refactor
- QA ensures tests still pass

### Fixing Bugs
```
/devteam fix the memory leak in the image processor
```
- QA identifies the root cause
- Backend/Frontend fixes the issue
- QA verifies the fix

### Deployment
```
/devteam set up CI/CD pipeline for the staging environment
```
- DevOps configures the pipeline
- QA adds deployment tests
- Architect reviews the setup

## Troubleshooting

### Plugin doesn't start
- Check that it's properly installed in `~/.claude/plugins/`
- Ensure `manifest.json` is valid
- Restart Claude Code

### Tasks are failing
- Review the workspace files for error details
- Check the knowledge base for conflicts
- Provide more context in your request

### Plan seems wrong
- Reject the plan and provide feedback
- Be more specific in your request
- Ask for clarification before approving

## Getting Help

- Review the **Specialist Guide** to understand capabilities
- Check the **Architecture** doc for technical details
- Report issues or suggestions to the plugin maintainer
