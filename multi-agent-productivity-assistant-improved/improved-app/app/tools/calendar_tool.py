"""
Calendar management tools with MCP-compatible interface.
"""

from typing import List, Optional, Dict, Any
from app.db.database import get_db_session
from app.db.models import Event


class CalendarTool:
    """MCP-compatible tool for calendar event management."""
    
    @staticmethod
    def add_event(name: str, date: str, time: Optional[str] = None,
                  description: Optional[str] = None,
                  location: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a new calendar event.
        
        Args:
            name: Event name
            date: Event date (YYYY-MM-DD format)
            time: Event time (optional)
            description: Event description (optional)
            location: Event location (optional)
            
        Returns:
            Dictionary containing event details
        """
        try:
            with get_db_session() as db:
                event = Event(
                    name=name,
                    date=date,
                    time=time,
                    description=description,
                    location=location
                )
                db.add(event)
                db.flush()
                
                return {
                    "success": True,
                    "message": f"Event '{name}' added successfully",
                    "event": event.to_dict()
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to add event: {str(e)}",
                "event": None
            }
    
    @staticmethod
    def get_events(date: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve calendar events with optional date filtering.
        
        Args:
            date: Filter by date (YYYY-MM-DD format, optional)
            
        Returns:
            Dictionary containing list of events
        """
        try:
            with get_db_session() as db:
                query = db.query(Event)
                
                if date:
                    query = query.filter(Event.date == date)
                
                events = query.order_by(Event.date, Event.time).all()
                
                return {
                    "success": True,
                    "message": f"Retrieved {len(events)} event(s)",
                    "events": [event.to_dict() for event in events],
                    "count": len(events)
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to retrieve events: {str(e)}",
                "events": [],
                "count": 0
            }
    
    @staticmethod
    def update_event(event_id: int, name: Optional[str] = None,
                    date: Optional[str] = None, time: Optional[str] = None,
                    description: Optional[str] = None,
                    location: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing event.
        
        Args:
            event_id: ID of the event to update
            name: New event name (optional)
            date: New event date (optional)
            time: New event time (optional)
            description: New event description (optional)
            location: New event location (optional)
            
        Returns:
            Dictionary containing updated event details
        """
        try:
            with get_db_session() as db:
                event = db.query(Event).filter(Event.id == event_id).first()
                
                if not event:
                    return {
                        "success": False,
                        "message": f"Event with ID {event_id} not found",
                        "event": None
                    }
                
                if name:
                    event.name = name
                if date:
                    event.date = date
                if time is not None:
                    event.time = time
                if description is not None:
                    event.description = description
                if location is not None:
                    event.location = location
                
                db.flush()
                
                return {
                    "success": True,
                    "message": f"Event {event_id} updated successfully",
                    "event": event.to_dict()
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update event: {str(e)}",
                "event": None
            }
    
    @staticmethod
    def delete_event(event_id: int) -> Dict[str, Any]:
        """
        Delete an event.
        
        Args:
            event_id: ID of the event to delete
            
        Returns:
            Dictionary containing deletion status
        """
        try:
            with get_db_session() as db:
                event = db.query(Event).filter(Event.id == event_id).first()
                
                if not event:
                    return {
                        "success": False,
                        "message": f"Event with ID {event_id} not found"
                    }
                
                event_name = event.name
                db.delete(event)
                db.flush()
                
                return {
                    "success": True,
                    "message": f"Event '{event_name}' deleted successfully"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to delete event: {str(e)}"
            }
