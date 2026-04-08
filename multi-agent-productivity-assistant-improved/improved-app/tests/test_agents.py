"""
Example tests for the Multi-Agent Productivity Assistant.
Run with: pytest tests/
"""

import pytest
from app.agents.coordinator import Coordinator
from app.db.database import init_db


@pytest.fixture
def coordinator():
    """Create a coordinator instance for testing."""
    init_db()
    return Coordinator()


class TestTaskAgent:
    """Test suite for TaskAgent functionality."""
    
    def test_create_task(self, coordinator):
        """Test task creation."""
        result = coordinator.route("add task complete unit tests")
        assert result["success"] is True
        assert "task" in result
    
    def test_list_tasks(self, coordinator):
        """Test listing tasks."""
        result = coordinator.route("show tasks")
        assert result["success"] is True
        assert "tasks" in result
    
    def test_complete_task(self, coordinator):
        """Test completing a task."""
        # First create a task
        create_result = coordinator.route("add task test task")
        task_id = create_result["task"]["id"]
        
        # Then complete it
        result = coordinator.route(f"complete task {task_id}")
        assert result["success"] is True


class TestCalendarAgent:
    """Test suite for CalendarAgent functionality."""
    
    def test_add_event(self, coordinator):
        """Test event creation."""
        result = coordinator.route("add event team meeting on 2024-04-15")
        assert result["success"] is True
        assert "event" in result
    
    def test_list_events(self, coordinator):
        """Test listing events."""
        result = coordinator.route("show events")
        assert result["success"] is True
        assert "events" in result


class TestNotesAgent:
    """Test suite for NotesAgent functionality."""
    
    def test_add_note(self, coordinator):
        """Test note creation."""
        result = coordinator.route("add note remember to buy groceries #shopping")
        assert result["success"] is True
        assert "note" in result
    
    def test_list_notes(self, coordinator):
        """Test listing notes."""
        result = coordinator.route("show notes")
        assert result["success"] is True
        assert "notes" in result


class TestMultiStep:
    """Test suite for multi-step workflow functionality."""
    
    def test_multi_step_workflow(self, coordinator):
        """Test chaining multiple commands."""
        result = coordinator.route(
            "add task prepare presentation and schedule meeting on 2024-04-20"
        )
        assert result["success"] is True
        assert result.get("workflow") is True
        assert len(result["steps"]) == 2
