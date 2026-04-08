# API Documentation

## Multi-Agent Productivity Assistant API

Base URL: `https://your-service-url` or `http://localhost:8000`

---

## Endpoints

### GET /

Get API information and available endpoints.

**Response:**
```json
{
  "name": "Multi-Agent Productivity Assistant",
  "version": "1.0.0",
  "description": "AI-powered task, calendar, and notes management system",
  "author": "Nutakki Chandra Sekhara Krishna Akash",
  "endpoints": {
    "health": "/health",
    "execute": "/execute (POST)",
    "status": "/status",
    "docs": "/docs"
  }
}
```

---

### GET /health

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-04-07T12:00:00.000Z"
}
```

**Status Codes:**
- 200: Service healthy
- 503: Service unhealthy

---

### GET /status

Get system status and statistics.

**Response:**
```json
{
  "success": true,
  "coordinator": "Coordinator",
  "agents": {
    "task": "TaskAgent",
    "calendar": "CalendarAgent",
    "notes": "NotesAgent"
  },
  "task_count": 10,
  "event_count": 5,
  "note_count": 15
}
```

---

### POST /execute

Execute a natural language command through the multi-agent system.

**Request Body:**
```json
{
  "command": "string"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Command executed successfully",
  "data": {
    "success": true,
    "message": "Task created successfully",
    "task": {
      "id": 1,
      "title": "Complete project report",
      "status": "pending",
      "priority": "high",
      "created_at": "2024-04-07T12:00:00",
      "updated_at": "2024-04-07T12:00:00"
    }
  },
  "agent": "TaskAgent"
}
```

**Status Codes:**
- 200: Command executed successfully
- 500: Internal server error

---

### GET /help

Get help information about available commands.

**Response:**
```json
{
  "tasks": {
    "add": "add task <title> [high/low priority]",
    "list": "show tasks [pending/completed] [high/low priority]",
    "complete": "complete task <id>",
    "update": "update task <id> [to <status/priority>]",
    "delete": "delete task <id>"
  },
  "calendar": {
    "add": "add event <name> on <date> [at <time>] [at <location>]",
    "list": "show events [on <date>]",
    "update": "update event <id> [to <date>] [at <time>]",
    "delete": "delete event <id>"
  },
  "notes": {
    "add": "add note <content> [#tag1 #tag2]",
    "list": "show notes [#tag] [containing <text>]",
    "update": "update note <id> to <new content> [#tags]",
    "delete": "delete note <id>"
  },
  "multi_step": {
    "description": "Chain multiple commands together",
    "connectors": ["and", "then", "also"],
    "example": "add task prepare for meeting and schedule meeting on 2024-04-15"
  }
}
```

---

## Command Examples

### Task Management

#### Create Task
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "add task complete hackathon project high priority"}'
```

#### List Tasks
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "show tasks pending"}'
```

#### Complete Task
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "complete task 1"}'
```

#### Update Task
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "update task 1 to high priority"}'
```

#### Delete Task
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "delete task 1"}'
```

---

### Calendar Management

#### Add Event
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "add event team standup on 2024-04-15 at 10:00 AM"}'
```

#### List Events
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "show events on 2024-04-15"}'
```

#### Update Event
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "update event 1 to 2024-04-20 at 2:00 PM"}'
```

#### Delete Event
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "delete event 1"}'
```

---

### Notes Management

#### Add Note
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "add note buy groceries tomorrow #shopping #personal"}'
```

#### List Notes
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "show notes #shopping"}'
```

#### Search Notes
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "show notes containing groceries"}'
```

#### Update Note
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "update note 1 to buy groceries and milk #shopping"}'
```

#### Delete Note
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "delete note 1"}'
```

---

### Multi-Step Workflows

#### Chain Multiple Commands
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "add task prepare presentation and schedule review meeting on 2024-04-20 and add note presentation topics #work"}'
```

**Response:**
```json
{
  "status": "success",
  "message": "Executed 3 step(s) successfully",
  "data": {
    "success": true,
    "workflow": true,
    "steps": [
      {
        "command": "add task prepare presentation",
        "result": {
          "success": true,
          "message": "Task created successfully",
          "task": {...}
        }
      },
      {
        "command": "schedule review meeting on 2024-04-20",
        "result": {
          "success": true,
          "message": "Event added successfully",
          "event": {...}
        }
      },
      {
        "command": "add note presentation topics #work",
        "result": {
          "success": true,
          "message": "Note added successfully",
          "note": {...}
        }
      }
    ]
  },
  "agent": "Coordinator"
}
```

---

## Error Handling

All endpoints return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Error Codes:**
- 400: Bad Request - Invalid command format
- 404: Not Found - Resource not found
- 500: Internal Server Error - Server-side error

---

## Rate Limiting

Currently, there are no rate limits implemented. For production deployment, consider adding rate limiting using middleware.

---

## Authentication

The current version does not require authentication. For production use, implement token-based authentication:

```python
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}
```

---

## WebSocket Support (Future)

Real-time updates via WebSocket will be available in a future release:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
    console.log('Update:', JSON.parse(event.data));
};
```

---

## SDK Examples

### Python
```python
import requests

BASE_URL = "http://localhost:8000"

def execute_command(command):
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"command": command}
    )
    return response.json()

# Create a task
result = execute_command("add task complete hackathon project")
print(result)
```

### JavaScript
```javascript
const BASE_URL = 'http://localhost:8000';

async function executeCommand(command) {
    const response = await fetch(`${BASE_URL}/execute`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command })
    });
    return await response.json();
}

// Create a task
executeCommand('add task complete hackathon project')
    .then(result => console.log(result));
```

---

## Interactive API Documentation

Visit the following URLs for interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test all endpoints directly from your browser.
