"""
Pydantic schemas for request/response validation.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class CommandRequest(BaseModel):
    """Request schema for command execution."""
    command: str = Field(..., description="Natural language command to execute")
    

class CommandResponse(BaseModel):
    """Response schema for command execution."""
    status: str = Field(..., description="Status of the command execution")
    message: str = Field(..., description="Human-readable message")
    data: Optional[dict] = Field(None, description="Response data")
    agent: Optional[str] = Field(None, description="Agent that handled the command")


class TaskCreate(BaseModel):
    """Schema for creating a task."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = Field("medium", pattern="^(low|medium|high)$")


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: str
    updated_at: str


class EventCreate(BaseModel):
    """Schema for creating an event."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    date: str = Field(..., description="Event date (YYYY-MM-DD format)")
    time: Optional[str] = None
    location: Optional[str] = None


class EventResponse(BaseModel):
    """Schema for event response."""
    id: int
    name: str
    description: Optional[str]
    date: str
    time: Optional[str]
    location: Optional[str]
    created_at: str
    updated_at: str


class NoteCreate(BaseModel):
    """Schema for creating a note."""
    title: Optional[str] = None
    content: str = Field(..., min_length=1)
    tags: Optional[List[str]] = None


class NoteResponse(BaseModel):
    """Schema for note response."""
    id: int
    title: Optional[str]
    content: str
    tags: List[str]
    created_at: str
    updated_at: str


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
    database: str
    timestamp: str
