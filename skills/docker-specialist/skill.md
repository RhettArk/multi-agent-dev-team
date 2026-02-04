# Docker Specialist

## Domain Expertise

- Docker containerization and multi-stage builds
- Docker Compose orchestration
- Volume management and networking
- Container optimization (image size, layer caching)
- Deployment configurations

## Responsibilities

1. **Containerize Applications** with Dockerfile
2. **Create Docker Compose** configurations for multi-service setups
3. **Optimize Container Images** for size and build performance
4. **Document Container Patterns** and best practices
5. **Update Knowledge Base** with Docker patterns in `kb/docker-patterns.md`

## Pre-Flight Checks

Before containerizing, ALWAYS:

1. **Read KB Patterns**: Check `kb/docker-patterns.md` for existing container patterns
2. **Read Backend Patterns**: Check `kb/backend-patterns.md` to understand app requirements
3. **Check Decision Log**: Review for Docker-related precedent and choices

## Task Execution Steps

### 1. Analyze Application Requirements

Review the application to understand:
- Runtime dependencies (Python, Node.js, etc.)
- Port requirements
- Environment variables
- Volume/persistence needs
- External service dependencies

### 2. Create Dockerfile with Multi-Stage Build

Design efficient Dockerfile:
- Use multi-stage builds to minimize final image size
- Choose appropriate base images (Alpine for production)
- Optimize layer caching
- Use .dockerignore to exclude unnecessary files

### 3. Create Docker Compose (if needed)

For multi-service applications:
- Define services and dependencies
- Configure networking
- Set up volumes for persistence
- Define environment variables

### 4. Optimize Image Size and Build Caching

Apply optimization techniques:
- Use Alpine-based images
- Combine RUN commands to reduce layers
- Order Dockerfile commands for better caching
- Remove build artifacts in same layer

### 5. Document Patterns

Update knowledge base:
- Add new patterns to `kb/docker-patterns.md`
- Document configuration choices
- Log decisions in decision log

## Post-Work Updates

After containerization, update:

1. **kb/docker-patterns.md**: Document container patterns used
2. **Decision Log**: Log base image choice, port mappings, optimization decisions
3. **Deployment Docs**: Add container deployment instructions

## System Prompt

```
You are a Docker Specialist responsible for containerizing applications.

WORKFLOW:

1. PRE-FLIGHT CHECKS (REQUIRED):
   - Read kb/docker-patterns.md for current container patterns
   - Read kb/backend-patterns.md to understand app requirements
   - Check decision log for Docker-related precedent

2. CONTAINERIZATION:
   - Analyze application dependencies and runtime requirements
   - Create Dockerfile with multi-stage build pattern
   - Create docker-compose.yml if multi-service setup needed
   - Create .dockerignore to exclude unnecessary files
   - Optimize image size using Alpine base and layer caching

3. KNOWLEDGE BASE UPDATES (REQUIRED):
   - Update kb/docker-patterns.md with new container patterns
   - Log decisions (base image choice, port mappings, optimization techniques)
   - Document deployment configuration

CONSTRAINTS:
- ALWAYS use multi-stage builds to minimize image size
- ALWAYS create .dockerignore file
- ALWAYS use Alpine-based images for production
- ALWAYS update KB after containerization

Current task: {task_description}
```

## Dockerfile Pattern (Multi-Stage Build)

### Python FastAPI Application Example

```dockerfile
# Build stage - install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage - minimal final image
FROM python:3.11-alpine

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Ensure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Expose application port
EXPOSE 8000

# Run as non-root user
RUN adduser -D appuser
USER appuser

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Node.js Application Example

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy application code
COPY . .

# Expose application port
EXPOSE 3000

# Run as non-root user
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

# Start application
CMD ["node", "server.js"]
```

## Docker Compose Pattern

### Multi-Service Application Example

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

## .dockerignore Pattern

```
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docs
*.md
docs/

# Tests
tests/
*.test.js
*.spec.js

# Environment
.env
.env.local
*.local
```

## Container Optimization Techniques

### 1. Multi-Stage Builds
- Use separate build and runtime stages
- Copy only necessary artifacts to final image
- Reduces final image size by 50-80%

### 2. Alpine Base Images
- Use Alpine Linux for minimal footprint
- 5-10x smaller than standard images
- Trade-off: may need additional packages for compatibility

### 3. Layer Caching
- Order commands from least to most frequently changed
- Copy dependency files before application code
- Speeds up rebuilds significantly

### 4. Combine RUN Commands
- Chain commands with && to reduce layers
- Clean up in same layer to reduce size
- Example: `RUN apt-get update && apt-get install -y pkg && rm -rf /var/lib/apt/lists/*`

### 5. Use .dockerignore
- Exclude unnecessary files from build context
- Reduces build time and image size
- Similar to .gitignore syntax

### 6. Non-Root User
- Always run containers as non-root for security
- Create dedicated user in Dockerfile
- Use USER directive to switch

## Common Patterns

### Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

### Build Arguments

```dockerfile
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-alpine

ARG ENV=production
ENV ENVIRONMENT=${ENV}
```

### Volume Management

```dockerfile
# Create volume mount point
VOLUME ["/app/data"]

# Or in docker-compose.yml
volumes:
  - ./local-data:/app/data
  - app-cache:/app/cache
```

### Network Configuration

```yaml
# docker-compose.yml
networks:
  frontend:
  backend:

services:
  web:
    networks:
      - frontend
  api:
    networks:
      - frontend
      - backend
  db:
    networks:
      - backend
```
