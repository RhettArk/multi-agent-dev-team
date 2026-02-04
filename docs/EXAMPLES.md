# Multi-Agent Dev Team - Real-World Examples

## Example 1: Adding a New API Endpoint

### Scenario
You need to add a new `/api/v1/users/{user_id}/profile` endpoint to retrieve and update user profiles.

### Request
```
/dev-team "Add user profile API endpoint with GET and PUT methods"
```

### Phase 1: Pre-Planning Cleanup

**Code Reviewer Output:**
```
Found 2 issues:
1. Unused import in backend/routers/users.py: from typing import Dict
2. Dead function in backend/services/user_service.py: get_legacy_user()

[Approve cleanup?]
```

**User:** Approved

---

### Phase 2: Auto-Planning

**Auto-Planner Consultation:**
1. **Backend Architect** consulted:
   - "What architecture patterns should we follow?"
   - Response: "Use router → service → database pattern"

2. **Backend Design** consulted:
   - "What schemas do we need?"
   - Response: "ProfileResponse, ProfileUpdate models"

3. **FastAPI Specialist** consulted:
   - "What route structure?"
   - Response: "GET and PUT under /users router"

4. **Code Reviewer** consulted:
   - "Any concerns?"
   - Response: "Ensure input validation on PUT"

**Generated Plan:**
```
Task 1: Design profile endpoint architecture [Backend Architect]
  Description: Define router → service → database flow for profile endpoint
  Dependencies: none

Task 2: Design profile schemas [Backend Design]
  Description: Create ProfileResponse and ProfileUpdate Pydantic models
  Dependencies: Task 1

Task 3: Implement profile service [FastAPI Specialist]
  Description: Add get_profile() and update_profile() to user_service.py
  Dependencies: Task 2

Task 4: Implement profile routes [FastAPI Specialist]
  Description: Add GET and PUT routes to users router
  Dependencies: Task 3

Task 5: Review and simplify [Code Reviewer]
  Description: Review implementation for simplifications and best practices
  Dependencies: Task 4

Scope:
  Change: backend/routers/users.py, backend/services/user_service.py, backend/models/requests.py
  Preserve: Existing user authentication, all other routers

[Approve plan?]
```

**User:** Approved

---

### Phase 3: Parallel Execution

**Task 1: Backend Architect**
```
Status: in_progress
---
Created: work/profile-architecture.md

## Profile Endpoint Architecture

Router: backend/routers/users.py
Service: backend/services/user_service.py
Database: users table (existing)

Flow:
1. Router validates JWT and user_id
2. Router calls service layer
3. Service queries database
4. Service returns Pydantic model
5. Router returns JSON response

Patterns:
- Use existing auth middleware
- Reuse db connection from dependency injection
- Follow error handling pattern from other endpoints
---

Checkpoint: PASS
- Validated architecture follows existing patterns
- KB synced: Updated backend-patterns.md
- Peer review: Backend Design approved
```

**Task 2: Backend Design** (runs after Task 1)
```
Status: in_progress
---
Created: backend/models/responses.py (updated)

class ProfileResponse(BaseModel):
    user_id: UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime
    updated_at: datetime

Created: backend/models/requests.py (updated)

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

    @validator('avatar_url')
    def validate_avatar_url(cls, v):
        if v and not v.startswith(('https://', 'http://')):
            raise ValueError('Avatar URL must be HTTPS')
        return v
---

Checkpoint: PASS
- Validated schemas follow Pydantic v2 conventions
- KB synced: Updated api-contracts.md with new schemas
- Peer review: Backend Architect confirmed matches design
```

**Task 3: FastAPI Specialist** (runs after Task 2)
```
Status: in_progress
---
Updated: backend/services/user_service.py

async def get_profile(user_id: UUID) -> ProfileResponse:
    """Get user profile by ID."""
    user = await db.query(
        "SELECT * FROM users WHERE user_id = $1",
        user_id
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ProfileResponse(**user)

async def update_profile(
    user_id: UUID,
    profile_update: ProfileUpdate
) -> ProfileResponse:
    """Update user profile."""
    update_data = profile_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    user = await db.query(
        """
        UPDATE users SET
            first_name = COALESCE($2, first_name),
            last_name = COALESCE($3, last_name),
            avatar_url = COALESCE($4, avatar_url),
            updated_at = NOW()
        WHERE user_id = $1
        RETURNING *
        """,
        user_id,
        update_data.get('first_name'),
        update_data.get('last_name'),
        update_data.get('avatar_url')
    )
    return ProfileResponse(**user)
---

Checkpoint: PASS
- Syntax validation: PASS
- Import validation: PASS
- KB synced: Logged decision "Use COALESCE for optional updates"
- Peer review: Backend Design confirmed schemas used correctly
```

**Task 4: FastAPI Specialist** (runs after Task 3)
```
Status: in_progress
---
Updated: backend/routers/users.py

@router.get("/users/{user_id}/profile", response_model=ProfileResponse)
async def get_user_profile(
    user_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """
    Get user profile.

    Requires authentication. Users can only access their own profile
    unless they have admin role.
    """
    if current_user.user_id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    return await user_service.get_profile(user_id)


@router.put("/users/{user_id}/profile", response_model=ProfileResponse)
async def update_user_profile(
    user_id: UUID,
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update user profile.

    Requires authentication. Users can only update their own profile.
    """
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return await user_service.update_profile(user_id, profile_update)
---

Checkpoint: PASS
- Syntax validation: PASS
- Structure validation: PASS (both GET and PUT present)
- KB synced: Updated api-contracts.md with route details
- Dependencies updated: Added routes to dependencies.json
- Peer review: Backend Architect confirmed follows architecture
```

**Task 5: Code Reviewer** (runs after Task 4)
```
Status: in_progress
---
Review findings:

Simplifications made:
1. Removed redundant type hints (already in Pydantic models)
2. Combined permission checks into decorator
3. Added docstrings for API documentation

Updated: backend/routers/users.py

# Added permission decorator
def require_self_or_admin(user_id: UUID, current_user: User):
    if current_user.user_id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

@router.get("/users/{user_id}/profile", response_model=ProfileResponse)
async def get_user_profile(
    user_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Get user profile. Requires authentication."""
    require_self_or_admin(user_id, current_user)
    return await user_service.get_profile(user_id)

# Similar for PUT endpoint

Updated: backend/services/user_service.py

# Simplified error handling
async def get_profile(user_id: UUID) -> ProfileResponse:
    """Get user profile by ID."""
    user = await db.query(
        "SELECT * FROM users WHERE user_id = $1",
        user_id
    )
    if not user:
        raise HTTPException(404, "User not found")  # Simplified
    return ProfileResponse(**user)
---

Checkpoint: PASS
- Reviewed all changes
- Applied simplifications
- KB synced: Added pattern "Use permission decorators for auth checks"
- All tests passing
```

---

### Phase 4: Completion

**Summary:**
```
✓ All tasks completed successfully

Changes made:
- Created: work/profile-architecture.md
- Updated: backend/models/responses.py (added ProfileResponse)
- Updated: backend/models/requests.py (added ProfileUpdate)
- Updated: backend/services/user_service.py (added get_profile, update_profile)
- Updated: backend/routers/users.py (added GET and PUT routes)

KB updates:
- backend-patterns.md: Added permission decorator pattern
- api-contracts.md: Added ProfileResponse, ProfileUpdate schemas
- decisions.log: 3 decisions logged
- dependencies.json: Added route → service dependencies

Ready to test:
- GET /api/v1/users/{user_id}/profile
- PUT /api/v1/users/{user_id}/profile

[Clean up workspace files?]
```

**User:** Yes

**Cleanup Complete**

---

## Example 2: Creating a New UI Component

### Scenario
Create a reusable notification toast component for the frontend.

### Request
```
/dev-team "Create a notification toast component with success, error, and info variants"
```

### Phase 1: Pre-Planning Cleanup

**Code Reviewer Output:**
```
Found 1 issue:
1. Unused component in frontend/components/alerts/Alert.js (legacy)

[Approve cleanup?]
```

**User:** Approved, removed Alert.js

---

### Phase 2: Auto-Planning

**Generated Plan:**
```
Task 1: Design toast component UX [UI/UX Specialist]
  Description: Design toast appearance, animations, positioning
  Dependencies: none

Task 2: Design component API [JavaScript Specialist]
  Description: Define component interface and usage patterns
  Dependencies: Task 1

Task 3: Implement toast component [JavaScript Specialist]
  Description: Create Toast.js with variants and animations
  Dependencies: Task 2

Task 4: Implement toast service [JavaScript Specialist]
  Description: Create toast.js service for showing/hiding toasts
  Dependencies: Task 3

Task 5: Refactor and simplify [Code Quality (Frontend)]
  Description: Simplify component logic and improve maintainability
  Dependencies: Task 4

Scope:
  Change: frontend/components/toast/, frontend/services/toast.js
  Preserve: Existing notification patterns (can be migrated later)

[Approve plan?]
```

**User:** Approved

---

### Phase 3: Parallel Execution

**Task 1: UI/UX Specialist**
```
Status: completed
---
Created: work/toast-design.md

## Toast Component Design

Variants:
- Success: Green background, checkmark icon
- Error: Red background, X icon
- Info: Blue background, info icon

Position: Top-right corner, 16px from edge
Animation: Slide in from right, fade out after 3s
Stacking: Multiple toasts stack vertically with 8px gap

Accessibility:
- role="alert" for screen readers
- Dismiss button with aria-label
- Keyboard accessible (Esc to dismiss)

CSS Variables:
--toast-success-bg: #10b981
--toast-error-bg: #ef4444
--toast-info-bg: #3b82f6
---

Checkpoint: PASS
```

**Task 2: JavaScript Specialist** (runs after Task 1)
```
Status: completed
---
Created: work/toast-api.md

## Toast Component API

Component Props:
- message: string (required)
- variant: 'success' | 'error' | 'info' (required)
- duration: number (default 3000ms)
- onDismiss: () => void (optional)

Service API:
- toast.success(message, options)
- toast.error(message, options)
- toast.info(message, options)
- toast.dismiss(toastId)

Usage:
import { toast } from './services/toast.js';

toast.success('Profile updated');
toast.error('Failed to save', { duration: 5000 });
---

Checkpoint: PASS
```

**Task 3: JavaScript Specialist** (runs after Task 2)
```
Status: completed
---
Created: frontend/components/toast/Toast.js

import { createElement } from '../../utils/dom.js';

export class Toast {
  constructor(message, variant, options = {}) {
    this.message = message;
    this.variant = variant;
    this.duration = options.duration || 3000;
    this.onDismiss = options.onDismiss;
    this.element = this.render();
    this.timeoutId = null;
  }

  render() {
    const toast = createElement('div', {
      className: `toast toast--${this.variant}`,
      role: 'alert',
      'aria-live': 'polite'
    });

    const icon = this.getIcon();
    const messageEl = createElement('span', {
      className: 'toast__message',
      textContent: this.message
    });

    const dismissBtn = createElement('button', {
      className: 'toast__dismiss',
      'aria-label': 'Dismiss notification',
      onclick: () => this.dismiss()
    }, '×');

    toast.appendChild(icon);
    toast.appendChild(messageEl);
    toast.appendChild(dismissBtn);

    return toast;
  }

  getIcon() {
    const icons = {
      success: '✓',
      error: '✕',
      info: 'ℹ'
    };
    return createElement('span', {
      className: 'toast__icon',
      textContent: icons[this.variant]
    });
  }

  show(container) {
    container.appendChild(this.element);

    // Trigger animation
    requestAnimationFrame(() => {
      this.element.classList.add('toast--visible');
    });

    // Auto-dismiss
    if (this.duration > 0) {
      this.timeoutId = setTimeout(() => {
        this.dismiss();
      }, this.duration);
    }
  }

  dismiss() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }

    this.element.classList.remove('toast--visible');
    this.element.addEventListener('transitionend', () => {
      this.element.remove();
      if (this.onDismiss) {
        this.onDismiss();
      }
    }, { once: true });
  }
}

Created: frontend/components/toast/toast.css

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 300px;
  max-width: 500px;
  opacity: 0;
  transform: translateX(100%);
  transition: opacity 0.3s, transform 0.3s;
}

.toast--visible {
  opacity: 1;
  transform: translateX(0);
}

.toast--success {
  background: var(--toast-success-bg);
  color: white;
}

.toast--error {
  background: var(--toast-error-bg);
  color: white;
}

.toast--info {
  background: var(--toast-info-bg);
  color: white;
}

.toast__icon {
  font-size: 20px;
  font-weight: bold;
}

.toast__message {
  flex: 1;
}

.toast__dismiss {
  background: none;
  border: none;
  color: inherit;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  line-height: 1;
}

.toast__dismiss:hover {
  opacity: 0.7;
}
---

Checkpoint: PASS
```

**Task 4: JavaScript Specialist** (runs after Task 3)
```
Status: completed
---
Created: frontend/services/toast.js

import { Toast } from '../components/toast/Toast.js';

class ToastService {
  constructor() {
    this.container = null;
    this.toasts = new Map();
    this.nextId = 0;
  }

  init() {
    this.container = document.createElement('div');
    this.container.className = 'toast-container';
    document.body.appendChild(this.container);
  }

  success(message, options = {}) {
    return this.show(message, 'success', options);
  }

  error(message, options = {}) {
    return this.show(message, 'error', options);
  }

  info(message, options = {}) {
    return this.show(message, 'info', options);
  }

  show(message, variant, options = {}) {
    if (!this.container) {
      this.init();
    }

    const id = this.nextId++;
    const toast = new Toast(message, variant, {
      ...options,
      onDismiss: () => {
        this.toasts.delete(id);
        if (options.onDismiss) {
          options.onDismiss();
        }
      }
    });

    this.toasts.set(id, toast);
    toast.show(this.container);

    return id;
  }

  dismiss(id) {
    const toast = this.toasts.get(id);
    if (toast) {
      toast.dismiss();
    }
  }

  dismissAll() {
    this.toasts.forEach(toast => toast.dismiss());
  }
}

export const toast = new ToastService();

Updated: frontend/styles/components/toast.css (in imports)
---

Checkpoint: PASS
```

**Task 5: Code Quality (Frontend)** (runs after Task 4)
```
Status: completed
---
Refactoring changes:

1. Simplified icon rendering:
  getIcon() {
    const ICONS = { success: '✓', error: '✕', info: 'ℹ' };
    return createElement('span', {
      className: 'toast__icon',
      textContent: ICONS[this.variant]
    });
  }

2. Extracted animation logic:
  async show(container) {
    container.appendChild(this.element);
    await this.animate('show');
    this.scheduleAutoDismiss();
  }

  async animate(type) {
    return new Promise(resolve => {
      requestAnimationFrame(() => {
        this.element.classList.add('toast--visible');
        this.element.addEventListener('transitionend', resolve, { once: true });
      });
    });
  }

3. Added cleanup method:
  cleanup() {
    if (this.timeoutId) clearTimeout(this.timeoutId);
    this.element.remove();
    if (this.onDismiss) this.onDismiss();
  }

Applied changes to Toast.js and toast.js
---

Checkpoint: PASS
```

---

### Phase 4: Completion

**Summary:**
```
✓ All tasks completed successfully

Changes made:
- Created: frontend/components/toast/Toast.js
- Created: frontend/components/toast/toast.css
- Created: frontend/services/toast.js

Usage:
import { toast } from './services/toast.js';

// Show notifications
toast.success('Operation successful');
toast.error('An error occurred');
toast.info('New message received');

// With options
toast.success('Saved!', { duration: 5000 });

KB updates:
- frontend-patterns.md: Added toast component pattern
- decisions.log: Logged decision "Use service pattern for toast management"

[Clean up workspace files?]
```

---

## Example 3: Containerizing an Application

### Scenario
Containerize your FastAPI application for production deployment.

### Request
```
/dev-team "Containerize the FastAPI app with multi-stage builds and production config"
```

### Phase 1: Pre-Planning Cleanup

**Code Reviewer Output:**
```
No dead code found.
[Continue to planning]
```

---

### Phase 2: Auto-Planning

**Generated Plan:**
```
Task 1: Design container architecture [Docker Specialist]
  Description: Plan multi-stage Dockerfile and deployment strategy
  Dependencies: none

Task 2: Review backend requirements [FastAPI Specialist]
  Description: Identify all dependencies and environment requirements
  Dependencies: none

Task 3: Create Dockerfile [Docker Specialist]
  Description: Implement multi-stage Dockerfile
  Dependencies: Task 1, Task 2

Task 4: Create docker-compose [Docker Specialist]
  Description: Create docker-compose.yml for local development
  Dependencies: Task 3

Task 5: Review and test [Code Reviewer]
  Description: Review Docker setup and test builds
  Dependencies: Task 4

Scope:
  Create: Dockerfile, docker-compose.yml, .dockerignore
  Update: .env.example (document container env vars)
  Preserve: Existing development setup

[Approve plan?]
```

**User:** Approved

---

### Phase 3: Parallel Execution

**Tasks 1 & 2 run in parallel:**

**Task 1: Docker Specialist**
```
Status: completed
---
Created: work/container-architecture.md

## Container Architecture

Multi-stage build:
1. Builder stage: Install dependencies
2. Runtime stage: Copy artifacts, minimal image

Base images:
- Builder: python:3.11-slim
- Runtime: python:3.11-slim

Optimizations:
- Use .dockerignore
- Layer caching for dependencies
- Non-root user
- Health checks

Environment:
- Production: Gunicorn with 4 workers
- Development: Uvicorn with reload
---

Checkpoint: PASS
```

**Task 2: FastAPI Specialist**
```
Status: completed
---
Created: work/backend-requirements.md

## Backend Requirements

Python version: 3.11+

Dependencies:
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- pydantic==2.5.0
- supabase==2.0.0
- openai==1.3.0

Environment variables required:
- SUPABASE_URL
- SUPABASE_ANON_KEY
- SUPABASE_SERVICE_KEY
- OPENAI_API_KEY
- ENVIRONMENT (dev|staging|production)

Port: 8082
Health check: GET /health
---

Checkpoint: PASS
```

**Task 3: Docker Specialist** (runs after Tasks 1 & 2)
```
Status: completed
---
Created: Dockerfile

# Multi-stage build for FastAPI application
FROM python:3.11-slim as builder

WORKDIR /build

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY backend/ ./backend/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Ensure Python packages are in PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8082

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8082/health')"

# Production command (Gunicorn)
CMD ["gunicorn", "backend.main:app", \
     "--bind", "0.0.0.0:8082", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]

Created: .dockerignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# IDEs
.vscode/
.idea/

# Project
.git/
.gitignore
*.md
tests/
.pytest_cache/

# Environment
.env
.env.local

# Workspace
workspace/
kb/
---

Checkpoint: PASS
```

**Task 4: Docker Specialist** (runs after Task 3)
```
Status: completed
---
Created: docker-compose.yml

version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8082:8082"
    environment:
      - ENVIRONMENT=development
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      # Mount code for development with hot reload
      - ./backend:/app/backend
    command: >
      uvicorn backend.main:app
      --host 0.0.0.0
      --port 8082
      --reload
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8082/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s

  # Frontend service (if needed)
  # frontend:
  #   build:
  #     context: ./frontend
  #   ports:
  #     - "3000:3000"

Updated: .env.example

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_KEY=eyJxxx...

# OpenAI
OPENAI_API_KEY=sk-xxx...

# Environment
ENVIRONMENT=development

Created: README.docker.md

# Docker Setup

## Development

```bash
# Build and start
docker-compose up --build

# Access logs
docker-compose logs -f backend

# Stop
docker-compose down
```

## Production

```bash
# Build production image
docker build -t myapp:latest .

# Run production container
docker run -d \
  -p 8082:8082 \
  --env-file .env.production \
  --name myapp \
  myapp:latest

# Check health
docker exec myapp curl http://localhost:8082/health
```

## Troubleshooting

- Container fails to start: Check environment variables
- Port already in use: Change port in docker-compose.yml
- Dependencies missing: Rebuild image after updating requirements.txt
---

Checkpoint: PASS
```

**Task 5: Code Reviewer** (runs after Task 4)
```
Status: completed
---
Review findings:

Improvements made:
1. Added .dockerignore entries for node_modules
2. Optimized layer caching in Dockerfile
3. Added restart policy to docker-compose
4. Added health check timeout to compose

Updated: Dockerfile

# Optimize dependency caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy code last (changes frequently)
COPY backend/ ./backend/

Updated: docker-compose.yml

services:
  backend:
    restart: unless-stopped  # Added restart policy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8082/health || exit 1"]
      timeout: 3s  # Added explicit timeout

Tested:
✓ Docker build completes successfully
✓ Container starts and responds to health checks
✓ Hot reload works in development mode
✓ Environment variables loaded correctly
---

Checkpoint: PASS
```

---

### Phase 4: Completion

**Summary:**
```
✓ All tasks completed successfully

Changes made:
- Created: Dockerfile (multi-stage, optimized)
- Created: docker-compose.yml (development setup)
- Created: .dockerignore
- Created: README.docker.md (usage guide)
- Updated: .env.example (container variables)

Quick start:
```bash
# Development
docker-compose up --build

# Production
docker build -t myapp:latest .
docker run -d -p 8082:8082 --env-file .env.production myapp:latest
```

KB updates:
- Logged decision: "Use multi-stage builds for size optimization"
- Logged decision: "Gunicorn for production, Uvicorn for dev"
- Dependencies updated: Dockerfile → .env, requirements.txt

[Clean up workspace files?]
```

---

## Example 4: Handling Migration Failures

### Scenario
A database migration fails during execution, and the system recovers automatically.

### Request
```
/dev-team "Add created_by column to assets table"
```

### Phase 2: Auto-Planning (abbreviated)

**Generated Plan:**
```
Task 1: Design migration [Database Migration Specialist]
Task 2: Review schema impact [Backend Design]
Task 3: Update models [Backend Design]
Task 4: Test migration [Code Reviewer]

[Plan approved]
```

---

### Phase 3: Execution with Error

**Task 1: Database Migration Specialist**
```
Status: in_progress
---
Created: migrations/20260204_add_created_by.sql

ALTER TABLE assets
ADD COLUMN created_by UUID REFERENCES users(user_id);

-- Backfill existing records
UPDATE assets SET created_by = '00000000-0000-0000-0000-000000000000'
WHERE created_by IS NULL;

-- Make column NOT NULL
ALTER TABLE assets
ALTER COLUMN created_by SET NOT NULL;
---

Checkpoint: FAIL
Error: Syntax error in migration
Detail: UUID '00000000-0000-0000-0000-000000000000' does not exist in users table
```

---

### Error Recovery Process

**Coordinator:**
```
Task 1 failed: "UUID does not exist in users table"

Classifying failure...
→ Classification: FIXABLE
→ Reason: Design issue - needs clarification on backfill strategy

Attempting recovery:
→ Loop back to: Backend Architect
→ Request: "How should we handle created_by for existing assets with no user?"
```

**Backend Architect (Recovery Consultation):**
```
For existing assets without a user:

Option 1: Create a system user
Option 2: Make column nullable initially
Option 3: Use a default admin user_id

Recommendation: Option 2 (nullable)
- Keep column nullable
- Backfill as users are identified
- Avoids fake data in database

Updated: work/created-by-design.md
```

**Coordinator:**
```
Recovery plan updated.
Retrying Task 1 with clarification...
```

**Task 1: Database Migration Specialist (Retry)**
```
Status: in_progress
---
Updated: migrations/20260204_add_created_by.sql

ALTER TABLE assets
ADD COLUMN created_by UUID REFERENCES users(user_id);

-- Column remains nullable for existing records
-- Will be backfilled as users are identified

-- Add partial index for NOT NULL check on new records
CREATE INDEX idx_assets_created_by
ON assets(created_by)
WHERE created_by IS NOT NULL;

-- Add trigger to require created_by for new inserts
CREATE OR REPLACE FUNCTION require_created_by()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.created_by IS NULL THEN
    RAISE EXCEPTION 'created_by is required for new assets';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ensure_created_by
BEFORE INSERT ON assets
FOR EACH ROW
EXECUTE FUNCTION require_created_by();
---

Checkpoint: PASS
Migration executed successfully
```

**Remaining tasks continue:**

**Task 2: Backend Design**
```
Updated: backend/models/responses.py

class AssetResponse(BaseModel):
    asset_id: UUID
    name: str
    created_by: Optional[UUID] = None  # Nullable for legacy records
    # ... other fields
```

**Task 3: Backend Design**
```
Updated: backend/models/requests.py

class AssetCreate(BaseModel):
    name: str
    created_by: UUID  # Required for new assets
    # ... other fields
```

**Task 4: Code Reviewer**
```
✓ Migration reviewed
✓ Models updated correctly
✓ Trigger handles new inserts
✓ Legacy records handled gracefully

Recommendation: Add backfill script for future use
Created: scripts/backfill_created_by.sql
```

---

### Phase 4: Completion

**Summary:**
```
✓ Task completed successfully (1 recovery required)

Error handled:
- Initial failure: Invalid UUID in backfill
- Recovery: Backend Architect clarified nullable approach
- Resolution: Updated migration with trigger instead of backfill

Changes made:
- Created: migrations/20260204_add_created_by.sql
- Updated: backend/models/responses.py (nullable created_by)
- Updated: backend/models/requests.py (required for new)
- Created: scripts/backfill_created_by.sql

KB updates:
- Logged decision: "Use triggers over backfills for data integrity"
- Logged learning: "Nullable approach better for legacy data"

[Clean up workspace files?]
```

---

## Key Takeaways from Examples

### Example 1: API Endpoint
- Auto-planning consulted 4 specialists
- Generated complete, correct plan automatically
- Code Reviewer found optimization opportunities
- KB captured reusable patterns

### Example 2: UI Component
- UX design informed implementation
- Component refactored for maintainability
- Service pattern applied for state management
- All accessibility concerns addressed

### Example 3: Containerization
- Parallel consultation sped up planning
- Multi-stage builds optimized image size
- Both dev and prod configs provided
- Documentation created automatically

### Example 4: Migration Failure
- Error detected automatically
- Recovery successful without user intervention
- Architect clarified design during recovery
- Better solution emerged from error

---

## Using These Examples

### Pattern Recognition

Look for similar scenarios in your work:
- Adding endpoints → Use Example 1 pattern
- Creating components → Use Example 2 pattern
- Deployment setup → Use Example 3 pattern
- Database changes → Use Example 4 pattern

### Customization

Adapt requests to your needs:
```
# Based on Example 1
/dev-team "Add POST /api/v1/comments endpoint with validation"

# Based on Example 2
/dev-team "Create modal dialog component with backdrop and animations"

# Based on Example 3
/dev-team "Add Redis caching layer to docker-compose"

# Based on Example 4
/dev-team "Add indexes to improve query performance"
```

### Learning from Failures

Example 4 shows error recovery in action:
- System classified error correctly
- Looped back to architect automatically
- Found better solution through recovery
- User only saw final success

This happens automatically - you don't need to manually retry or debug.
