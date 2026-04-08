"""
Task Agent - Handles all task-related operations.
"""

import re
from typing import Dict, Any
from app.tools.task_tool import TaskTool


class TaskAgent:
    """Agent responsible for task management operations."""
    
    def __init__(self):
        self.tool = TaskTool()
        self.name = "TaskAgent"
    
    def can_handle(self, command: str) -> bool:
        """
        Determine if this agent can handle the given command.
        
        Args:
            command: User command string
            
        Returns:
            True if agent can handle the command
        """
        task_keywords = [
            "task", "todo", "to-do", "to do",
            "complete", "finish", "done",
            "pending", "in progress"
        ]
        return any(keyword in command.lower() for keyword in task_keywords)
    
    def handle(self, command: str) -> Dict[str, Any]:
        """
        Process task-related commands.
        
        Args:
            command: User command string
            
        Returns:
            Dictionary containing operation results
        """
        command_lower = command.lower().strip()
        
        # Create task
        if any(phrase in command_lower for phrase in ["add task", "create task", "new task"]):
            return self._create_task(command)
        
        # Show/list tasks
        elif any(phrase in command_lower for phrase in ["show task", "list task", "get task", "view task"]):
            return self._get_tasks(command)
        
        # Complete task
        elif any(phrase in command_lower for phrase in ["complete task", "finish task", "done task", "mark task complete"]):
            return self._complete_task(command)
        
        # Update task
        elif any(phrase in command_lower for phrase in ["update task", "edit task", "change task"]):
            return self._update_task(command)
        
        # Delete task
        elif any(phrase in command_lower for phrase in ["delete task", "remove task"]):
            return self._delete_task(command)
        
        else:
            return {
                "success": False,
                "message": "I didn't understand that task command. Try 'add task <title>' or 'show tasks'.",
                "agent": self.name
            }
    
    def _create_task(self, command: str) -> Dict[str, Any]:
        """Extract task details and create a new task."""
        # Remove command prefix
        for prefix in ["add task", "create task", "new task"]:
            if prefix in command.lower():
                title = command.lower().replace(prefix, "").strip()
                break
        
        # Extract priority if mentioned
        priority = "medium"
        if "high priority" in title or "urgent" in title:
            priority = "high"
            title = title.replace("high priority", "").replace("urgent", "").strip()
        elif "low priority" in title:
            priority = "low"
            title = title.replace("low priority", "").strip()
        
        if not title:
            return {
                "success": False,
                "message": "Please provide a task title. Example: 'add task finish project'",
                "agent": self.name
            }
        
        result = self.tool.create_task(title=title, priority=priority)
        result["agent"] = self.name
        return result
    
    def _get_tasks(self, command: str) -> Dict[str, Any]:
        """Retrieve tasks with optional filtering."""
        status = None
        priority = None
        
        command_lower = command.lower()
        
        # Extract status filter
        if "pending" in command_lower:
            status = "pending"
        elif "completed" in command_lower:
            status = "completed"
        
        # Extract priority filter
        if "high priority" in command_lower:
            priority = "high"
        elif "low priority" in command_lower:
            priority = "low"
        
        result = self.tool.get_tasks(status=status, priority=priority)
        result["agent"] = self.name
        return result
    
    def _complete_task(self, command: str) -> Dict[str, Any]:
        """Mark a task as completed."""
        # Try to extract task ID
        match = re.search(r'(\d+)', command)
        if not match:
            return {
                "success": False,
                "message": "Please specify a task ID. Example: 'complete task 1'",
                "agent": self.name
            }
        
        task_id = int(match.group(1))
        result = self.tool.complete_task(task_id)
        result["agent"] = self.name
        return result
    
    def _update_task(self, command: str) -> Dict[str, Any]:
        """Update task details."""
        match = re.search(r'(\d+)', command)
        if not match:
            return {
                "success": False,
                "message": "Please specify a task ID. Example: 'update task 1 to high priority'",
                "agent": self.name
            }
        
        task_id = int(match.group(1))
        
        # Determine what to update
        priority = None
        status = None
        
        if "high priority" in command.lower():
            priority = "high"
        elif "low priority" in command.lower():
            priority = "low"
        elif "medium priority" in command.lower():
            priority = "medium"
        
        if "completed" in command.lower():
            status = "completed"
        elif "pending" in command.lower():
            status = "pending"
        
        result = self.tool.update_task(task_id, status=status, priority=priority)
        result["agent"] = self.name
        return result
    
    def _delete_task(self, command: str) -> Dict[str, Any]:
        """Delete a task."""
        match = re.search(r'(\d+)', command)
        if not match:
            return {
                "success": False,
                "message": "Please specify a task ID. Example: 'delete task 1'",
                "agent": self.name
            }
        
        task_id = int(match.group(1))
        result = self.tool.delete_task(task_id)
        result["agent"] = self.name
        return result
