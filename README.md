# Multi-Agent Dev Team Plugin

**Version 0.2.0-alpha** - Multi-agent coordination system with 12 domain specialists for complex development tasks.

## Overview

A multi-agent system where a central coordinator manages 12 specialized agents to complete complex development tasks. Features planning via specialist consultation, parallel execution via Claude Code's Task tool, validation checkpoints, and error recovery.

> **Note:** This is an alpha release. Core coordination logic is implemented as prompt-based instructions for Claude Code's agent system. The `utils/` Python modules provide supporting DAG parsing and KB management but are not directly executed by the plugin runtime.

## Quick Start

```bash
# Invoke the coordinator with a natural language request
/dev-team "Add user authentication to the API with JWT tokens"

# The system will:
# 1. Auto-generate an implementation plan by consulting specialists
# 2. Execute tasks in parallel (respecting dependencies)
# 3. Run multi-stage checkpoints (validation → peer review → KB sync)
# 4. Recover automatically from failures (loop-back, escalation, or abort)
```

## Core Features

- **Auto-Planning**: Natural language → DAG generation via specialist consultation
- **Parallel Execution**: Up to 3 concurrent tasks with dependency resolution
- **Advanced Checkpoints**: Multi-stage validation with peer review and KB sync
- **Error Recovery**: Automatic loop-back, escalation, or abort with state rollback
- **Shared Knowledge**: File-based KB for cross-specialist context and decisions

## 12 Specialists (+ 1 Coordinator)

**Core Coordination:**
- `/dev-team` - Orchestrates all specialists with auto-planning and parallel execution

**Backend Development:**
- `/backend-architect` - System design, service boundaries, API contracts
- `/backend-design` - Architecture patterns, service layer, caching strategies
- `/fastapi-specialist` - FastAPI routing, dependency injection, testing
- `/db-migration` - Supabase migrations, RLS policies, schema optimization
- `/openai-agents-sdk` - OpenAI Agents SDK integration, Swarm patterns

**Frontend Development:**
- `/ui-ux` - User experience, accessibility, responsive design
- `/javascript-specialist` - Modern JS, async/await, DOM manipulation
- `/matterport-sdk` - Matterport SDK integration, camera controls, tags
- `/chat-specialist` - SSE streaming, message rendering, markdown support
- `/code-quality-frontend` - ESLint, dead code removal, bundle optimization

**DevOps & Quality:**
- `/docker-specialist` - Dockerfile optimization, Docker Compose, deployment
- `/code-reviewer` - Code quality validation, complexity reduction, best practices

## Documentation

- `docs/USER_GUIDE.md` - How to use the dev-team coordinator
- `docs/SPECIALIST_GUIDE.md` - How to create new specialists
- `docs/ARCHITECTURE.md` - System design and data flow
- `CHANGELOG.md` - Version history and migration guide

## Requirements

- Python 3.10+
- PyYAML 6.0+
- jsonschema 4.17+
- pytest 7.4+ (for testing)

## License

MIT
