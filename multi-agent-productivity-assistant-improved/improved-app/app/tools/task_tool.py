"""
Task management tools with MCP-compatible interface.
"""

from typing import List, Optional, Dict, Any
from app.db.database import get_db_session
from app.db.models import Task


class TaskTool:
    """MCP-compatible tool for task management."""
    
    @staticmethod
    def create_task(title: str, description: Optional[str] = None, 
                   priority: str = "medium") -> Dict[str, Any]:
        """
        Create a new task.
        
        Args:
            title: Task title
            description: Task description (optional)
            priority: Task priority (low/medium/high)
            
        Returns:
            Dictionary containing task details
        """
        try:
            with get_db_session() as db:
                task = Task(
                    title=title,
                    description=description,
                    status="pending",
                    priority=priority
                )
                db.add(task)
                db.flush()  # Flush to get the ID
                
                return {
                    "success": True,
                    "message": f"Task '{title}' created successfully",
                    "task": task.to_dict()
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create task: {str(e)}",
                "task": None
            }
    
    @staticmethod
    def get_tasks(status: Optional[str] = None, 
                  priority: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve tasks with optional filtering.
        
        Args:
            status: Filter by status (optional)
            priority: Filter by priority (optional)
            
        Returns:
            Dictionary containing list of tasks
        """
        try:
            with get_db_session() as db:
                query = db.query(Task)
                
                if status:
                    query = query.filter(Task.status == status)
                if priority:
                    query = query.filter(Task.priority == priority)
                
                tasks = query.order_by(Task.created_at.desc()).all()
                
                return {
                    "success": True,
                    "message": f"Retrieved {len(tasks)} task(s)",
                    "tasks": [task.to_dict() for task in tasks],
                    "count": len(tasks)
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to retrieve tasks: {str(e)}",
                "tasks": [],
                "count": 0
            }
    
    @staticmethod
    def update_task(task_id: int, status: Optional[str] = None,
                   priority: Optional[str] = None,
                   description: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing task.
        
        Args:
            task_id: ID of the task to update
            status: New status (optional)
            priority: New priority (optional)
            description: New description (optional)
            
        Returns:
            Dictionary containing updated task details
        """
        try:
            with get_db_session() as db:
                task = db.query(Task).filter(Task.id == task_id).first()
                
                if not task:
                    return {
                        "success": False,
                        "message": f"Task with ID {task_id} not found",
                        "task": None
                    }
                
                if status:
                    task.status = status
                if priority:
                    task.priority = priority
                if description is not None:
                    task.description = description
                
                db.flush()
                
                return {
                    "success": True,
                    "message": f"Task {task_id} updated successfully",
                    "task": task.to_dict()
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update task: {str(e)}",
                "task": None
            }
    
    @staticmethod
    def delete_task(task_id: int) -> Dict[str, Any]:
        """
        Delete a task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            Dictionary containing deletion status
        """
        try:
            with get_db_session() as db:
                task = db.query(Task).filter(Task.id == task_id).first()
                
                if not task:
                    return {
                        "success": False,
                        "message": f"Task with ID {task_id} not found"
                    }
                
                task_title = task.title
                db.delete(task)
                db.flush()
                
                return {
                    "success": True,
                    "message": f"Task '{task_title}' deleted successfully"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to delete task: {str(e)}"
            }
    
    @staticmethod
    def complete_task(task_id: int) -> Dict[str, Any]:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to complete
            
        Returns:
            Dictionary containing completion status
        """
        return TaskTool.update_task(task_id, status="completed")
