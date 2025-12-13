"""
Memory Manager for Autonomous Multi-Agent System

Manages project-specific memory storage and retrieval.
"""

from pathlib import Path
from datetime import datetime
import json
from typing import Optional, Dict, Any


class MemoryManager:
    """Manages Memory for a specific project"""
    
    def __init__(self, project_name: str):
        """
        Initialize Memory Manager
        
        Args:
            project_name: Name of the project
        """
        self.project_name = project_name
        self.base_path = Path.home() / ".global" / "memory" / project_name
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize memory files
        self._initialize_memory()
    
    def _initialize_memory(self):
        """Initialize memory files if they don't exist"""
        default_files = {
            "context.md": f"# Project: {self.project_name}\n\nCreated: {datetime.now().isoformat()}\n",
            "decisions.md": "# Architectural Decisions\n\n",
            "architecture.md": "# System Architecture\n\n",
            "preferences.md": "# Development Preferences\n\n",
            "progress.md": "# Project Progress\n\n",
            "agents_log.md": "# Agent Interactions Log\n\n"
        }
        
        for filename, content in default_files.items():
            file_path = self.base_path / filename
            if not file_path.exists():
                file_path.write_text(content, encoding='utf-8')
    
    def save(self, key: str, content: str):
        """
        Save content to memory
        
        Args:
            key: Memory key (e.g., 'context', 'decisions')
            content: Content to save
        """
        file_path = self.base_path / f"{key}.md"
        file_path.write_text(content, encoding='utf-8')
        
        # Log the save
        self._log_action("save", key)
    
    def load(self, key: str) -> Optional[str]:
        """
        Load content from memory
        
        Args:
            key: Memory key
            
        Returns:
            Content if exists, None otherwise
        """
        file_path = self.base_path / f"{key}.md"
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        return None
    
    def append(self, key: str, content: str):
        """
        Append content to memory
        
        Args:
            key: Memory key
            content: Content to append
        """
        existing = self.load(key) or ""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_content = f"{existing}\n\n---\n**[{timestamp}]**\n\n{content}"
        self.save(key, new_content)
    
    def _log_action(self, action: str, key: str):
        """Log memory action"""
        log_entry = f"[{datetime.now().isoformat()}] {action.upper()}: {key}"
        self.append("agents_log", log_entry)
    
    def get_all_context(self) -> Dict[str, str]:
        """
        Get all memory context
        
        Returns:
            Dictionary of all memory content
        """
        context = {}
        for file_path in self.base_path.glob("*.md"):
            key = file_path.stem
            context[key] = file_path.read_text(encoding='utf-8')
        return context
    
    def save_json(self, key: str, data: Any):
        """
        Save JSON data to memory
        
        Args:
            key: Memory key
            data: Data to save (will be JSON serialized)
        """
        file_path = self.base_path / f"{key}.json"
        file_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        self._log_action("save_json", key)
    
    def load_json(self, key: str) -> Optional[Any]:
        """
        Load JSON data from memory
        
        Args:
            key: Memory key
            
        Returns:
            Parsed JSON data if exists, None otherwise
        """
        file_path = self.base_path / f"{key}.json"
        if file_path.exists():
            return json.loads(file_path.read_text(encoding='utf-8'))
        return None
    
    def clear(self):
        """Clear all memory for this project"""
        for file_path in self.base_path.glob("*"):
            if file_path.is_file():
                file_path.unlink()
        self._initialize_memory()
    
    def __repr__(self):
        return f"MemoryManager(project='{self.project_name}', path='{self.base_path}')"


if __name__ == "__main__":
    # Test
    memory = MemoryManager("test-project")
    memory.save("context", "This is a test project")
    print(memory.load("context"))
    memory.append("progress", "Phase 0: Initialized")
    print(memory.load("progress"))
    print(memory.get_all_context().keys())

