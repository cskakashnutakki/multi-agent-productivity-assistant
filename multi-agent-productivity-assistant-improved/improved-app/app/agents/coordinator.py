"""
Coordinator Agent - Primary orchestrator for multi-agent system.
"""

from typing import Dict, Any, List
from app.agents.task_agent import TaskAgent
from app.agents.calendar_agent import CalendarAgent
from app.agents.notes_agent import NotesAgent


class Coordinator:
    """
    Primary coordinator agent that routes commands to specialized sub-agents.
    Supports multi-step workflows and intelligent command routing.
    """
    
    def __init__(self):
        self.agents = {
            "task": TaskAgent(),
            "calendar": CalendarAgent(),
            "notes": NotesAgent()
        }
        self.name = "Coordinator"
    
    def route(self, command: str) -> Dict[str, Any]:
        """
        Route command to appropriate agent(s).
        
        Supports:
        - Single commands: "add task finish report"
        - Multi-step workflows: "add task prepare for meeting and schedule meeting on 2024-04-15"
        
        Args:
            command: User command string
            
        Returns:
            Dictionary containing operation results
        """
        try:
            # Check if this is a multi-step command (contains "and", "then", "also")
            if any(connector in command.lower() for connector in [" and ", " then ", " also "]):
                return self._handle_multi_step(command)
            
            # Single command - route to appropriate agent
            return self._route_single_command(command)
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error processing command: {str(e)}",
                "agent": self.name
            }
    
    def _route_single_command(self, command: str) -> Dict[str, Any]:
        """
        Route a single command to the appropriate agent.
        
        Args:
            command: User command string
            
        Returns:
            Dictionary containing operation results
        """
        # Try each agent to see who can handle this
        for agent_name, agent in self.agents.items():
            if agent.can_handle(command):
                return agent.handle(command)
        
        # No agent could handle this command
        return {
            "success": False,
            "message": self._get_help_message(),
            "agent": self.name
        }
    
    def _handle_multi_step(self, command: str) -> Dict[str, Any]:
        """
        Handle multi-step workflows by breaking down and executing sequentially.
        
        Args:
            command: Multi-step command string
            
        Returns:
            Dictionary containing aggregated results
        """
        # Split command by connectors
        sub_commands = []
        current_command = command
        
        for connector in [" and then ", " and ", " then ", " also "]:
            if connector in current_command.lower():
                parts = current_command.split(connector, 1)
                sub_commands.append(parts[0].strip())
                current_command = parts[1].strip()
        
        # Add the last part
        sub_commands.append(current_command)
        
        # Execute each sub-command
        results = []
        for sub_cmd in sub_commands:
            result = self._route_single_command(sub_cmd)
            results.append({
                "command": sub_cmd,
                "result": result
            })
        
        # Aggregate results
        all_success = all(r["result"].get("success", False) for r in results)
        
        return {
            "success": all_success,
            "message": f"Executed {len(results)} step(s)" + (" successfully" if all_success else " with some failures"),
            "steps": results,
            "agent": self.name,
            "workflow": True
        }
    
    def _get_help_message(self) -> str:
        """Generate helpful message with available commands."""
        return """I can help you with:
        
Tasks:
  - add task <title> [high/low priority]
  - show tasks [pending/completed]
  - complete task <id>
  - update task <id> [to <status/priority>]
  - delete task <id>

Calendar:
  - add event <name> on <date> [at <time>]
  - show events [on <date>]
  - update event <id> to <date/time>
  - delete event <id>

Notes:
  - add note <content> [#tag1 #tag2]
  - show notes [#tag] [containing <text>]
  - update note <id> to <new content>
  - delete note <id>

Multi-step:
  - Use 'and', 'then', or 'also' to chain commands
  - Example: "add task prepare for meeting and schedule meeting on 2024-04-15"
"""
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get system status and statistics.
        
        Returns:
            Dictionary containing system status
        """
        try:
            status = {
                "success": True,
                "coordinator": self.name,
                "agents": {
                    "task": self.agents["task"].name,
                    "calendar": self.agents["calendar"].name,
                    "notes": self.agents["notes"].name
                }
            }
            
            # Get counts from each agent
            task_result = self.agents["task"].tool.get_tasks()
            status["task_count"] = task_result.get("count", 0)
            
            calendar_result = self.agents["calendar"].tool.get_events()
            status["event_count"] = calendar_result.get("count", 0)
            
            notes_result = self.agents["notes"].tool.get_notes()
            status["note_count"] = notes_result.get("count", 0)
            
            return status
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting status: {str(e)}",
                "agent": self.name
            }
