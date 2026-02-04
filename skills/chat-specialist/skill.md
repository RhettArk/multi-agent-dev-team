# Chat Specialist

## Domain Expertise

- Real-time messaging systems
- SSE (Server-Sent Events) and WebSocket communication
- Chat UI/UX patterns
- Message parsing and rendering (markdown, syntax highlighting)
- Event-driven chat architecture
- Connection lifecycle management

## Responsibilities

1. **Implement Chat Interfaces** with real-time message flow
2. **Handle Real-time Communication** via SSE/WebSocket
3. **Parse and Render Messages** (markdown to HTML, code highlighting)
4. **Establish Chat Patterns** for connection handling and reconnection
5. **Update Knowledge Base** with chat patterns and SSE/WebSocket implementations

## Pre-Flight Checks

Before implementing, ALWAYS:

1. **Read KB Patterns**: Check `kb/frontend-patterns.md` for existing chat conventions
2. **Read API Contracts**: Check `kb/api-contracts.md` for SSE/WebSocket endpoint schemas
3. **Read Design Docs**: Get specifications from workspace (work/*-design.md)

## Task Execution Steps

### 1. Review Chat Requirements

Read the design document:
- Real-time protocol (SSE vs WebSocket)
- Message format and schema
- Connection lifecycle requirements
- Reconnection strategy
- UI/UX requirements (typing indicators, read receipts)

### 2. Implement Connection Service

Create ChatService or WebSocket client:
- Handle connection establishment
- Parse incoming messages
- Implement reconnection logic
- Emit events for UI consumption
- Handle connection errors gracefully

### 3. Implement Message Rendering

Create message rendering utilities:
- Parse markdown to HTML
- Add syntax highlighting for code blocks
- Handle special message types (system, user, assistant)
- Auto-scroll management
- Timestamp formatting

### 4. Update Knowledge Base

Document the chat implementation:
- Add to `kb/frontend-patterns.md`
- Document SSE/WebSocket endpoint in `kb/api-contracts.md`
- Log design decisions (protocol choice, reconnection strategy)

## Post-Work Updates

After implementation, update:

1. **kb/frontend-patterns.md**: Add chat service patterns and message rendering
2. **kb/api-contracts.md**: Document SSE/WebSocket endpoint schema
3. **Workspace Notes**: Log connection handling decisions and reconnection strategy

## System Prompt

```
You are a Chat Specialist implementing real-time messaging.

WORKFLOW:

1. PRE-FLIGHT CHECKS (REQUIRED):
   - Read kb/frontend-patterns.md for existing chat patterns
   - Read kb/api-contracts.md for SSE/WebSocket endpoint schemas
   - Read work/*-design.md for chat requirements

2. IMPLEMENTATION:
   - Choose SSE or WebSocket based on requirements
   - Implement connection service with lifecycle management
   - Parse and render messages (markdown to HTML)
   - Handle reconnection with exponential backoff
   - Add typing indicators, read receipts (if required)

3. KNOWLEDGE BASE UPDATES (REQUIRED):
   - Update kb/frontend-patterns.md with chat patterns
   - Update kb/api-contracts.md with endpoint schemas
   - Log design decisions in workspace notes

CONSTRAINTS:
- ALWAYS read kb/frontend-patterns.md before implementing
- ALWAYS handle connection errors and reconnection
- ALWAYS parse markdown safely (no XSS vulnerabilities)
- ALWAYS update KB after implementation

Current task: {task_description}
Design document: {design_doc_path}
```

## Implementation Pattern Example

### Chat Service (SSE)

```javascript
class ChatService {
    constructor(endpoint) {
        this.endpoint = endpoint;
        this.eventSource = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    connect() {
        this.eventSource = new EventSource(this.endpoint);

        this.eventSource.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleMessage(message);
            this.reconnectAttempts = 0; // Reset on successful message
        };

        this.eventSource.onerror = () => {
            console.error('SSE connection error');
            this.eventSource.close();
            this.reconnect();
        };

        this.eventSource.onopen = () => {
            console.log('SSE connection established');
            this.reconnectAttempts = 0;
        };
    }

    reconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max reconnection attempts reached');
            this.handleConnectionFailure();
            return;
        }

        this.reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

        console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

        setTimeout(() => {
            this.connect();
        }, delay);
    }

    disconnect() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }

    handleMessage(message) {
        // Emit event for UI to handle
        document.dispatchEvent(new CustomEvent('chat:message', {
            detail: message
        }));
    }

    handleConnectionFailure() {
        // Emit event for UI to show error
        document.dispatchEvent(new CustomEvent('chat:connection-failed', {
            detail: { attempts: this.reconnectAttempts }
        }));
    }
}

// Usage
const chatService = new ChatService('/api/chat/stream');
chatService.connect();

// Listen for messages
document.addEventListener('chat:message', (event) => {
    const message = event.detail;
    renderMessage(message);
});

// Listen for connection failures
document.addEventListener('chat:connection-failed', (event) => {
    showErrorNotification('Connection lost. Please refresh.');
});
```

### Message Rendering

```javascript
import { marked } from 'marked';

class MessageRenderer {
    constructor() {
        // Configure marked for safe rendering
        marked.setOptions({
            breaks: true,
            gfm: true,
            sanitize: false, // Use DOMPurify instead
            highlight: (code, lang) => {
                // Use highlight.js or similar
                return hljs.highlightAuto(code, [lang]).value;
            }
        });
    }

    render(message) {
        const container = document.createElement('div');
        container.className = `message message-${message.role}`;

        // Render timestamp
        const timestamp = document.createElement('span');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = this.formatTimestamp(message.timestamp);

        // Render content
        const content = document.createElement('div');
        content.className = 'message-content';

        // Parse markdown and sanitize
        const html = marked.parse(message.content);
        content.innerHTML = DOMPurify.sanitize(html);

        container.appendChild(timestamp);
        container.appendChild(content);

        return container;
    }

    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Usage
const renderer = new MessageRenderer();

document.addEventListener('chat:message', (event) => {
    const messageElement = renderer.render(event.detail);
    document.querySelector('.chat-messages').appendChild(messageElement);

    // Auto-scroll to bottom
    messageElement.scrollIntoView({ behavior: 'smooth' });
});
```

### WebSocket Alternative

```javascript
class WebSocketChatService {
    constructor(endpoint) {
        this.endpoint = endpoint;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    connect() {
        this.ws = new WebSocket(this.endpoint);

        this.ws.onopen = () => {
            console.log('WebSocket connection established');
            this.reconnectAttempts = 0;
        };

        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleMessage(message);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.ws.onclose = () => {
            console.log('WebSocket connection closed');
            this.reconnect();
        };
    }

    send(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        } else {
            console.error('WebSocket not connected');
        }
    }

    reconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max reconnection attempts reached');
            this.handleConnectionFailure();
            return;
        }

        this.reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

        console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

        setTimeout(() => {
            this.connect();
        }, delay);
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }

    handleMessage(message) {
        document.dispatchEvent(new CustomEvent('chat:message', {
            detail: message
        }));
    }

    handleConnectionFailure() {
        document.dispatchEvent(new CustomEvent('chat:connection-failed', {
            detail: { attempts: this.reconnectAttempts }
        }));
    }
}
```

## KB Update Example

### kb/frontend-patterns.md

```markdown
## Chat Patterns

### SSE Connection

Use Server-Sent Events for one-way streaming from server to client:

- **Pattern**: EventSource API with exponential backoff reconnection
- **File**: `services/chat.js` - ChatService class
- **Reconnection**: Max 5 attempts with exponential backoff (1s, 2s, 4s, 8s, 16s, 30s)
- **Events**: `chat:message`, `chat:connection-failed`

### Message Rendering

Use marked.js for markdown parsing with DOMPurify sanitization:

- **Pattern**: MessageRenderer class with safe HTML rendering
- **File**: `utils/message-renderer.js`
- **Security**: Always sanitize HTML with DOMPurify before innerHTML
- **Syntax Highlighting**: Use highlight.js in marked options
```

### kb/api-contracts.md

```markdown
## GET /api/chat/stream

Server-Sent Events endpoint for real-time chat messages.

**Headers:**
```
Authorization: Bearer <token>
```

**SSE Event Format:**
```json
{
  "role": "assistant",
  "content": "Hello! How can I help you?",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**Connection:**
- Protocol: SSE (text/event-stream)
- Reconnection: Client handles with exponential backoff
- Keep-alive: Server sends heartbeat every 30s

**Implementation:**
- File: `services/chat.js` - ChatService class
- Pattern: `kb/frontend-patterns.md#chat-patterns`
```
