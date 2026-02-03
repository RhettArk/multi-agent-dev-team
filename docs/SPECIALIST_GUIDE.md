# Specialist Guide

## Creating a New Specialist

This guide shows you how to create a custom specialist agent for the Multi-Agent Dev Team plugin.

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
