"""
Notes Agent - Handles all note-taking and information storage operations.
"""

import re
from typing import Dict, Any
from app.tools.notes_tool import NotesTool


class NotesAgent:
    """Agent responsible for notes management operations."""
    
    def __init__(self):
        self.tool = NotesTool()
        self.name = "NotesAgent"
    
    def can_handle(self, command: str) -> bool:
        """
        Determine if this agent can handle the given command.
        
        Args:
            command: User command string
            
        Returns:
            True if agent can handle the command
        """
        notes_keywords = [
            "note", "notes", "jot", "write down",
            "remember", "save", "record"
        ]
        return any(keyword in command.lower() for keyword in notes_keywords)
    
    def handle(self, command: str) -> Dict[str, Any]:
        """
        Process notes-related commands.
        
        Args:
            command: User command string
            
        Returns:
            Dictionary containing operation results
        """
        command_lower = command.lower().strip()
        
        # Add note
        if any(phrase in command_lower for phrase in ["add note", "create note", "new note", "save note", "jot down", "write down"]):
            return self._add_note(command)
        
        # Show/list notes
        elif any(phrase in command_lower for phrase in ["show note", "list note", "get note", "view note", "find note", "search note"]):
            return self._get_notes(command)
        
        # Update note
        elif any(phrase in command_lower for phrase in ["update note", "edit note", "change note"]):
            return self._update_note(command)
        
        # Delete note
        elif any(phrase in command_lower for phrase in ["delete note", "remove note"]):
            return self._delete_note(command)
        
        else:
            return {
                "success": False,
                "message": "I didn't understand that note command. Try 'add note <content>' or 'show notes'.",
                "agent": self.name
            }
    
    def _add_note(self, command: str) -> Dict[str, Any]:
        """Extract note details and create a new note."""
        # Remove command prefix
        content = command
        for prefix in ["add note", "create note", "new note", "save note", "jot down", "write down"]:
            if prefix in command.lower():
                content = command.lower().replace(prefix, "").strip()
                break
        
        # Extract tags if mentioned using #tag format
        tags = []
        tag_matches = re.findall(r'#(\w+)', content)
        if tag_matches:
            tags = tag_matches
            # Remove tags from content
            content = re.sub(r'#\w+', '', content).strip()
        
        if not content:
            return {
                "success": False,
                "message": "Please provide note content. Example: 'add note buy groceries tomorrow'",
                "agent": self.name
            }
        
        result = self.tool.add_note(content=content, tags=tags if tags else None)
        result["agent"] = self.name
        return result
    
    def _get_notes(self, command: str) -> Dict[str, Any]:
        """Retrieve notes with optional filtering."""
        tag = None
        search = None
        
        command_lower = command.lower()
        
        # Extract tag filter
        tag_match = re.search(r'#(\w+)', command_lower)
        if tag_match:
            tag = tag_match.group(1)
        elif "tagged" in command_lower or "tag" in command_lower:
            # Try to extract tag after "tagged" or "tag"
            tag_pattern = re.search(r'(?:tagged?|with tag)\s+(\w+)', command_lower)
            if tag_pattern:
                tag = tag_pattern.group(1)
        
        # Extract search term
        if "containing" in command_lower or "with" in command_lower:
            search_pattern = re.search(r'(?:containing|with)\s+"?([^"]+)"?', command_lower)
            if search_pattern:
                search = search_pattern.group(1).strip()
        
        result = self.tool.get_notes(tag=tag, search=search)
        result["agent"] = self.name
        return result
    
    def _update_note(self, command: str) -> Dict[str, Any]:
        """Update note details."""
        match = re.search(r'(\d+)', command)
        if not match:
            return {
                "success": False,
                "message": "Please specify a note ID. Example: 'update note 1 to <new content>'",
                "agent": self.name
            }
        
        note_id = int(match.group(1))
        
        # Extract new content after "to"
        content = None
        content_match = re.search(r'to\s+(.+)', command, re.IGNORECASE)
        if content_match:
            content = content_match.group(1).strip()
        
        # Extract tags if present
        tags = None
        if content:
            tag_matches = re.findall(r'#(\w+)', content)
            if tag_matches:
                tags = tag_matches
                content = re.sub(r'#\w+', '', content).strip()
        
        result = self.tool.update_note(note_id, content=content, tags=tags)
        result["agent"] = self.name
        return result
    
    def _delete_note(self, command: str) -> Dict[str, Any]:
        """Delete a note."""
        match = re.search(r'(\d+)', command)
        if not match:
            return {
                "success": False,
                "message": "Please specify a note ID. Example: 'delete note 1'",
                "agent": self.name
            }
        
        note_id = int(match.group(1))
        result = self.tool.delete_note(note_id)
        result["agent"] = self.name
        return result
