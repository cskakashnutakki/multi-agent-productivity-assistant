# Multi-Agent Productivity Assistant

A sophisticated multi-agent AI system that helps users manage tasks, schedules, and information by intelligently coordinating multiple specialized agents and integrating with external tools through the Model Context Protocol (MCP).

## 🎯 Problem Statement

Build a multi-agent AI system that helps users manage tasks, schedules, and information by interacting with multiple tools and data sources.

## ✨ Core Features

### Multi-Agent Architecture
- **Coordinator Agent**: Primary orchestrator that routes commands to specialized sub-agents
- **Task Agent**: Manages task creation, updates, completion, and retrieval
- **Calendar Agent**: Handles event scheduling, viewing, and management
- **Notes Agent**: Stores and retrieves user notes and information

### Database Integration
- SQLite database for persistent structured data storage
- SQLAlchemy ORM for robust database operations
- Automatic schema creation and migration support

### MCP (Model Context Protocol) Integration
- Extensible tool integration framework
- Support for external calendar, task manager, and note-taking tools
- Standardized interface for adding new tools

### Multi-Step Workflow Support
- Intelligent command parsing and intent recognition
- Sequential task execution with context preservation
- Error handling and graceful degradation

### API-Based Deployment
- FastAPI backend with RESTful endpoints
- Async request handling for scalability
- Comprehensive error responses
- OpenAPI documentation auto-generation

## 🏗️ Architecture

```
┌─────────────────┐
│   API Layer     │ ← FastAPI REST endpoints
│  (main.py)      │
└────────┬────────┘
         │
┌────────▼────────┐
│   Coordinator   │ ← Primary routing agent
│     Agent       │
└────────┬────────┘
         │
    ┌────┴────┬─────────┬──────────┐
    │         │         │          │
┌───▼──┐  ┌──▼───┐  ┌──▼────┐  ┌──▼────┐
│Task  │  │Calen-│  │Notes  │  │Future │
│Agent │  │dar   │  │Agent  │  │Agents │
└───┬──┘  └──┬───┘  └──┬────┘  └───────┘
    │        │         │
┌───▼────────▼─────────▼───┐
│      Tool Layer          │ ← MCP-compatible tools
│  (Task/Calendar/Notes)   │
└──────────┬───────────────┘
           │
┌──────────▼───────────────┐
│   Database Layer         │ ← SQLite + SQLAlchemy
│   (Tasks/Events/Notes)   │
└──────────────────────────┘
```

## 🚀 Getting Started

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access the API
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Using the API

#### Create a Task
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "add task finish project presentation"}'
```

#### View Tasks
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "show tasks"}'
```

#### Add Calendar Event
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "add event team meeting on 2024-04-15"}'
```

#### Create Note
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "add note remember to buy groceries"}'
```

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t multi-agent-assistant .

# Run the container
docker run -p 8000:8000 multi-agent-assistant
```

## ☁️ Google Cloud Run Deployment

```bash
# Build and deploy to Cloud Run
gcloud run deploy multi-agent-assistant \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📊 Database Schema

### Tasks Table
- `id`: Integer (Primary Key)
- `title`: String
- `status`: String (pending/completed)
- `created_at`: DateTime

### Events Table
- `id`: Integer (Primary Key)
- `name`: String
- `date`: String
- `created_at`: DateTime

### Notes Table
- `id`: Integer (Primary Key)
- `content`: String
- `created_at`: DateTime

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **AI/ML**: Anthropic Claude (for future NLP enhancements)
- **Deployment**: Docker, Google Cloud Run
- **API Documentation**: OpenAPI/Swagger

## 🔮 Future Enhancements

1. **Enhanced NLP**: Integration with Claude AI for natural language understanding
2. **MCP Server Integration**: Connect to real calendar APIs (Google Calendar, Outlook)
3. **User Authentication**: Multi-user support with JWT tokens
4. **WebSocket Support**: Real-time updates for collaborative features
5. **Advanced Workflows**: Chain multiple commands in a single request
6. **Analytics Dashboard**: Task completion metrics and productivity insights

## 📝 API Endpoints

### POST /execute
Execute a command through the multi-agent system.

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
  "data": { ... },
  "agent": "TaskAgent"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project was created for the Gen AI Academy APAC Edition Hackathon.

## 👨‍💻 Author

**Nutakki Chandra Sekhara Krishna Akash**

