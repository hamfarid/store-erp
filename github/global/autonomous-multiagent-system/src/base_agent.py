"""
Base Agent for Autonomous Multi-Agent System

Base class for all agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, role: str, model: str):
        """
        Initialize Base Agent
        
        Args:
            name: Agent name
            role: Agent role
            model: AI model to use
        """
        self.name = name
        self.role = role
        self.model = model
        self.conversation_history = []
    
    @abstractmethod
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a task
        
        Args:
            task: Task description
            context: Additional context
            
        Returns:
            Task result
        """
        pass
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', role='{self.role}', model='{self.model}')"

