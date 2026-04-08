"""
Calendar Agent - Handles all calendar and event-related operations.
"""

import re
from typing import Dict, Any
from app.tools.calendar_tool import CalendarTool


class CalendarAgent:
    """Agent responsible for calendar event management operations."""
    
    def __init__(self):
        self.tool = CalendarTool()
        self.name = "CalendarAgent"
    
    def can_handle(self, command: str) -> bool:
        """
        Determine if this agent can handle the given command.
        
        Args:
            command: User command string
            
        Returns:
            True if agent can handle the command
        """
        calendar_keywords = [
            "event", "calendar", "meeting", "appointment",
            "schedule", "scheduled", "reminder"
        ]
        return any(keyword in command.lower() for keyword in calendar_keywords)
    
    def handle(self, command: str) -> Dict[str, Any]:
        """
        Process calendar-related commands.
        
        Args:
            command: User command string
            
        Returns:
            Dictionary containing operation results
        """
        command_lower = command.lower().strip()
        
        # Add event
        if any(phrase in command_lower for phrase in ["add event", "create event", "new event", "schedule"]):
            return self._add_event(command)
        
        # Show/list events
        elif any(phrase in command_lower for phrase in ["show event", "list event", "get event", "view event"]):
            return self._get_events(command)
        
        # Update event
        elif any(phrase in command_lower for phrase in ["update event", "edit event", "change event"]):
            return self._update_event(command)
        
        # Delete event
        elif any(phrase in command_lower for phrase in ["delete event", "remove event", "cancel event"]):
            return self._delete_event(command)
        
        else:
            return {
                "success": False,
                "message": "I didn't understand that calendar command. Try 'add event <name> on <date>' or 'show events'.",
                "agent": self.name
            }
    
    def _add_event(self, command: str) -> Dict[str, Any]:
        """Extract event details and create a new event."""
        command_lower = command.lower()
        
        # Try to extract date using "on <date>" pattern
        date_match = re.search(r'on\s+([\d-]+)', command_lower)
        if not date_match:
            return {
                "success": False,
                "message": "Please specify a date. Example: 'add event team meeting on 2024-04-15'",
                "agent": self.name
            }
        
        date = date_match.group(1)
        
        # Extract event name (everything before "on")
        name_part = command_lower.split(" on ")[0]
        for prefix in ["add event", "create event", "new event", "schedule"]:
            if prefix in name_part:
                name = name_part.replace(prefix, "").strip()
                break
        
        # Try to extract time using "at <time>" pattern
        time = None
        time_match = re.search(r'at\s+([\d:]+\s*(?:am|pm)?)', command_lower)
        if time_match:
            time = time_match.group(1)
        
        # Try to extract location
        location = None
        location_match = re.search(r'at\s+([^0-9][^,]+?)(?:\s+on|\s+at\s+\d|$)', command_lower)
        if location_match and not time_match:
            location = location_match.group(1).strip()
        
        if not name:
            return {
                "success": False,
                "message": "Please provide an event name. Example: 'add event team meeting on 2024-04-15'",
                "agent": self.name
            }
        
        result = self.tool.add_event(name=name, date=date, time=time, location=location)
        result["agent"] = self.name
        return result
    
    def _get_events(self, command: str) -> Dict[str, Any]:
        """Retrieve events with optional date filtering."""
        date = None
        
        # Try to extract date
        date_match = re.search(r'on\s+([\d-]+)', command.lower())
        if date_match:
            date = date_match.group(1)
        elif "today" in command.lower():
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d")
        
        result = self.tool.get_events(date=date)
        result["agent"] = self.name
        return result
    
    def _update_event(self, command: str) -> Dict[str, Any]:
        """Update event details."""
        match = re.search(r'(\d+)', command)
        if not match:
            return {
                "success": False,
                "message": "Please specify an event ID. Example: 'update event 1 to 2024-04-20'",
                "agent": self.name
            }
        
        event_id = int(match.group(1))
        
        # Extract new date if provided
        new_date = None
        date_match = re.search(r'(?:to|on)\s+([\d-]+)', command.lower())
        if date_match:
            new_date = date_match.group(1)
        
        # Extract new time if provided
        new_time = None
        time_match = re.search(r'at\s+([\d:]+\s*(?:am|pm)?)', command.lower())
        if time_match:
            new_time = time_match.group(1)
        
        result = self.tool.update_event(event_id, date=new_date, time=new_time)
        result["agent"] = self.name
        return result
    
    def _delete_event(self, command: str) -> Dict[str, Any]:
        """Delete an event."""
        match = re.search(r'(\d+)', command)
        if not match:
            return {
                "success": False,
                "message": "Please specify an event ID. Example: 'delete event 1'",
                "agent": self.name
            }
        
        event_id = int(match.group(1))
        result = self.tool.delete_event(event_id)
        result["agent"] = self.name
        return result
