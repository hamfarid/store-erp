#!/usr/bin/env python3
"""
Example setup script for AI Memory System.

This script demonstrates how to set up and configure the memory system.
"""

import json
from pathlib import Path
from datetime import datetime


def setup_memory_directories():
    """Create memory directory structure."""
    base_dir = Path(__file__).parent
    
    directories = [
        'conversations',
        'knowledge',
        'preferences',
        'state',
        'checkpoints',
        'vectors'
    ]
    
    for dir_name in directories:
        dir_path = base_dir / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {dir_path}")


def create_example_files():
    """Create example files for each directory."""
    base_dir = Path(__file__).parent
    
    # Example conversation
    conversation = {
        "timestamp": datetime.now().isoformat(),
        "user_id": "user123",
        "conversation_id": "conv_001",
        "messages": [
            {"role": "user", "content": "How do I implement authentication?"},
            {"role": "assistant", "content": "I recommend using JWT tokens..."}
        ],
        "context": {
            "project": "ecommerce",
            "task": "authentication"
        }
    }
    
    conv_file = base_dir / 'conversations' / 'example_conversation.json'
    with open(conv_file, 'w') as f:
        json.dump(conversation, f, indent=2)
    print(f"✅ Created: {conv_file}")
    
    # Example knowledge
    knowledge = {
        "id": "know_001",
        "type": "semantic",
        "content": "User prefers PostgreSQL for this project",
        "importance": 8,
        "metadata": {
            "category": "preference",
            "project": "ecommerce"
        },
        "created_at": datetime.now().isoformat()
    }
    
    know_file = base_dir / 'knowledge' / 'example_knowledge.json'
    with open(know_file, 'w') as f:
        json.dump(knowledge, f, indent=2)
    print(f"✅ Created: {know_file}")
    
    # Example preferences
    preferences = {
        "user_id": "user123",
        "preferences": {
            "language": "python",
            "style": "functional",
            "database": "postgresql",
            "testing": "pytest"
        },
        "updated_at": datetime.now().isoformat()
    }
    
    pref_file = base_dir / 'preferences' / 'user123.json'
    with open(pref_file, 'w') as f:
        json.dump(preferences, f, indent=2)
    print(f"✅ Created: {pref_file}")
    
    # Example state
    state = {
        "user_id": "user123",
        "current_project": "ecommerce",
        "current_task": "authentication",
        "context": {
            "stack": ["Python", "React", "PostgreSQL"],
            "phase": "implementation"
        },
        "updated_at": datetime.now().isoformat()
    }
    
    state_file = base_dir / 'state' / 'current_state.json'
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"✅ Created: {state_file}")
    
    # Example checkpoint
    checkpoint = {
        "checkpoint_id": "cp_001",
        "name": "after_auth_implementation",
        "timestamp": datetime.now().isoformat(),
        "state": {
            "project": "ecommerce",
            "progress": 0.75,
            "completed_tasks": [
                "User model created",
                "JWT authentication implemented",
                "Login endpoint created"
            ]
        }
    }
    
    cp_file = base_dir / 'checkpoints' / 'after_auth_implementation.json'
    with open(cp_file, 'w') as f:
        json.dump(checkpoint, f, indent=2)
    print(f"✅ Created: {cp_file}")


def main():
    """Main setup function."""
    print("🚀 Setting up AI Memory System...\n")
    
    print("1️⃣ Creating directory structure...")
    setup_memory_directories()
    print()
    
    print("2️⃣ Creating example files...")
    create_example_files()
    print()
    
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Review the example files in each directory")
    print("2. Configure PostgreSQL (optional): createdb ai_memory")
    print("3. Start Redis (optional): redis-server --daemonize yes")
    print("4. Install ChromaDB (optional): pip install chromadb")
    print("5. See Module 60 for complete implementation")


if __name__ == '__main__':
    main()

