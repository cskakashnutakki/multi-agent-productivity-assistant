"""
Multi-Agent Productivity Assistant - Main FastAPI Application
"""

import os
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.agents.coordinator import Coordinator
from app.db.database import init_db, engine
from app.schemas import CommandRequest, CommandResponse, HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initialize database on startup.
    """
    # Startup: Create database tables
    init_db()
    print("✓ Database initialized")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    yield
    
    # Shutdown: cleanup if needed
    print("✓ Application shutdown")


# Initialize FastAPI application
app = FastAPI(
    title="Multi-Agent Productivity Assistant",
    description="A sophisticated multi-agent AI system for task, calendar, and notes management",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize coordinator
coordinator = Coordinator()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
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


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring and deployment.
    Returns system health status and database connectivity.
    """
    try:
        # Check database connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        return HealthResponse(
            status="healthy",
            database="connected",
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@app.get("/status")
async def get_status():
    """
    Get system status and statistics.
    Returns information about agents and data counts.
    """
    try:
        status = coordinator.get_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/execute", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Execute a natural language command through the multi-agent system.
    
    Supports:
    - Task management (add, list, update, complete, delete tasks)
    - Calendar events (add, list, update, delete events)
    - Notes (add, list, update, delete notes)
    - Multi-step workflows (chain multiple commands with 'and', 'then', 'also')
    
    Examples:
    - "add task finish project report"
    - "schedule meeting on 2024-04-15 at 2pm"
    - "add note buy groceries #shopping"
    - "add task prepare presentation and schedule review meeting on 2024-04-20"
    """
    try:
        # Route command to coordinator
        result = coordinator.route(request.command)
        
        # Format response
        if result.get("success"):
            return CommandResponse(
                status="success",
                message=result.get("message", "Command executed successfully"),
                data=result,
                agent=result.get("agent")
            )
        else:
            return CommandResponse(
                status="error",
                message=result.get("message", "Command failed"),
                data=result,
                agent=result.get("agent")
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error executing command: {str(e)}"
        )


@app.get("/help")
async def get_help():
    """
    Get help information about available commands.
    """
    return {
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
