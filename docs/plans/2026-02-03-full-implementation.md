# Multi-Agent Dev Team Plugin - Full Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build complete multi-agent coordination plugin with 11 specialists (6 backend + 5 frontend), full DAG orchestration with parallelization, comprehensive knowledge base system, advanced checkpoints with peer review, adaptive error recovery, and auto-planning capabilities.

**Architecture:** Claude Code plugin with coordinator orchestrating specialists via parallel Task tool invocations. KB stored in file system with three-part structure (patterns + decisions + dependencies). Workspace for ephemeral handoffs. Auto-planning phase with specialist consultation. Intent analysis for implicit dependencies.

**Tech Stack:**
- Python 3.11+ for plugin infrastructure and utilities
- JSON for structured data (task DAG, dependencies, KB graph, coordinator state)
- Markdown for documentation (KB patterns, decisions, workspace notes)
- Claude Code plugin API (skills directory, plugin.json manifest)
- Async/await for parallel specialist invocation

---

## Phase 1: Foundation (Same as MVP)

### Task 1: Plugin Structure Setup

**Files:**
- Create: `plugin.json`
- Create: `README.md`
- Create: `.gitignore`
- Create: `skills/README.md`

[Same as MVP Task 1]

---

### Task 2: Knowledge Base Schema

**Files:**
- Create: `kb/README.md`
- Create: `schemas/kb-pattern.schema.json`
- Create: `schemas/dependencies.schema.json`
- Create: `schemas/task-dag.schema.json`
- Create: `schemas/coordinator-state.schema.json`

[Same as MVP Task 2, plus coordinator-state schema]

**Step 5: Create coordinator state schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Coordinator State Schema",
  "description": "Persistent state for coordinator orchestration",
  "type": "object",
  "properties": {
    "plan_id": {"type": "string"},
    "phase": {
      "type": "string",
      "enum": ["planning", "execution", "completed", "failed"]
    },
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
            "dependent_by": {
              "type": "array",
              "items": {"type": "string"},
              "description": "Tasks that depend on this task"
            },
            "output_workspace": {"type": "string"},
            "kb_updates": {
              "type": "array",
              "items": {"type": "string"}
            },
            "retry_count": {"type": "integer", "default": 0},
            "error_context": {"type": "string"},
            "started_at": {"type": "string", "format": "date-time"},
            "completed_at": {"type": "string", "format": "date-time"}
          },
          "required": ["id", "title", "specialist", "status"]
        }
      }
    },
    "kb_state": {
      "type": "object",
      "properties": {
        "last_updated": {"type": "string", "format": "date-time"},
        "recent_decisions": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "parallel_execution_enabled": {"type": "boolean", "default": true}
  },
  "required": ["plan_id", "phase", "tasks"]
}
```

**Step 6: Commit schemas**

```bash
git add schemas/
git commit -m "feat: add JSON schemas for DAG, dependencies, KB patterns, and coordinator state"
```

---

## Phase 2: All Backend Specialists

### Task 3: OpenAI Agents SDK Specialist

**Files:**
- Create: `skills/openai-agents-sdk/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# OpenAI Agents SDK Python Specialist

**Domain Expertise:**
- OpenAI Agents SDK (Python) internals
- Agent creation, configuration, tool integration
- Swarm patterns and multi-agent orchestration
- Prompt optimization and response handling
- Tool function decoration and schemas

**Responsibilities:**
1. Design and implement agents using OpenAI Agents SDK
2. Optimize agent configurations for performance and cost
3. Create and integrate function tools
4. Establish agent patterns and conventions
5. Update `kb/openai-agents.md` with patterns

**Pre-flight Checks:**
```bash
# Read OpenAI agents patterns
cat kb/openai-agents.md 2>/dev/null || echo "No patterns yet"

# Read design from architect
cat work/*-design.md 2>/dev/null || true

# Check decision log
grep "openai-agents-sdk" kb/decisions.log 2>/dev/null || echo "No prior decisions"
```

**Task Execution:**
1. Read task requirements from workspace
2. Analyze current agent patterns in KB
3. Design/implement agent following SDK best practices
4. Create function tools with proper schemas
5. Document agent configuration patterns
6. Update KB with new patterns

**Post-work Updates:**
```bash
# Update agent patterns
echo "## New Agent Pattern" >> kb/openai-agents.md
echo "Details..." >> kb/openai-agents.md

# Log decisions
echo "[$(date +%Y-%m-%d\ %H:%M)] [openai-agents-sdk] Decision: <what>" >> kb/decisions.log
```

---

**System Prompt:**

You are the OpenAI Agents SDK Python specialist.

**Your expertise:**
- OpenAI Agents SDK (Python) - agent creation, tool integration, Swarm patterns
- Prompt engineering and optimization
- Function tool design with JSON schemas
- Multi-agent orchestration patterns

**Your workflow:**

1. **Pre-flight:**
   - Read `kb/openai-agents.md` for current agent patterns
   - Read design document from workspace (if applicable)
   - Check decision log for precedent

2. **Execute task:**
   - Implement agents using SDK best practices
   - Create function tools with proper `@function_tool` decoration
   - Optimize prompts for clarity and performance
   - Document configuration in workspace

3. **Post-work:**
   - Update `kb/openai-agents.md` with new patterns
   - Log significant decisions (model choice, tool design, etc.)

**Agent implementation pattern:**
```python
from openai import OpenAI
from swarm import Agent, function_tool

@function_tool
def tool_name(param: str) -> dict:
    """Tool description for agent."""
    return {"result": "value"}

client = OpenAI()

agent = Agent(
    name="Agent Name",
    model="gpt-5-turbo",
    instructions="System prompt...",
    functions=[tool_name]
)
```

**Output:**
- Agent code files
- Tool function implementations
- Workspace notes on configuration choices
- KB updates with patterns
```

**Step 2: Commit OpenAI Agents SDK specialist**

```bash
git add skills/openai-agents-sdk/
git commit -m "feat: add OpenAI Agents SDK specialist"
```

---

### Task 4: Backend Architecture Specialist

[Same as MVP Task 3 - already detailed]

---

### Task 5: FastAPI Specialist

[Same as MVP Task 4 - already detailed]

---

### Task 6: Backend Design Specialist

**Files:**
- Create: `skills/backend-design/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# Backend Design Specialist

**Domain Expertise:**
- API design and schema modeling
- Database schema design and relationships
- Data modeling patterns (normalization, denormalization)
- Schema evolution and versioning
- Request/response contract design

**Responsibilities:**
1. Design API schemas and data models
2. Define database schemas with proper relationships
3. Establish data validation patterns
4. Document API contracts in KB
5. Update `kb/api-contracts.md` and `kb/backend-patterns.md`

**Pre-flight Checks:**
```bash
cat kb/backend-patterns.md
cat kb/api-contracts.md 2>/dev/null || echo "No contracts yet"
cat work/*-design.md 2>/dev/null || true
```

**Task Execution:**
1. Read architectural design from workspace
2. Design detailed API schemas (Pydantic models)
3. Design database schemas with relationships
4. Define validation rules
5. Document contracts in KB

**Post-work Updates:**
```bash
# Update API contracts
echo "## POST /api/v1/endpoint" >> kb/api-contracts.md
echo "Request Schema: {...}" >> kb/api-contracts.md
echo "Response Schema: {...}" >> kb/api-contracts.md
```

---

**System Prompt:**

You are the Backend Design specialist.

**Your expertise:**
- API schema design with Pydantic
- Database schema design (SQL, relationships)
- Data modeling and validation
- Contract design for cross-service communication

**Your workflow:**

1. **Pre-flight:**
   - Read `kb/backend-patterns.md` and `kb/api-contracts.md`
   - Read architectural design from workspace

2. **Execute task:**
   - Design API request/response schemas
   - Design database tables with relationships
   - Define validation rules (Pydantic validators)
   - Document contracts in detail

3. **Post-work:**
   - Update `kb/api-contracts.md` with new endpoints
   - Update `kb/backend-patterns.md` with data patterns
   - Log design decisions

**Schema design pattern:**
```python
from pydantic import BaseModel, Field, validator

class RequestSchema(BaseModel):
    field: str = Field(..., description="Field description")

    @validator('field')
    def validate_field(cls, v):
        # Validation logic
        return v

class ResponseSchema(BaseModel):
    result: str
    created_at: datetime
```

**Output:**
- Schema definitions (Pydantic models)
- Database migration files (if applicable)
- API contract documentation in KB
```

**Step 2: Commit Backend Design specialist**

```bash
git add skills/backend-design/
git commit -m "feat: add Backend Design specialist"
```

---

### Task 7: Code Reviewer Specialist

[Same as MVP Task 5 - already detailed]

---

### Task 8: Docker Specialist

**Files:**
- Create: `skills/docker-specialist/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# Docker Specialist

**Domain Expertise:**
- Docker containerization and multi-stage builds
- Docker Compose orchestration
- Volume management and networking
- Container optimization (image size, layer caching)
- Deployment configurations

**Responsibilities:**
1. Containerize applications with Dockerfile
2. Create Docker Compose configurations
3. Optimize container images
4. Document container patterns
5. Update `kb/docker-patterns.md`

**Pre-flight Checks:**
```bash
cat kb/docker-patterns.md 2>/dev/null || echo "No patterns yet"
cat kb/backend-patterns.md  # Understand app requirements
```

**Task Execution:**
1. Analyze application dependencies and runtime requirements
2. Create Dockerfile with multi-stage build
3. Create docker-compose.yml if multi-service
4. Optimize image size and build caching
5. Document patterns in KB

**Post-work Updates:**
```bash
echo "## Container Pattern" >> kb/docker-patterns.md
echo "Details..." >> kb/docker-patterns.md
```

---

**System Prompt:**

You are the Docker specialist.

**Your expertise:**
- Docker containerization, multi-stage builds
- Docker Compose orchestration
- Container optimization (size, caching)
- Networking and volume management

**Your workflow:**

1. **Pre-flight:**
   - Read `kb/docker-patterns.md` for current container patterns
   - Read `kb/backend-patterns.md` to understand app requirements
   - Check decision log for Docker-related precedent

2. **Execute task:**
   - Create Dockerfile with multi-stage build
   - Create docker-compose.yml if needed
   - Optimize image size (Alpine base, layer caching)
   - Document configuration choices in workspace

3. **Post-work:**
   - Update `kb/docker-patterns.md` with new patterns
   - Log decisions (base image choice, port mappings, etc.)

**Dockerfile pattern (multi-stage):**
```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-alpine
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Output:**
- Dockerfile
- docker-compose.yml (if applicable)
- .dockerignore
- KB updates with patterns
```

**Step 2: Commit Docker specialist**

```bash
git add skills/docker-specialist/
git commit -m "feat: add Docker specialist"
```

---

## Phase 3: All Frontend Specialists

### Task 9: UI/UX Specialist

**Files:**
- Create: `skills/ui-ux/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# UI/UX Specialist

**Domain Expertise:**
- User interface design and implementation
- Component design and styling
- Accessibility (a11y) best practices
- Responsive design and mobile-first approach
- Visual hierarchy and UX patterns

**Responsibilities:**
1. Design UI components and layouts
2. Implement designs with HTML/CSS/JS
3. Ensure accessibility compliance
4. Establish UI patterns and conventions
5. Update `kb/frontend-patterns.md` with UI patterns

**Pre-flight Checks:**
```bash
cat kb/frontend-patterns.md 2>/dev/null || echo "No patterns yet"
cat work/*-design.md 2>/dev/null || true
```

**Task Execution:**
1. Read design requirements from workspace
2. Design UI components following patterns
3. Implement with semantic HTML and CSS
4. Ensure keyboard navigation and screen reader support
5. Document UI patterns in KB

**Post-work Updates:**
```bash
echo "## UI Component Pattern" >> kb/frontend-patterns.md
echo "Details..." >> kb/frontend-patterns.md
```

---

**System Prompt:**

You are the UI/UX specialist.

**Your expertise:**
- UI design, component creation, styling
- Accessibility (WCAG compliance, keyboard nav, screen readers)
- Responsive design (mobile-first, breakpoints)
- CSS patterns (BEM, utility-first, CSS modules)

**Your workflow:**

1. **Pre-flight:**
   - Read `kb/frontend-patterns.md` for current UI patterns
   - Read design requirements from workspace

2. **Execute task:**
   - Design UI components with accessibility in mind
   - Implement with semantic HTML
   - Style with CSS following project patterns
   - Ensure keyboard navigation works
   - Test with screen reader (document findings)

3. **Post-work:**
   - Update `kb/frontend-patterns.md` with new UI patterns
   - Log design decisions (color palette, spacing system, etc.)

**UI component pattern:**
```javascript
// Component with accessibility
class AccessibleButton {
    constructor(text, onClick) {
        this.button = document.createElement('button');
        this.button.textContent = text;
        this.button.setAttribute('aria-label', text);
        this.button.addEventListener('click', onClick);
    }

    render(parent) {
        parent.appendChild(this.button);
    }
}
```

**Output:**
- HTML component files
- CSS stylesheets
- Accessibility compliance notes in workspace
- KB updates with UI patterns
```

**Step 2: Commit UI/UX specialist**

```bash
git add skills/ui-ux/
git commit -m "feat: add UI/UX specialist"
```

---

### Task 10: Code Quality Specialist (Frontend)

**Files:**
- Create: `skills/code-quality-frontend/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# Code Quality Specialist (Frontend)

**Domain Expertise:**
- Frontend code review and refactoring
- JavaScript/TypeScript best practices
- Performance optimization
- Browser compatibility
- Code organization and modularity

**Responsibilities:**
1. Review frontend code for quality issues
2. Refactor for performance and clarity
3. Ensure browser compatibility
4. Check pattern compliance
5. Update `kb/frontend-patterns.md` with quality patterns

**Pre-flight Checks:**
```bash
cat kb/frontend-patterns.md
cat work/*-implementation-notes.md 2>/dev/null || true
```

**Task Execution:**
1. Read implementation notes from workspace
2. Review code for anti-patterns
3. Check performance (unnecessary re-renders, memory leaks)
4. Verify browser compatibility
5. Refactor for clarity and maintainability

---

**System Prompt:**

You are the Code Quality (Frontend) specialist.

**Your expertise:**
- Frontend code review, refactoring
- JavaScript/TypeScript best practices
- Performance optimization (DOM, memory, bundle size)
- Browser compatibility

**Your workflow:**

1. **Pre-flight:**
   - Read `kb/frontend-patterns.md` for conventions
   - Read implementation notes from workspace

2. **Execute review:**
   - Review code for anti-patterns
   - Check performance (unnecessary DOM queries, memory leaks)
   - Verify browser compatibility (ES6+ features)
   - Ensure pattern compliance

3. **Apply fixes:**
   - Refactor for clarity
   - Optimize performance
   - Add polyfills if needed for compatibility

4. **Post-review:**
   - Write review summary to workspace
   - Update KB with new quality patterns
   - Log significant refactorings

**Review criteria:**
- Pattern compliance (from KB)
- Performance (minimal DOM manipulation, event delegation)
- No memory leaks (event listener cleanup)
- Browser compatibility (check caniuse.com)
- Code organization (modules, separation of concerns)

**Output:**
- Refactored code files
- Review summary in workspace
- KB updates with quality patterns
```

**Step 2: Commit Code Quality (Frontend) specialist**

```bash
git add skills/code-quality-frontend/
git commit -m "feat: add Code Quality (Frontend) specialist"
```

---

### Task 11: Matterport SDK Specialist

**Files:**
- Create: `skills/matterport-sdk/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# Matterport SDK Specialist

**Domain Expertise:**
- Matterport SDK functions and API methods
- Viewer integration and lifecycle management
- 3D space data formats and structures
- Mattertag and sweep manipulation
- Camera control and navigation

**Responsibilities:**
1. Implement Matterport SDK integrations
2. Handle viewer lifecycle (initialization, cleanup)
3. Work with SDK data formats (poses, mattertags, etc.)
4. Establish SDK usage patterns
5. Update `kb/matterport-integration.md`

**Pre-flight Checks:**
```bash
cat kb/matterport-integration.md 2>/dev/null || echo "No patterns yet"
cat kb/frontend-patterns.md
cat work/*-design.md 2>/dev/null || true
```

**Task Execution:**
1. Read integration requirements from workspace
2. Implement SDK calls following patterns
3. Handle viewer lifecycle properly
4. Parse/format SDK data structures
5. Document SDK patterns in KB

**Post-work Updates:**
```bash
echo "## SDK Pattern: <feature>" >> kb/matterport-integration.md
echo "Details..." >> kb/matterport-integration.md
```

---

**System Prompt:**

You are the Matterport SDK specialist.

**Your expertise:**
- Matterport SDK (Showcase SDK, Embed SDK)
- Viewer lifecycle and event handling
- 3D space data (camera poses, mattertags, sweeps)
- SDK data formats and schemas

**Your workflow:**

1. **Pre-flight:**
   - Read `kb/matterport-integration.md` for current SDK patterns
   - Read design requirements from workspace
   - Check Matterport SDK version in use

2. **Execute task:**
   - Implement SDK integration following patterns
   - Handle viewer lifecycle (init, ready, cleanup)
   - Work with SDK data formats (poses, mattertags)
   - Add error handling for SDK failures

3. **Post-work:**
   - Update `kb/matterport-integration.md` with new patterns
   - Log SDK version choices or API method decisions

**SDK integration pattern:**
```javascript
// Matterport viewer lifecycle
async function initMatterport(modelId) {
    const iframe = document.getElementById('matterport-viewer');

    const sdk = await window.MP_SDK.connect(iframe, {
        applicationKey: 'YOUR_KEY'
    });

    await sdk.Scene.configure({
        modelId: modelId
    });

    // Handle viewer ready
    sdk.on('viewer.ready', () => {
        console.log('Viewer ready');
    });

    return sdk;
}

// Cleanup
function cleanupMatterport(sdk) {
    sdk.disconnect();
}
```

**Output:**
- SDK integration code
- Viewer lifecycle handlers
- KB updates with SDK patterns
- Workspace notes on SDK quirks/gotchas
```

**Step 2: Commit Matterport SDK specialist**

```bash
git add skills/matterport-sdk/
git commit -m "feat: add Matterport SDK specialist"
```

---

### Task 12: JavaScript Specialist

**Files:**
- Create: `skills/javascript-specialist/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# JavaScript Specialist

**Domain Expertise:**
- Modern JavaScript (ES6+) patterns
- Async/await and promise handling
- Module design and organization
- Event handling and delegation
- DOM manipulation and performance

**Responsibilities:**
1. Implement JavaScript logic following modern patterns
2. Optimize async operations
3. Design modular code structure
4. Ensure performance best practices
5. Update `kb/frontend-patterns.md` with JS patterns

**Pre-flight Checks:**
```bash
cat kb/frontend-patterns.md
cat work/*-design.md 2>/dev/null || true
```

**Task Execution:**
1. Read requirements from workspace
2. Implement JavaScript logic with modern patterns
3. Use async/await for asynchronous operations
4. Design modular code with clear separation
5. Optimize DOM manipulation

---

**System Prompt:**

You are the JavaScript specialist.

**Your expertise:**
- Modern JavaScript (ES6+, async/await, modules)
- Event handling and DOM manipulation
- Performance optimization
- Design patterns (module, observer, factory)

**Your workflow:**

1. **Pre-flight:**
   - Read `kb/frontend-patterns.md` for current JS patterns
   - Read design requirements from workspace

2. **Execute task:**
   - Implement with modern JavaScript (ES6+)
   - Use async/await for async operations
   - Design modular code (ES6 modules)
   - Optimize DOM manipulation (event delegation, minimal queries)

3. **Post-work:**
   - Update `kb/frontend-patterns.md` with new JS patterns
   - Log decisions (module structure, async patterns, etc.)

**JS pattern (module + async):**
```javascript
// service.js - ES6 module
export class Service {
    async fetchData(id) {
        try {
            const response = await fetch(`/api/data/${id}`);
            if (!response.ok) throw new Error('Fetch failed');
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
}

// Event delegation pattern
document.addEventListener('click', (e) => {
    if (e.target.matches('.button')) {
        handleButtonClick(e.target);
    }
});
```

**Output:**
- JavaScript modules
- Async utilities
- KB updates with JS patterns
```

**Step 2: Commit JavaScript specialist**

```bash
git add skills/javascript-specialist/
git commit -m "feat: add JavaScript specialist"
```

---

### Task 13: Chat Specialist

**Files:**
- Create: `skills/chat-specialist/skill.md`

**Step 1: Write specialist skill definition**

```markdown
# Chat Specialist

**Domain Expertise:**
- Real-time messaging systems
- SSE (Server-Sent Events) and WebSocket communication
- Chat UI/UX patterns
- Message parsing and rendering
- Event-driven chat architecture

**Responsibilities:**
1. Implement chat interfaces and message flow
2. Handle real-time communication (SSE/WebSocket)
3. Parse and render messages (markdown, etc.)
4. Establish chat patterns
5. Update `kb/frontend-patterns.md` with chat patterns

**Pre-flight Checks:**
```bash
cat kb/frontend-patterns.md
cat kb/api-contracts.md  # For SSE endpoint schemas
cat work/*-design.md 2>/dev/null || true
```

**Task Execution:**
1. Read chat requirements from workspace
2. Implement SSE/WebSocket connection
3. Design message rendering with markdown support
4. Handle connection failures and reconnection
5. Document chat patterns in KB

---

**System Prompt:**

You are the Chat specialist.

**Your expertise:**
- Real-time messaging (SSE, WebSocket)
- Chat UI/UX (message rendering, scrolling, typing indicators)
- Message parsing (markdown, syntax highlighting)
- Event-driven architecture for chat

**Your workflow:**

1. **Pre-flight:**
   - Read `kb/frontend-patterns.md` for chat patterns
   - Read `kb/api-contracts.md` for SSE/WebSocket endpoint schemas
   - Read design requirements from workspace

2. **Execute task:**
   - Implement SSE or WebSocket connection
   - Parse and render messages (markdown to HTML)
   - Handle connection lifecycle (connect, disconnect, reconnect)
   - Add typing indicators, read receipts (if required)

3. **Post-work:**
   - Update `kb/frontend-patterns.md` with chat patterns
   - Log decisions (SSE vs WebSocket choice, reconnection strategy)

**Chat pattern (SSE):**
```javascript
class ChatService {
    constructor(endpoint) {
        this.endpoint = endpoint;
        this.eventSource = null;
    }

    connect() {
        this.eventSource = new EventSource(this.endpoint);

        this.eventSource.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleMessage(message);
        };

        this.eventSource.onerror = () => {
            console.error('SSE connection error');
            this.reconnect();
        };
    }

    reconnect() {
        setTimeout(() => {
            this.connect();
        }, 5000);
    }

    disconnect() {
        if (this.eventSource) {
            this.eventSource.close();
        }
    }

    handleMessage(message) {
        // Emit event for UI to handle
        document.dispatchEvent(new CustomEvent('chat:message', {
            detail: message
        }));
    }
}
```

**Output:**
- Chat service code
- Message rendering utilities
- KB updates with chat patterns
- Workspace notes on connection handling
```

**Step 2: Commit Chat specialist**

```bash
git add skills/chat-specialist/
git commit -m "feat: add Chat specialist"
```

---

## Phase 4: Advanced Coordinator

### Task 14: Auto-Planning Module

**Files:**
- Create: `utils/auto_planner.py`
- Create: `utils/specialist_consultation.py`

**Step 1: Create specialist consultation utility**

```python
# utils/specialist_consultation.py
"""Utilities for coordinator to consult specialists during planning."""

from typing import Dict, List
import json

async def consult_specialist(specialist_name: str, question: str, context: Dict) -> str:
    """
    Consult a specialist for their input during planning phase.

    Args:
        specialist_name: Name of specialist to consult (e.g., 'backend-architect')
        question: Question to ask the specialist
        context: Context dict with relevant info (feature description, current KB state, etc.)

    Returns:
        Specialist's response as string
    """
    # In actual implementation, this would invoke the specialist via Task tool
    # For now, placeholder that constructs consultation prompt

    prompt = f"""
You are being consulted during the planning phase.

Context:
{json.dumps(context, indent=2)}

Question from coordinator:
{question}

Provide your expert input for planning this feature. Focus on:
- What tasks are needed in your domain
- Dependencies on other domains
- Potential challenges or risks
- Estimated complexity

Keep response concise (2-3 paragraphs).
"""

    # TODO: Invoke specialist via Task tool with prompt
    # For now, return placeholder
    return f"[Consultation response from {specialist_name}]"


async def consult_all_relevant_specialists(
    feature_description: str,
    domains_affected: List[str],
    kb_state: Dict
) -> Dict[str, str]:
    """
    Consult all relevant specialists for a feature.

    Args:
        feature_description: User's feature request
        domains_affected: List of domains (e.g., ['backend', 'frontend'])
        kb_state: Current KB state (patterns, recent decisions)

    Returns:
        Dict mapping specialist name to their consultation response
    """
    domain_specialist_map = {
        'backend': ['backend-architect', 'backend-design'],
        'backend-api': ['fastapi-specialist', 'backend-design'],
        'backend-agents': ['openai-agents-sdk'],
        'backend-deployment': ['docker-specialist'],
        'frontend': ['ui-ux', 'javascript-specialist'],
        'frontend-3d': ['matterport-sdk'],
        'frontend-chat': ['chat-specialist']
    }

    specialists_to_consult = set()
    for domain in domains_affected:
        specialists_to_consult.update(domain_specialist_map.get(domain, []))

    # Always consult code reviewer for cleanup assessment
    specialists_to_consult.add('code-reviewer')

    context = {
        'feature_description': feature_description,
        'kb_state': kb_state
    }

    responses = {}
    for specialist in specialists_to_consult:
        question = get_consultation_question(specialist, feature_description)
        response = await consult_specialist(specialist, question, context)
        responses[specialist] = response

    return responses


def get_consultation_question(specialist: str, feature_description: str) -> str:
    """Generate domain-specific consultation question."""
    questions = {
        'backend-architect': f"What's the high-level architecture approach for: {feature_description}?",
        'fastapi-specialist': f"What endpoints/routes are needed for: {feature_description}?",
        'backend-design': f"What API schemas and data models are needed for: {feature_description}?",
        'openai-agents-sdk': f"What agents or tools are needed for: {feature_description}?",
        'docker-specialist': f"Any container config changes needed for: {feature_description}?",
        'ui-ux': f"What UI components and designs are needed for: {feature_description}?",
        'javascript-specialist': f"What JavaScript modules are needed for: {feature_description}?",
        'matterport-sdk': f"Any Matterport SDK integration needed for: {feature_description}?",
        'chat-specialist': f"Any chat/messaging features needed for: {feature_description}?",
        'code-reviewer': f"Any existing code that should be refactored before implementing: {feature_description}?",
        'code-quality-frontend': f"Any frontend code quality concerns for: {feature_description}?"
    }
    return questions.get(specialist, f"Your input for: {feature_description}?")
```

**Step 2: Create auto-planner**

```python
# utils/auto_planner.py
"""Auto-planning module for coordinator."""

from typing import Dict, List
from utils.specialist_consultation import consult_all_relevant_specialists
from utils.dag_parser import parse_task_list
import json

async def auto_plan_feature(
    feature_description: str,
    user_hints: Dict = None
) -> Dict:
    """
    Auto-generate implementation plan by consulting specialists.

    Args:
        feature_description: User's feature request
        user_hints: Optional hints like domains_affected, constraints

    Returns:
        Plan dict with tasks, dependencies, and scope boundaries
    """
    # Step 1: Analyze feature to determine domains affected
    domains = analyze_domains(feature_description, user_hints)

    # Step 2: Load KB state
    kb_state = load_kb_state()

    # Step 3: Consult specialists
    specialist_responses = await consult_all_relevant_specialists(
        feature_description,
        domains,
        kb_state
    )

    # Step 4: Synthesize plan from specialist input
    plan = synthesize_plan(
        feature_description,
        specialist_responses,
        domains
    )

    return plan


def analyze_domains(feature_description: str, user_hints: Dict = None) -> List[str]:
    """
    Analyze feature description to determine affected domains.

    Uses keyword matching and user hints.
    """
    if user_hints and 'domains' in user_hints:
        return user_hints['domains']

    domains = []

    # Keyword-based domain detection
    backend_keywords = ['api', 'endpoint', 'database', 'backend', 'server', 'agent', 'tool']
    frontend_keywords = ['ui', 'component', 'frontend', 'client', 'interface']
    docker_keywords = ['container', 'docker', 'deploy']
    chat_keywords = ['chat', 'message', 'conversation']
    matterport_keywords = ['3d', 'matterport', 'viewer', 'mattertag']

    desc_lower = feature_description.lower()

    if any(kw in desc_lower for kw in backend_keywords):
        domains.append('backend')
    if any(kw in desc_lower for kw in frontend_keywords):
        domains.append('frontend')
    if any(kw in desc_lower for kw in docker_keywords):
        domains.append('backend-deployment')
    if any(kw in desc_lower for kw in chat_keywords):
        domains.append('frontend-chat')
    if any(kw in desc_lower for kw in matterport_keywords):
        domains.append('frontend-3d')

    # Default to both if unclear
    if not domains:
        domains = ['backend', 'frontend']

    return domains


def load_kb_state() -> Dict:
    """Load current KB state (patterns, recent decisions)."""
    from pathlib import Path

    kb_dir = Path('kb')
    state = {
        'patterns': {},
        'recent_decisions': []
    }

    # Load pattern files
    pattern_files = [
        'backend-patterns.md',
        'frontend-patterns.md',
        'api-contracts.md',
        'openai-agents.md',
        'matterport-integration.md',
        'docker-patterns.md'
    ]

    for pattern_file in pattern_files:
        path = kb_dir / pattern_file
        if path.exists():
            state['patterns'][pattern_file] = path.read_text()

    # Load recent decisions (last 10)
    decisions_path = kb_dir / 'decisions.log'
    if decisions_path.exists():
        lines = decisions_path.read_text().split('\n')
        # Parse last 10 decision entries
        state['recent_decisions'] = lines[-50:]  # ~10 decisions (5 lines each)

    return state


def synthesize_plan(
    feature_description: str,
    specialist_responses: Dict[str, str],
    domains: List[str]
) -> Dict:
    """
    Synthesize plan from specialist consultation responses.

    Returns plan with:
    - Task breakdown
    - Dependencies
    - Scope boundaries
    - Success criteria
    """
    tasks = []
    task_id = 1

    # Order specialists by typical workflow
    workflow_order = [
        'code-reviewer',  # Pre-planning cleanup
        'backend-architect',
        'backend-design',
        'openai-agents-sdk',
        'fastapi-specialist',
        'docker-specialist',
        'ui-ux',
        'javascript-specialist',
        'matterport-sdk',
        'chat-specialist',
        'code-quality-frontend'
    ]

    previous_task_id = None

    for specialist in workflow_order:
        if specialist not in specialist_responses:
            continue

        response = specialist_responses[specialist]

        # Extract task from specialist response
        # (In real implementation, parse response to extract task details)
        task_title = extract_task_title(specialist, response)

        task = {
            'id': f'task-{task_id}',
            'title': task_title,
            'specialist': specialist,
            'dependencies': [previous_task_id] if previous_task_id else []
        }

        tasks.append(task)
        previous_task_id = f'task-{task_id}'
        task_id += 1

    plan = {
        'plan_id': f'auto-plan-{hash(feature_description) % 10000}',
        'feature_description': feature_description,
        'domains_affected': domains,
        'tasks': {task['id']: task for task in tasks},
        'scope_boundaries': {
            'what_to_change': extract_scope_from_responses(specialist_responses, 'change'),
            'what_not_to_change': extract_scope_from_responses(specialist_responses, 'preserve')
        },
        'success_criteria': [
            'All tasks completed successfully',
            'KB updated with new patterns',
            'No breaking changes to existing functionality'
        ]
    }

    return plan


def extract_task_title(specialist: str, response: str) -> str:
    """Extract task title from specialist response."""
    # Placeholder - in real implementation, parse response
    titles = {
        'code-reviewer': 'Pre-planning cleanup: remove dead code',
        'backend-architect': 'Design architecture',
        'backend-design': 'Design API schemas',
        'fastapi-specialist': 'Implement endpoints',
        'openai-agents-sdk': 'Create agents and tools',
        'docker-specialist': 'Update container config',
        'ui-ux': 'Design and implement UI',
        'javascript-specialist': 'Implement JavaScript logic',
        'matterport-sdk': 'Integrate Matterport SDK',
        'chat-specialist': 'Implement chat features',
        'code-quality-frontend': 'Review and optimize frontend'
    }
    return titles.get(specialist, f'{specialist} task')


def extract_scope_from_responses(responses: Dict[str, str], scope_type: str) -> List[str]:
    """Extract scope boundaries from specialist responses."""
    # Placeholder - in real implementation, parse responses for scope mentions
    return [
        f'Items to {scope_type} based on specialist input',
        '(Extracted from consultation responses)'
    ]
```

**Step 3: Commit auto-planning module**

```bash
git add utils/auto_planner.py utils/specialist_consultation.py
git commit -m "feat: add auto-planning module with specialist consultation"
```

---

### Task 15: Parallel Execution Engine

**Files:**
- Create: `utils/parallel_executor.py`

**Step 1: Create parallel executor**

```python
# utils/parallel_executor.py
"""Parallel task execution engine for coordinator."""

import asyncio
from typing import Dict, List, Set
from utils.dag_parser import get_ready_tasks, update_task_status

class ParallelExecutor:
    """Executes tasks in parallel based on DAG dependencies."""

    def __init__(self, plan: Dict):
        self.plan = plan
        self.running_tasks: Set[str] = set()
        self.max_parallel = 3  # Max concurrent specialist invocations

    async def execute_plan(self) -> None:
        """Execute all tasks in plan with parallelization."""
        while not self.is_plan_complete():
            ready_tasks = get_ready_tasks(self.plan)

            # Filter out tasks already running
            ready_tasks = [t for t in ready_tasks if t not in self.running_tasks]

            if not ready_tasks:
                # No ready tasks, wait for running tasks to complete
                if self.running_tasks:
                    await asyncio.sleep(1)
                    continue
                else:
                    # No ready tasks and nothing running = blocked or complete
                    break

            # Launch tasks in parallel (up to max_parallel)
            tasks_to_launch = ready_tasks[:self.max_parallel - len(self.running_tasks)]

            for task_id in tasks_to_launch:
                asyncio.create_task(self.execute_task(task_id))
                self.running_tasks.add(task_id)

            await asyncio.sleep(0.5)  # Brief pause before next iteration

    async def execute_task(self, task_id: str) -> None:
        """Execute a single task via specialist invocation."""
        task = self.plan['tasks'][task_id]

        try:
            # Update status to in-progress
            update_task_status(self.plan, task_id, 'in-progress')

            # Invoke specialist (placeholder - actual implementation uses Task tool)
            result = await self.invoke_specialist(
                specialist=task['specialist'],
                task_title=task['title'],
                task_id=task_id
            )

            # Run checkpoint
            await self.run_checkpoint(task_id, result)

            # Update status to completed
            update_task_status(self.plan, task_id, 'completed')

        except Exception as e:
            # Handle failure
            update_task_status(self.plan, task_id, 'failed')
            task['error_context'] = str(e)

        finally:
            # Remove from running set
            self.running_tasks.discard(task_id)

    async def invoke_specialist(
        self,
        specialist: str,
        task_title: str,
        task_id: str
    ) -> Dict:
        """
        Invoke specialist via Task tool.

        In actual implementation, this uses the Task tool to spawn specialist agent.
        Specialist receives:
        - Task title and description
        - Workspace files from predecessor tasks
        - Relevant KB sections

        Returns specialist output.
        """
        # Placeholder - actual implementation uses Task tool
        print(f"[Parallel Executor] Invoking {specialist} for {task_id}")

        # Simulate work
        await asyncio.sleep(2)

        return {
            'task_id': task_id,
            'specialist': specialist,
            'output': f'Completed {task_title}',
            'workspace_files': [f'work/{task_id}-output.md'],
            'kb_updates': []
        }

    async def run_checkpoint(self, task_id: str, result: Dict) -> None:
        """
        Run checkpoint validation after task completes.

        Checks:
        - Workspace file created
        - KB updated if needed
        - Pattern compliance
        """
        print(f"[Checkpoint] Validating {task_id}")

        # Verify workspace file exists
        workspace_files = result.get('workspace_files', [])
        for wf in workspace_files:
            # In real implementation, check file exists
            pass

        # Verify KB updated if needed
        kb_updates = result.get('kb_updates', [])
        # In real implementation, check KB files modified

        # Update task with outputs
        task = self.plan['tasks'][task_id]
        task['output_workspace'] = ','.join(workspace_files)
        task['kb_updates'] = kb_updates

        print(f"[Checkpoint] {task_id} validated ✓")

    def is_plan_complete(self) -> bool:
        """Check if all tasks are completed or blocked."""
        statuses = [task['status'] for task in self.plan['tasks'].values()]
        return all(s in ['completed', 'failed', 'blocked'] for s in statuses)


async def execute_plan_parallel(plan: Dict) -> Dict:
    """
    Execute plan with parallel task orchestration.

    Args:
        plan: Plan dict from auto_planner or manual parsing

    Returns:
        Updated plan with task statuses and results
    """
    executor = ParallelExecutor(plan)
    await executor.execute_plan()
    return executor.plan
```

**Step 2: Commit parallel executor**

```bash
git add utils/parallel_executor.py
git commit -m "feat: add parallel execution engine for DAG orchestration"
```

---

### Task 16: Advanced Checkpoints

**Files:**
- Create: `utils/checkpoint_validator.py`

**Step 1: Create checkpoint validator**

```python
# utils/checkpoint_validator.py
"""Advanced checkpoint validation with peer review."""

from typing import Dict, List
from pathlib import Path
import json

class CheckpointValidator:
    """Comprehensive checkpoint validation after each task."""

    def __init__(self, plan: Dict, task_id: str):
        self.plan = plan
        self.task = plan['tasks'][task_id]
        self.task_id = task_id

    async def run_checkpoint(self) -> bool:
        """
        Run full checkpoint workflow.

        Returns True if validation passed, False otherwise.
        """
        print(f"\n=== Checkpoint: {self.task_id} ===")

        # Step 1: Automatic validation
        if not await self.automatic_validation():
            print("❌ Automatic validation failed")
            return False

        # Step 2: Peer review
        if not await self.peer_review():
            print("❌ Peer review failed")
            return False

        # Step 3: KB sync
        if not await self.kb_sync():
            print("❌ KB sync failed")
            return False

        # Step 4: Final approval
        self.final_approval()
        print("✅ Checkpoint passed\n")
        return True

    async def automatic_validation(self) -> bool:
        """
        Step 1: Automatic validation (fast feedback).

        Checks:
        - Workspace files created
        - Pattern compliance
        - No obvious errors
        """
        print("  [1/4] Running automatic validation...")

        # Check workspace files
        workspace_file = self.task.get('output_workspace')
        if workspace_file and not Path(workspace_file).exists():
            print(f"    ⚠ Workspace file missing: {workspace_file}")
            return False

        # Check KB updates if expected
        # (Pattern compliance check would go here)

        print("    ✓ Automatic validation passed")
        return True

    async def peer_review(self) -> bool:
        """
        Step 2: Peer review by relevant specialists.

        Invokes:
        - Code Reviewer (always)
        - Domain specialists (if cross-domain impact)
        - Architecture specialist (for design tasks)
        """
        print("  [2/4] Running peer review...")

        reviewers = self.get_peer_reviewers()

        for reviewer in reviewers:
            print(f"    Consulting {reviewer}...")
            review_result = await self.invoke_reviewer(reviewer)

            if not review_result['approved']:
                print(f"    ❌ {reviewer} flagged issues:")
                for issue in review_result['issues']:
                    print(f"      - {issue}")
                return False

        print("    ✓ Peer review passed")
        return True

    def get_peer_reviewers(self) -> List[str]:
        """Determine which specialists should review this task."""
        specialist = self.task['specialist']
        reviewers = []

        # Always review by code reviewer
        if specialist not in ['code-reviewer', 'code-quality-frontend']:
            if 'frontend' in specialist or 'ui' in specialist or 'javascript' in specialist:
                reviewers.append('code-quality-frontend')
            else:
                reviewers.append('code-reviewer')

        # Cross-domain review
        domain_map = {
            'fastapi-specialist': ['backend-architect'],  # Architect reviews implementation
            'openai-agents-sdk': ['backend-architect'],
            'ui-ux': ['code-quality-frontend'],
            'javascript-specialist': ['code-quality-frontend']
        }

        if specialist in domain_map:
            reviewers.extend(domain_map[specialist])

        return reviewers

    async def invoke_reviewer(self, reviewer: str) -> Dict:
        """
        Invoke reviewer specialist to check task output.

        Reviewer receives:
        - Task output (code files, workspace notes)
        - KB patterns to check against
        - Review checklist

        Returns review result with approval status and issues found.
        """
        # Placeholder - actual implementation invokes reviewer via Task tool
        # For now, simulate approval
        return {
            'reviewer': reviewer,
            'approved': True,
            'issues': []
        }

    async def kb_sync(self) -> bool:
        """
        Step 3: Knowledge base sync.

        Ensures:
        - Pattern files updated if new conventions introduced
        - Decisions logged with rationale
        - Dependencies updated if contracts changed
        - No conflicts with recent decisions
        """
        print("  [3/4] Running KB sync...")

        # Check if task made KB updates
        kb_updates = self.task.get('kb_updates', [])

        if not kb_updates:
            print("    ℹ No KB updates for this task")
            return True

        # Verify KB files were actually modified
        for kb_file in kb_updates:
            if not Path(kb_file).exists():
                print(f"    ⚠ KB file missing: {kb_file}")
                return False

        # Check for decision conflicts
        if 'kb/decisions.log' in kb_updates:
            if not self.check_decision_conflicts():
                print("    ⚠ Decision conflicts detected")
                return False

        print("    ✓ KB sync completed")
        return True

    def check_decision_conflicts(self) -> bool:
        """Check if new decisions conflict with recent ones."""
        # In real implementation, parse decisions.log and check for conflicts
        # For now, assume no conflicts
        return True

    def final_approval(self) -> None:
        """
        Step 4: Final approval.

        Mark task as validated and prepare next tasks.
        """
        print("  [4/4] Final approval...")

        # Update task status to validated
        self.task['status'] = 'validated'

        # Transition dependent tasks to ready
        for task_id, task in self.plan['tasks'].items():
            if self.task_id in task.get('dependencies', []):
                deps_satisfied = all(
                    self.plan['tasks'][dep]['status'] in ['completed', 'validated']
                    for dep in task['dependencies']
                )
                if deps_satisfied and task['status'] == 'pending':
                    task['status'] = 'ready'

        print("    ✓ Task validated, dependents transitioned to ready")


async def run_checkpoint(plan: Dict, task_id: str) -> bool:
    """
    Run comprehensive checkpoint for a task.

    Args:
        plan: Current plan state
        task_id: ID of task to validate

    Returns:
        True if checkpoint passed, False otherwise
    """
    validator = CheckpointValidator(plan, task_id)
    return await validator.run_checkpoint()
```

**Step 2: Commit checkpoint validator**

```bash
git add utils/checkpoint_validator.py
git commit -m "feat: add advanced checkpoint validator with peer review"
```

---

### Task 17: Error Recovery System

**Files:**
- Create: `utils/error_recovery.py`

**Step 1: Create error recovery system**

```python
# utils/error_recovery.py
"""Adaptive error recovery for specialist task failures."""

from typing import Dict, Optional
from enum import Enum

class FailureType(Enum):
    FIXABLE = "fixable"
    FUNDAMENTAL = "fundamental"

class ErrorRecovery:
    """Handles specialist task failures with adaptive recovery."""

    def __init__(self, plan: Dict, task_id: str):
        self.plan = plan
        self.task = plan['tasks'][task_id]
        self.task_id = task_id
        self.max_retries = 3

    async def handle_failure(self, error: Exception) -> bool:
        """
        Handle task failure with adaptive recovery.

        Returns True if recovery successful and task can retry,
        False if fundamental failure requiring user escalation.
        """
        print(f"\n=== Error Recovery: {self.task_id} ===")
        print(f"Error: {error}")

        # Step 1: Capture context
        context = self.capture_failure_context(error)

        # Step 2: Classify failure type
        failure_type = self.classify_failure(error, context)

        if failure_type == FailureType.FIXABLE:
            return await self.handle_fixable_failure(context)
        else:
            return await self.handle_fundamental_failure(context)

    def capture_failure_context(self, error: Exception) -> Dict:
        """Capture full context of failure."""
        return {
            'task_id': self.task_id,
            'specialist': self.task['specialist'],
            'error_message': str(error),
            'retry_count': self.task.get('retry_count', 0),
            'dependencies': self.task.get('dependencies', []),
            'workspace_files': self.get_workspace_files(),
            'kb_state': self.get_kb_state()
        }

    def classify_failure(self, error: Exception, context: Dict) -> FailureType:
        """
        Classify failure as fixable or fundamental.

        Fixable:
        - Missing information from upstream task
        - Unclear requirements
        - Dependency conflict (can be resolved)

        Fundamental:
        - Plan assumption incorrect
        - Architectural conflict
        - Impossible requirement
        """
        error_msg = str(error).lower()

        # Fixable indicators
        fixable_keywords = [
            'unclear', 'missing', 'not found', 'undefined',
            'need more', 'clarification', 'incomplete'
        ]

        # Fundamental indicators
        fundamental_keywords = [
            'impossible', 'conflict', 'incompatible',
            'architecture', 'cannot', 'violation'
        ]

        if any(kw in error_msg for kw in fundamental_keywords):
            return FailureType.FUNDAMENTAL

        if any(kw in error_msg for kw in fixable_keywords):
            return FailureType.FIXABLE

        # Default to fixable if under retry limit
        if context['retry_count'] < self.max_retries:
            return FailureType.FIXABLE
        else:
            return FailureType.FUNDAMENTAL

    async def handle_fixable_failure(self, context: Dict) -> bool:
        """
        Handle fixable failure with loop-back or consultation.

        Strategies:
        1. Loop back to prerequisite specialist for clarification
        2. Consult other specialists for solution
        3. Retry with additional context
        """
        print("  Classified as FIXABLE failure")

        retry_count = context['retry_count']

        if retry_count < self.max_retries:
            # Attempt recovery
            recovery_successful = await self.attempt_recovery(context)

            if recovery_successful:
                print("  ✓ Recovery successful, will retry task")
                self.task['retry_count'] = retry_count + 1
                return True
            else:
                print("  ✗ Recovery failed, escalating")
                return False
        else:
            print(f"  ✗ Max retries ({self.max_retries}) exceeded, escalating")
            return False

    async def attempt_recovery(self, context: Dict) -> bool:
        """
        Attempt to recover from fixable failure.

        Steps:
        1. Identify prerequisite task that needs clarification
        2. Loop back to prerequisite specialist
        3. Get clarification
        4. Update workspace with clarification
        """
        dependencies = context['dependencies']

        if not dependencies:
            print("    No dependencies to loop back to")
            return False

        # Loop back to last dependency (most recent prerequisite)
        prerequisite_task_id = dependencies[-1]
        prerequisite_task = self.plan['tasks'][prerequisite_task_id]
        prerequisite_specialist = prerequisite_task['specialist']

        print(f"    Looping back to {prerequisite_specialist} ({prerequisite_task_id})")

        # Extract question from failure context
        question = self.extract_clarification_question(context)

        print(f"    Question: {question}")

        # Invoke prerequisite specialist for clarification
        clarification = await self.get_clarification(
            prerequisite_specialist,
            question,
            context
        )

        # Update workspace with clarification
        self.update_workspace_with_clarification(
            prerequisite_task_id,
            clarification
        )

        return True

    def extract_clarification_question(self, context: Dict) -> str:
        """Extract specific question from failure context."""
        error_msg = context['error_message']
        # In real implementation, parse error to extract question
        return f"Clarification needed: {error_msg}"

    async def get_clarification(
        self,
        specialist: str,
        question: str,
        context: Dict
    ) -> str:
        """
        Get clarification from prerequisite specialist.

        Invokes specialist with question and context.
        """
        # Placeholder - actual implementation invokes specialist via Task tool
        print(f"    Getting clarification from {specialist}...")
        return f"Clarification: [Response from {specialist}]"

    def update_workspace_with_clarification(
        self,
        prerequisite_task_id: str,
        clarification: str
    ) -> None:
        """Update workspace file with clarification."""
        prerequisite_task = self.plan['tasks'][prerequisite_task_id]
        workspace_file = prerequisite_task.get('output_workspace')

        if workspace_file:
            # Append clarification to workspace file
            print(f"    Updated {workspace_file} with clarification")

    async def handle_fundamental_failure(self, context: Dict) -> bool:
        """
        Handle fundamental failure with user escalation.

        Actions:
        1. Block failed task and all dependents
        2. Continue independent parallel tasks
        3. Present failure report to user with options
        """
        print("  Classified as FUNDAMENTAL failure")

        # Block this task and dependents
        self.block_task_and_dependents()

        # Generate failure report
        report = self.generate_failure_report(context)

        print("\n" + "="*60)
        print("FUNDAMENTAL FAILURE - USER ESCALATION REQUIRED")
        print("="*60)
        print(report)
        print("="*60)

        # In real implementation, present to user and get decision
        # For now, return False (not recovered)
        return False

    def block_task_and_dependents(self) -> None:
        """Block failed task and all downstream dependents."""
        self.task['status'] = 'blocked'

        # Block all tasks that depend on this one
        for task_id, task in self.plan['tasks'].items():
            if self.task_id in task.get('dependencies', []):
                task['status'] = 'blocked'
                print(f"    Blocked dependent task: {task_id}")

    def generate_failure_report(self, context: Dict) -> str:
        """Generate detailed failure report for user."""
        report = f"""
Task Failed: {self.task['title']}
Specialist: {self.task['specialist']}
Reason: {context['error_message']}

Context:
- Retry attempts: {context['retry_count']}/{self.max_retries}
- Dependencies: {', '.join(context['dependencies']) or 'None'}

Impact:
- This task is blocked
- Dependent tasks are blocked: [list]

Options:
1. Amend plan to adjust scope
2. Provide additional information/requirements
3. Abandon this feature
4. Continue with independent tasks

Recommendation: [Coordinator's recommendation based on failure type]
"""
        return report

    def get_workspace_files(self) -> list:
        """Get workspace files for this task."""
        # Placeholder
        return []

    def get_kb_state(self) -> dict:
        """Get current KB state."""
        # Placeholder
        return {}


async def handle_task_failure(plan: Dict, task_id: str, error: Exception) -> bool:
    """
    Handle task failure with adaptive recovery.

    Args:
        plan: Current plan state
        task_id: Failed task ID
        error: Exception that caused failure

    Returns:
        True if recovery successful (can retry), False if escalation needed
    """
    recovery = ErrorRecovery(plan, task_id)
    return await recovery.handle_failure(error)
```

**Step 2: Commit error recovery system**

```bash
git add utils/error_recovery.py
git commit -m "feat: add adaptive error recovery system with loop-back and escalation"
```

---

### Task 18: Full Coordinator Skill

**Files:**
- Create: `skills/dev-team/skill.md` (full version, replacing MVP)

**Step 1: Write full coordinator skill**

```markdown
# Dev Team Coordinator (Full)

**Purpose:** Orchestrate multiple specialists to complete complex multi-domain tasks with auto-planning, parallel execution, advanced checkpoints, and adaptive error recovery.

**Workflow:**

## Phase 1: Pre-Planning Cleanup

Invoke Code Reviewer specialist to scan for dead/stale code before planning.

```python
from utils.kb_manager import initialize_kb

# Initialize KB if this is first use
if not verify_kb_exists():
    initialize_kb()

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

## Phase 2: Auto-Planning

Consult specialists to generate implementation plan.

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

if not user_approved:
    # User wants to modify plan
    plan = await modify_plan_with_user_input(plan)
```

## Phase 3: Parallel Execution

Execute tasks via DAG with parallelization.

```python
from utils.parallel_executor import execute_plan_parallel
from utils.checkpoint_validator import run_checkpoint
from utils.error_recovery import handle_task_failure

# Execute plan with parallel orchestration
try:
    updated_plan = await execute_plan_parallel(plan)

    # Present completion summary
    present_completion_summary(updated_plan)

except Exception as e:
    # Handle plan-level failures
    handle_plan_failure(plan, e)
```

## Phase 4: Completion

Present summary, offer workspace cleanup.

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

---

**System Prompt for Full Coordinator:**

You are the Coordinator for the multi-agent dev team (full version).

**Your capabilities:**
- Auto-planning via specialist consultation
- Parallel task execution via DAG
- Advanced checkpoints with peer review
- Adaptive error recovery

**Phase 1: Pre-Planning Cleanup**

Invoke code-reviewer specialist to scan for dead/stale code:
- Unused imports, functions, classes
- Dead code paths
- Deprecated patterns

Present findings to user for approval before planning.

**Phase 2: Auto-Planning**

1. Analyze feature description to determine domains
2. Consult relevant specialists for their input
3. Synthesize plan with:
   - Task breakdown
   - Dependencies (explicit + inferred)
   - Scope boundaries (what to change, what NOT to change)
   - Success criteria
4. Present plan to user for approval

**Phase 3: Parallel Execution**

1. Parse plan into task DAG
2. Execute tasks in parallel (up to 3 concurrent)
3. Run checkpoints after each task:
   - Automatic validation
   - Peer review by specialists
   - KB sync (patterns, decisions, dependencies)
   - Final approval
4. Handle failures with adaptive recovery:
   - Fixable: Loop back to prerequisite specialist
   - Fundamental: Block dependents, escalate to user

**Phase 4: Completion**

1. Present summary:
   - Tasks completed
   - KB updates made
   - Workspace files created
2. Offer workspace cleanup
3. Log session summary to KB

**Example invocation:**

```
User: /dev-team "Add user authentication with JWT"

Coordinator:
→ Phase 1: Code Reviewer scans for dead code
  → Finds 3 unused imports in auth.py
  → User approves cleanup

→ Phase 2: Auto-planning
  → Consults backend-architect, fastapi-specialist, backend-design, docker-specialist
  → Synthesizes plan with 5 tasks
  → User approves plan

→ Phase 3: Parallel execution
  → Task 1 (backend-architect): Design auth flow
    → Checkpoint passed
  → Task 2 (backend-design): Design API schemas
  → Task 3 (fastapi-specialist): Implement /auth/login
    → Runs in parallel with Task 2
    → Checkpoint passed
  → Task 4 (code-reviewer): Review and simplify
    → Checkpoint passed
  → Task 5 (docker-specialist): Update container config
    → Checkpoint passed

→ Phase 4: Completion
  → Summary: 5 tasks completed, KB updated, 5 workspace files created
  → User approves workspace cleanup
  → Session complete
```

**Error handling example:**

```
Task 3 (fastapi-specialist) fails: "Design unclear about token storage"

Coordinator:
→ Classifies as FIXABLE failure
→ Loops back to Task 1 (backend-architect)
→ Gets clarification: "Store tokens in Redis with TTL"
→ Updates work/auth-design.md with clarification
→ Retries Task 3
→ Task 3 succeeds on retry
→ Continues execution
```

**Utilities available:**
- `utils/auto_planner.py` - Auto-planning with specialist consultation
- `utils/parallel_executor.py` - Parallel DAG execution
- `utils/checkpoint_validator.py` - Advanced checkpoints
- `utils/error_recovery.py` - Adaptive error recovery
- `utils/kb_manager.py` - KB initialization and management
- `utils/dag_parser.py` - DAG parsing and manipulation
```

**Step 2: Commit full coordinator**

```bash
git add skills/dev-team/
git commit -m "feat: upgrade coordinator to full version with auto-planning and parallel execution"
```

---

## Phase 5: Testing & Documentation

### Task 19: Integration Tests (Full System)

**Files:**
- Create: `tests/test_full_system.py`
- Create: `tests/test_auto_planner.py`
- Create: `tests/test_parallel_executor.py`
- Create: `tests/test_error_recovery.py`

[Similar to MVP tests but comprehensive]

---

### Task 20: Full Documentation

**Files:**
- Create/Update: `docs/USER_GUIDE.md` (full version)
- Create/Update: `docs/SPECIALIST_GUIDE.md` (all 11 specialists)
- Create/Update: `docs/ARCHITECTURE.md` (full system)
- Create: `docs/TROUBLESHOOTING.md`
- Create: `docs/EXAMPLES.md`

[Comprehensive documentation for all features]

---

## Phase 6: Deployment

### Task 21: Final Packaging

**Step 1: Update plugin.json with all specialists**

```json
{
  "name": "multi-agent-dev-team",
  "version": "1.0.0",
  "description": "Domain specialist agents that collaborate through shared knowledge to prevent codebase drift",
  "author": "Rhett",
  "skills": [
    "dev-team",
    "openai-agents-sdk",
    "backend-architect",
    "fastapi-specialist",
    "backend-design",
    "code-reviewer",
    "docker-specialist",
    "ui-ux",
    "code-quality-frontend",
    "matterport-sdk",
    "javascript-specialist",
    "chat-specialist"
  ],
  "requires": {
    "claude-code": ">=1.0.0",
    "python": ">=3.11"
  }
}
```

**Step 2: Create CHANGELOG**

[Comprehensive changelog with all features]

**Step 3: Final commit and tag**

```bash
git tag -a v1.0.0 -m "Full release: 11 specialists with auto-planning, parallel execution, and error recovery"
```

---

## Success Criteria (Full System)

✅ All 11 specialists implemented with system prompts
✅ Auto-planning module with specialist consultation
✅ Parallel DAG execution engine
✅ Advanced checkpoints with peer review
✅ Adaptive error recovery system
✅ KB system with 3-part structure
✅ Comprehensive tests passing
✅ Full documentation complete
✅ Plugin recognized by Claude Code

---

## Implementation Sequence

**Recommended order:**
1. Foundation (Tasks 1-2) - Plugin structure and schemas
2. MVP specialists (Tasks 3-8) - Validate core patterns
3. Full backend specialists (Tasks 3-8) - Complete backend coverage
4. Full frontend specialists (Tasks 9-13) - Complete frontend coverage
5. Advanced coordinator (Tasks 14-18) - Auto-planning, parallel execution, error recovery
6. Testing (Task 19) - Validate full system
7. Documentation (Task 20) - Comprehensive guides
8. Deployment (Task 21) - Final packaging

**Milestones:**
- M1: Foundation complete (Tasks 1-2)
- M2: MVP specialists working (Tasks 3-8, subset)
- M3: All 11 specialists implemented (Tasks 3-13)
- M4: Advanced coordinator features (Tasks 14-18)
- M5: Full system validated (Tasks 19-21)

---

## Appendix: Full File Tree

```
multi-agent-dev-team/
├── plugin.json
├── README.md
├── CHANGELOG.md
├── .gitignore
├── docs/
│   ├── plans/
│   │   ├── 2026-02-03-mvp-implementation.md
│   │   └── 2026-02-03-full-implementation.md
│   ├── USER_GUIDE.md
│   ├── SPECIALIST_GUIDE.md
│   ├── ARCHITECTURE.md
│   ├── TROUBLESHOOTING.md
│   └── EXAMPLES.md
├── skills/
│   ├── README.md
│   ├── dev-team/skill.md (full coordinator)
│   ├── openai-agents-sdk/skill.md
│   ├── backend-architect/skill.md
│   ├── fastapi-specialist/skill.md
│   ├── backend-design/skill.md
│   ├── code-reviewer/skill.md
│   ├── docker-specialist/skill.md
│   ├── ui-ux/skill.md
│   ├── code-quality-frontend/skill.md
│   ├── matterport-sdk/skill.md
│   ├── javascript-specialist/skill.md
│   └── chat-specialist/skill.md
├── utils/
│   ├── dag_parser.py
│   ├── kb_manager.py
│   ├── auto_planner.py
│   ├── specialist_consultation.py
│   ├── parallel_executor.py
│   ├── checkpoint_validator.py
│   └── error_recovery.py
├── schemas/
│   ├── kb-pattern.schema.json
│   ├── dependencies.schema.json
│   ├── task-dag.schema.json
│   └── coordinator-state.schema.json
├── kb/
│   └── README.md
├── tests/
│   ├── test_mvp_flow.py
│   ├── test_full_system.py
│   ├── test_auto_planner.py
│   ├── test_parallel_executor.py
│   └── test_error_recovery.py
└── test_codebase/
    ├── backend/
    ├── frontend/
    ├── kb/
    └── work/
```
