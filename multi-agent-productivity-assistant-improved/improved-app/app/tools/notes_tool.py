"""
Notes management tools with MCP-compatible interface.
"""

from typing import List, Optional, Dict, Any
from app.db.database import get_db_session
from app.db.models import Note


class NotesTool:
    """MCP-compatible tool for notes management."""
    
    @staticmethod
    def add_note(content: str, title: Optional[str] = None,
                 tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Add a new note.
        
        Args:
            content: Note content
            title: Note title (optional)
            tags: List of tags (optional)
            
        Returns:
            Dictionary containing note details
        """
        try:
            with get_db_session() as db:
                note = Note(
                    content=content,
                    title=title,
                    tags=",".join(tags) if tags else None
                )
                db.add(note)
                db.flush()
                
                return {
                    "success": True,
                    "message": "Note added successfully",
                    "note": note.to_dict()
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to add note: {str(e)}",
                "note": None
            }
    
    @staticmethod
    def get_notes(tag: Optional[str] = None,
                  search: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve notes with optional filtering.
        
        Args:
            tag: Filter by tag (optional)
            search: Search in content (optional)
            
        Returns:
            Dictionary containing list of notes
        """
        try:
            with get_db_session() as db:
                query = db.query(Note)
                
                if tag:
                    query = query.filter(Note.tags.contains(tag))
                if search:
                    query = query.filter(Note.content.contains(search))
                
                notes = query.order_by(Note.created_at.desc()).all()
                
                return {
                    "success": True,
                    "message": f"Retrieved {len(notes)} note(s)",
                    "notes": [note.to_dict() for note in notes],
                    "count": len(notes)
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to retrieve notes: {str(e)}",
                "notes": [],
                "count": 0
            }
    
    @staticmethod
    def update_note(note_id: int, content: Optional[str] = None,
                   title: Optional[str] = None,
                   tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Update an existing note.
        
        Args:
            note_id: ID of the note to update
            content: New note content (optional)
            title: New note title (optional)
            tags: New list of tags (optional)
            
        Returns:
            Dictionary containing updated note details
        """
        try:
            with get_db_session() as db:
                note = db.query(Note).filter(Note.id == note_id).first()
                
                if not note:
                    return {
                        "success": False,
                        "message": f"Note with ID {note_id} not found",
                        "note": None
                    }
                
                if content:
                    note.content = content
                if title is not None:
                    note.title = title
                if tags is not None:
                    note.tags = ",".join(tags)
                
                db.flush()
                
                return {
                    "success": True,
                    "message": f"Note {note_id} updated successfully",
                    "note": note.to_dict()
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update note: {str(e)}",
                "note": None
            }
    
    @staticmethod
    def delete_note(note_id: int) -> Dict[str, Any]:
        """
        Delete a note.
        
        Args:
            note_id: ID of the note to delete
            
        Returns:
            Dictionary containing deletion status
        """
        try:
            with get_db_session() as db:
                note = db.query(Note).filter(Note.id == note_id).first()
                
                if not note:
                    return {
                        "success": False,
                        "message": f"Note with ID {note_id} not found"
                    }
                
                db.delete(note)
                db.flush()
                
                return {
                    "success": True,
                    "message": "Note deleted successfully"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to delete note: {str(e)}"
            }
