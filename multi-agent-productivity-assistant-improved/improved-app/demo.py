#!/usr/bin/env python3
"""
Demo script to showcase the Multi-Agent Productivity Assistant
"""

import json
from app.agents.coordinator import Coordinator
from app.db.database import init_db

def demo():
    """Run demonstration commands."""
    
    # Initialize database
    print("Initializing database...")
    init_db()
    print("✓ Database ready\n")
    
    # Create coordinator
    coordinator = Coordinator()
    
    # Demo commands
    commands = [
        "add task complete hackathon presentation high priority",
        "add task review code",
        "add event team standup on 2024-04-15 at 10:00 AM",
        "add note remember to update GitHub repository #important",
        "show tasks",
        "show events",
        "show notes",
        "add task prepare demo and schedule demo meeting on 2024-04-20"
    ]
    
    print("=" * 60)
    print("MULTI-AGENT PRODUCTIVITY ASSISTANT - DEMO")
    print("=" * 60)
    print()
    
    for i, command in enumerate(commands, 1):
        print(f"\n[Command {i}] {command}")
        print("-" * 60)
        
        result = coordinator.route(command)
        
        # Pretty print result
        print(json.dumps(result, indent=2, default=str))
        print()
    
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    demo()
