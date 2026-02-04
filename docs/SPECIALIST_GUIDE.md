# Specialist Guide

## Overview

The Multi-Agent Dev Team plugin includes 12 specialized agents, each with focused expertise. This guide documents all specialists and how to create new ones.

## All Specialists (12)

### Backend Specialists (5)

#### 1. Backend Architect
**Role:** System design, architecture patterns, multi-agent coordination

**Capabilities:**
- Design system architectures and module structures
- Define integration patterns between components
- Coordinate multi-agent workflows
- Establish architectural patterns and conventions

**When to use:**
- Designing new features or systems
- Planning major refactors
- Setting architectural direction
- Resolving cross-domain issues

**KB Usage:**
- Reads: `backend-patterns.md`, `api-contracts.md`, `decisions.log`
- Writes: Architecture decisions, design patterns

---

#### 2. Backend Design
**Role:** API schemas, data structures, contract design

**Capabilities:**
- Design Pydantic models and schemas
- Define API request/response contracts
- Structure data validation rules
- Design error responses

**When to use:**
- Defining new API endpoints
- Updating data models
- Designing database schemas
- Creating validation logic

**KB Usage:**
- Reads: `api-contracts.md`, `backend-patterns.md`
- Writes: Schema definitions, contract updates to `api-contracts.md`

---

#### 3. FastAPI Specialist
**Role:** FastAPI endpoints, routing, middleware implementation

**Capabilities:**
- Implement FastAPI endpoints
- Configure routing and middleware
- Handle SSE streaming
- Implement dependency injection

**When to use:**
- Creating new API endpoints
- Implementing authentication/middleware
- Setting up routing logic
- Adding SSE/WebSocket endpoints

**KB Usage:**
- Reads: `api-contracts.md` (implements contracts)
- Writes: Implementation decisions, patterns discovered

---

#### 4. Database Migration Specialist
**Role:** Schema changes, migrations, data integrity

**Capabilities:**
- Design database migrations
- Handle schema evolution
- Ensure data integrity during changes
- Write migration scripts (Supabase SQL)

**When to use:**
- Adding/modifying database tables
- Changing column types or constraints
- Data migrations
- Database refactoring

**KB Usage:**
- Reads: `backend-patterns.md`, `dependencies.json`
- Writes: Migration decisions, schema evolution notes

---

#### 5. OpenAI Agents SDK Specialist
**Role:** Agent creation, tool definitions, streaming

**Capabilities:**
- Create OpenAI agents with proper configuration
- Define @function_tool decorated tools
- Implement streaming responses
- Handle agent orchestration

**When to use:**
- Adding new AI agents
- Creating agent tools
- Implementing streaming logic
- Debugging agent behavior

**KB Usage:**
- Reads: `backend-patterns.md`
- Writes: Agent patterns, tool design decisions

---

### Frontend Specialists (5)

#### 6. UI/UX Specialist
**Role:** Component design, user flows, accessibility

**Capabilities:**
- Design UI component structure
- Plan user interaction flows
- Ensure accessibility (WCAG)
- Design responsive layouts

**When to use:**
- Creating new UI features
- Redesigning user flows
- Improving accessibility
- Planning component hierarchy

**KB Usage:**
- Reads: `frontend-patterns.md`
- Writes: UI patterns, design decisions

---

#### 7. JavaScript Specialist
**Role:** Core JavaScript, async patterns, module organization

**Capabilities:**
- Implement JavaScript logic
- Handle async/await patterns
- Organize module structure
- Optimize performance

**When to use:**
- Implementing business logic
- Refactoring JavaScript code
- Fixing JavaScript bugs
- Optimizing performance

**KB Usage:**
- Reads: `frontend-patterns.md`, `api-contracts.md`
- Writes: JavaScript patterns, module organization decisions

---

#### 8. Code Quality (Frontend)
**Role:** Refactoring, simplification, frontend best practices

**Capabilities:**
- Refactor complex frontend code
- Simplify component logic
- Remove code duplication
- Apply frontend best practices

**When to use:**
- Cleaning up legacy code
- Simplifying complex components
- Removing duplication
- Improving maintainability

**KB Usage:**
- Reads: `frontend-patterns.md`
- Writes: Refactoring patterns, anti-patterns to avoid

---

#### 9. Chat Specialist
**Role:** Chat UI, message streaming, real-time features

**Capabilities:**
- Implement chat interfaces
- Handle SSE message streaming
- Manage chat state
- Parse and render markdown

**When to use:**
- Building/updating chat UI
- Implementing message streaming
- Adding chat features
- Debugging chat issues

**KB Usage:**
- Reads: `frontend-patterns.md`, `api-contracts.md`
- Writes: Chat patterns, streaming implementation notes

---

#### 10. Matterport SDK Specialist
**Role:** 3D viewer integration, camera positioning, scene interaction

**Capabilities:**
- Integrate Matterport SDK
- Control camera positioning
- Add 3D tags/mattertags
- Handle scene events

**When to use:**
- Adding Matterport features
- Debugging 3D viewer issues
- Implementing navigation in 3D
- Adding scene interactivity

**KB Usage:**
- Reads: `frontend-patterns.md`
- Writes: Matterport integration patterns

---

### Cross-Cutting Specialists (2)

#### 11. Code Reviewer
**Role:** Dead code detection, simplification, anti-pattern identification

**Capabilities:**
- Scan for unused code (imports, functions, classes)
- Identify deprecated patterns
- Find dead code paths
- Suggest simplifications

**When to use:**
- Pre-planning cleanup (automatic)
- Post-implementation review
- Periodic codebase cleanup
- Before major refactors

**KB Usage:**
- Reads: All KB files to identify unused patterns
- Writes: Cleanup recommendations, anti-patterns found

---

#### 12. Docker Specialist
**Role:** Containerization, environment config, deployment

**Capabilities:**
- Create/update Dockerfiles
- Configure docker-compose
- Manage environment variables
- Design multi-stage builds

**When to use:**
- Containerizing applications
- Updating deployment config
- Adding new services
- Optimizing container builds

**KB Usage:**
- Reads: `backend-patterns.md`, `dependencies.json`
- Writes: Deployment patterns, configuration decisions

---

## Cross-Specialist Coordination Patterns

### Pattern 1: Design → Implementation → Review

**Flow:**
```
Backend Architect → Backend Design → FastAPI Specialist → Code Reviewer
```

**Example:** Adding a new API endpoint
1. Backend Architect: Design overall architecture
2. Backend Design: Define request/response schemas
3. FastAPI Specialist: Implement the endpoint
4. Code Reviewer: Simplify and validate

**KB Coordination:**
- Architect writes to `decisions.log`
- Design writes to `api-contracts.md`
- FastAPI reads contracts, writes implementation notes
- Reviewer reads all, writes simplification suggestions

---

### Pattern 2: Parallel Frontend + Backend

**Flow:**
```
         Backend Architect
         /              \
Backend Design    UI/UX Specialist
         |              |
  FastAPI Specialist  JavaScript Specialist
         \              /
          Code Reviewer
```

**Example:** Adding user authentication
- Backend Architect + UI/UX run in parallel
- Backend Design + JavaScript Specialist run in parallel
- Code Reviewer integrates and validates both

**KB Coordination:**
- Both write to `api-contracts.md` (API contract)
- Both write to `dependencies.json` (frontend ↔ backend)
- Code Reviewer ensures consistency

---

### Pattern 3: Migration with Fallback

**Flow:**
```
DB Migration Specialist → Backend Design → FastAPI Specialist → Code Reviewer
                       ↓ (if fails)
                Backend Architect (clarify design)
```

**Example:** Changing database schema
1. DB Migration proposes schema change
2. If unclear, Backend Architect clarifies
3. Backend Design updates models
4. FastAPI updates endpoints
5. Code Reviewer validates

**KB Coordination:**
- Migration writes to `decisions.log` (why schema changed)
- Design updates `api-contracts.md` (new models)
- Dependencies tracked in `dependencies.json`

---

### Pattern 4: 3D Feature Implementation

**Flow:**
```
UI/UX Specialist → Matterport SDK Specialist → JavaScript Specialist → Code Quality
```

**Example:** Adding 3D navigation markers
1. UI/UX: Design marker appearance and behavior
2. Matterport SDK: Implement mattertag creation
3. JavaScript: Connect to backend navigation data
4. Code Quality: Refactor for maintainability

**KB Coordination:**
- UI/UX writes design patterns to `frontend-patterns.md`
- Matterport SDK writes integration patterns
- JavaScript writes data flow patterns

---

### Pattern 5: Full-Stack Feature with Deployment

**Flow:**
```
Backend Architect → [Backend Design + UI/UX] → [FastAPI + JavaScript] → Docker Specialist → Code Reviewer
```

**Example:** Complete new feature with deployment
1. Architect: Overall design
2. Design + UI/UX: Parallel schema and UI design
3. FastAPI + JavaScript: Parallel implementation
4. Docker: Update deployment config
5. Code Reviewer: Final validation

**KB Coordination:**
- All specialists read/write to relevant KB files
- Docker ensures deployment reflects KB patterns
- Code Reviewer ensures consistency across all domains

---

### How Specialists Use KB

**Before starting work:**
1. Read relevant pattern files for conventions
2. Check `decisions.log` for precedent
3. Review `dependencies.json` for conflicts

**During work:**
4. Follow established patterns from KB
5. Update patterns if establishing new conventions
6. Log interim decisions

**After completing work:**
7. Write final decisions to `decisions.log`
8. Update pattern files with new conventions
9. Update `dependencies.json` if contracts changed

**Example KB workflow:**
```
FastAPI Specialist starts work:
→ Reads kb/backend-patterns.md: "Use snake_case for endpoints"
→ Reads kb/api-contracts.md: "Auth returns {token, expires_at}"
→ Implements /auth/login following conventions
→ Writes to kb/decisions.log: "Used bcrypt cost factor 12"
→ Updates kb/dependencies.json: "/auth/login → frontend/auth.js"
```

---

## Creating a New Specialist

This section shows you how to create a custom specialist agent for the Multi-Agent Dev Team plugin.

## Directory Structure

Each specialist has this structure:

```
specialists/
└── your-specialist/
    ├── skill.md              # The specialist's skill definition
    ├── context/              # Optional: specialist-specific context
    │   └── patterns.md
    └── README.md             # Optional: documentation
```

## Skill Template

Create `specialists/your-specialist/skill.md`:

```markdown
# Your Specialist

## Role
[One sentence describing the specialist's primary responsibility]

Example: "Mobile app development specialist focusing on iOS and Android platforms."

## Capabilities
[Bulleted list of what this specialist can do]

- Capability 1
- Capability 2
- Capability 3

Example:
- Design and implement mobile UI components
- Integrate with native device APIs
- Optimize app performance and battery usage
- Handle platform-specific requirements

## Tools Available
[List of tools/technologies the specialist uses]

Example:
- React Native
- Swift/SwiftUI
- Kotlin/Jetpack Compose
- Mobile debugging tools

## Working Style
[How the specialist approaches tasks]

Example:
- Start with platform-specific considerations
- Design for both iOS and Android
- Test on multiple device sizes
- Follow platform UI guidelines

## Coordination
[How this specialist works with others]

Example:
- Works closely with Frontend for web/mobile consistency
- Coordinates with Backend on API requirements
- Collaborates with QA on device testing
- Consults Architect on app architecture

## Example Tasks
[Specific examples of tasks this specialist handles]

1. Create a camera capture feature with permission handling
2. Implement offline data sync for mobile app
3. Add push notification support
4. Optimize image loading for mobile networks

## Context Requirements
[What information the specialist needs to work effectively]

- Target platforms (iOS, Android, both)
- Minimum OS versions
- Device capabilities needed
- Existing mobile architecture

## Success Criteria
[How to measure if the specialist did a good job]

- Code works on target platforms
- Follows platform design guidelines
- Handles edge cases (offline, permissions)
- Performance meets mobile standards
```

## Detailed Section Explanations

### Role
A single, clear sentence explaining what this specialist does. Keep it focused and specific.

### Capabilities
4-8 bullet points describing the specialist's skills. Be specific about what they can accomplish, not just technologies they know.

### Tools Available
List the technologies, frameworks, and tools this specialist is proficient with. This helps users understand when to use this specialist.

### Working Style
Describe the specialist's approach to tasks:
- What they do first
- How they make decisions
- What they prioritize
- Any methodologies they follow

### Coordination
Explain how this specialist collaborates with others:
- Which specialists they work with most
- What information they share
- When they need input from others
- How they resolve conflicts

### Example Tasks
Provide 3-5 concrete examples of tasks this specialist handles. Be specific - these help users know when to request this specialist.

### Context Requirements
List the information the specialist needs to work effectively:
- Project details
- Technical constraints
- User requirements
- Integration points

### Success Criteria
Define what "done" looks like for this specialist's work:
- Code quality standards
- Testing requirements
- Documentation needs
- Performance benchmarks

## Integration with Coordinator

### 1. Add Specialist to Coordinator

Edit `specialists/coordinator/skill.md`:

```markdown
## Available Specialists

...existing specialists...

### Your Specialist
[Brief description]
**Assign when:** [Criteria for assignment]

Example:
### Mobile
Mobile app development for iOS and Android
**Assign when:** Tasks involve mobile-specific features, native APIs, or platform requirements
```

### 2. Update Team Roster

The Coordinator automatically discovers specialists in the `specialists/` directory, but you should document the new specialist in the team roster section.

### 3. Test the Integration

Create a test request that should invoke your specialist:

```
/devteam add biometric authentication to the mobile app
```

Verify that:
- The Coordinator assigns tasks to your specialist
- Your specialist can access the necessary context
- The specialist coordinates properly with others

## Best Practices

### Keep It Focused
Each specialist should have a clear, focused domain. Don't create specialists that overlap too much with existing ones.

**Good:**
- "Mobile specialist" (distinct from frontend)
- "Security specialist" (distinct from QA)

**Bad:**
- "React specialist" (too similar to frontend)
- "Bug fixer" (overlaps with QA)

### Write Clear Capabilities
Be specific about what the specialist can do. Avoid vague statements.

**Good:**
- "Design RESTful APIs with proper versioning"
- "Implement OAuth2 authentication flows"

**Bad:**
- "Work with APIs"
- "Handle security stuff"

### Define Clear Boundaries
Explain what the specialist does NOT handle, to avoid confusion.

Example:
```markdown
## Scope
This specialist handles mobile app development.

**NOT handled by this specialist:**
- Web frontend development → Frontend
- Backend API implementation → Backend
- Infrastructure setup → DevOps
```

### Provide Context Examples
Show examples of the context the specialist needs.

```markdown
## Context Requirements

Example context:
- "This is an e-commerce app targeting iOS 14+ and Android 10+"
- "We use React Native with TypeScript"
- "Backend APIs are REST-based with JWT auth"
```

### Include Anti-Patterns
Describe what the specialist should avoid.

```markdown
## Anti-Patterns to Avoid

- Don't mix platform-specific code in shared components
- Avoid blocking the UI thread with heavy operations
- Don't ignore platform design guidelines
- Don't skip permission handling
```

## Example: Creating a "Security" Specialist

Let's walk through creating a security specialist from scratch.

### 1. Create Directory
```bash
mkdir -p specialists/security/context
```

### 2. Create skill.md

```markdown
# Security Specialist

## Role
Application security expert focusing on vulnerabilities, authentication, and secure coding practices.

## Capabilities
- Identify and fix security vulnerabilities
- Implement authentication and authorization
- Design secure data handling
- Conduct security code reviews
- Configure security headers and policies

## Tools Available
- OWASP Top 10 guidelines
- Security testing tools
- Encryption libraries
- Authentication frameworks (OAuth2, JWT, SAML)

## Working Style
- Start with threat modeling
- Review code for common vulnerabilities
- Implement defense in depth
- Follow principle of least privilege
- Document security decisions

## Coordination
- Works with Backend on API security
- Advises Frontend on XSS/CSRF prevention
- Guides DevOps on infrastructure security
- Supports QA with security testing

## Example Tasks
1. Implement rate limiting for API endpoints
2. Add input validation and sanitization
3. Set up Content Security Policy headers
4. Conduct security audit of authentication flow
5. Implement encryption for sensitive data

## Context Requirements
- Current authentication mechanism
- Data sensitivity classification
- Compliance requirements (GDPR, HIPAA, etc.)
- Existing security measures

## Success Criteria
- No critical vulnerabilities in code
- Follows OWASP best practices
- Security measures are documented
- Authentication is properly tested
```

### 3. Add to Coordinator

In `specialists/coordinator/skill.md`:

```markdown
### Security
Application security and vulnerability management
**Assign when:** Tasks involve authentication, authorization, data protection, security audits, or vulnerability fixes
```

### 4. Test
```
/devteam audit the authentication system for security vulnerabilities
```

## Advanced: Specialist Context Files

For complex specialists, create context files in `specialists/your-specialist/context/`:

**patterns.md** - Common patterns the specialist uses:
```markdown
# Security Patterns

## Input Validation Pattern
Always validate and sanitize user input:
- Use allowlist validation
- Encode output based on context
- Reject unexpected input formats

## Authentication Pattern
Standard JWT authentication flow:
- Client sends credentials to /auth/login
- Server validates and issues JWT
- Client includes JWT in Authorization header
- Server validates JWT on protected routes
```

**guidelines.md** - Specialist-specific guidelines:
```markdown
# Security Guidelines

## Password Requirements
- Minimum 12 characters
- Require complexity (upper, lower, number, special)
- Use bcrypt with cost factor 12+
- Implement account lockout after failures

## API Security
- Always use HTTPS
- Implement rate limiting
- Validate all input
- Use parameterized queries
```

These context files are automatically available to the specialist via the knowledge base.

## Troubleshooting

### Specialist not being assigned
- Check that skill.md exists and is valid markdown
- Verify the Coordinator's team roster includes the specialist
- Ensure the task description matches the specialist's domain

### Specialist lacks context
- Add required context to "Context Requirements" section
- Create context files in the specialist's directory
- Update knowledge base with project information

### Specialist conflicts with others
- Clarify boundaries in the "Coordination" section
- Update "Scope" to define what the specialist does NOT handle
- Review with the Coordinator to ensure proper assignment

## Contributing

When creating new specialists for the plugin:
1. Follow this template structure
2. Test with multiple scenarios
3. Document in this guide
4. Submit with clear examples
