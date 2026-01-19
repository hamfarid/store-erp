#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Integration module for memory and AI functionality in Gaara ERP system.
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from src.modules.memory.models import Memory, MemoryType, MemoryCategory, MemoryAccessLevel
from src.modules.ai_agent.models import AgentCapability
from src.modules.memory.services import MemoryService
from src.modules.ai_agent.services import AIAgentService


# Define constants for repeated strings
AGENT_NOT_FOUND_MSG = "لم يتم العثور على وكيل الذكاء الاصطناعي بالمعرف: {agent_id}"
AGENT_KEY_PREFIX = "agent:{agent_id}"
MEMORY_NOT_FOUND_MSG = "لم يتم العثور على الذاكرة بالمعرف: {memory_id}"
MEMORY_AGENT_MISMATCH_MSG = "الذاكرة {memory_id} لا تنتمي للوكيل {agent_id}"

logger = logging.getLogger(__name__)


class MemoryAIIntegration:
    """Integration class for memory and AI functionality."""

    def __init__(self, memory_service: MemoryService, ai_agent_service: AIAgentService):
        """Initialize the integration with required services."""
        self.memory_service = memory_service
        self.ai_agent_service = ai_agent_service
        self.logger = logging.getLogger(__name__)
        logger.info("MemoryAIIntegration initialized")

    def store_agent_memory(
            self,
            agent_id: str,
            content: str,
            memory_type: MemoryType,
            category: MemoryCategory,
            access_level: MemoryAccessLevel,
            metadata: Optional[Dict[str, Any]] = None
    ) -> Memory:
        """Store a new memory for an AI agent."""
        # Verify agent exists
        agent = self.ai_agent_service.get_agent_by_id(agent_id)
        if not agent:
            raise ValueError(AGENT_NOT_FOUND_MSG.format(agent_id=agent_id))

        # Create memory
        memory = Memory(
            agent_id=agent_id,
            content=content,
            memory_type=memory_type,
            category=category,
            access_level=access_level,
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        return self.memory_service.create_memory(memory)

    def retrieve_agent_memories(
            self,
            agent_id: str,
            memory_type: Optional[MemoryType] = None,
            category: Optional[MemoryCategory] = None,
            limit: int = 100
    ) -> List[Memory]:
        """Retrieve memories for an AI agent with optional filtering."""
        # Verify agent exists
        agent = self.ai_agent_service.get_agent_by_id(agent_id)
        if not agent:
            raise ValueError(AGENT_NOT_FOUND_MSG.format(agent_id=agent_id))

        # Build query filters
        filters = {"agent_id": agent_id}
        if memory_type:
            filters["memory_type"] = memory_type
        if category:
            filters["category"] = category

        return self.memory_service.get_memories(filters, limit=limit)

    def update_agent_memory(
            self,
            memory_id: str,
            agent_id: str,
            content: Optional[str] = None,
            memory_type: Optional[MemoryType] = None,
            category: Optional[MemoryCategory] = None,
            access_level: Optional[MemoryAccessLevel] = None,
            metadata: Optional[Dict[str, Any]] = None
    ) -> Memory:
        """Update an existing memory for an AI agent."""
        # Verify memory exists and belongs to agent
        memory = self.memory_service.get_memory_by_id(memory_id)
        if not memory:
            raise ValueError(MEMORY_NOT_FOUND_MSG.format(memory_id=memory_id))
        if memory.agent_id != agent_id:
            raise ValueError(MEMORY_AGENT_MISMATCH_MSG.format(memory_id=memory_id, agent_id=agent_id))

        # Update memory fields
        if content is not None:
            memory.content = content
        if memory_type is not None:
            memory.memory_type = memory_type
        if category is not None:
            memory.category = category
        if access_level is not None:
            memory.access_level = access_level
        if metadata is not None:
            memory.metadata.update(metadata)
        memory.updated_at = datetime.now(timezone.utc)

        return self.memory_service.update_memory(memory)

    def delete_agent_memory(self, memory_id: str, agent_id: str) -> bool:
        """Delete a memory for an AI agent."""
        # Verify memory exists and belongs to agent
        memory = self.memory_service.get_memory_by_id(memory_id)
        if not memory:
            raise ValueError(MEMORY_NOT_FOUND_MSG.format(memory_id=memory_id))
        if memory.agent_id != agent_id:
            raise ValueError(MEMORY_AGENT_MISMATCH_MSG.format(memory_id=memory_id, agent_id=agent_id))

        return self.memory_service.delete_memory(memory_id)

    def process_memory_with_ai(self, memory_id: str, agent_id: str) -> Dict[str, Any]:
        """Process a memory using AI capabilities."""
        # Verify memory exists and belongs to agent
        memory = self.memory_service.get_memory_by_id(memory_id)
        if not memory:
            raise ValueError(MEMORY_NOT_FOUND_MSG.format(memory_id=memory_id))
        if memory.agent_id != agent_id:
            raise ValueError(MEMORY_AGENT_MISMATCH_MSG.format(memory_id=memory_id, agent_id=agent_id))

        # Get agent capabilities
        agent = self.ai_agent_service.get_agent_by_id(agent_id)
        if not agent:
            raise ValueError(AGENT_NOT_FOUND_MSG.format(agent_id=agent_id))

        # Process memory based on agent capabilities
        results = {}
        for capability in agent.capabilities:
            if capability == AgentCapability.TEXT_ANALYSIS:
                results['text_analysis'] = self._analyze_text()
            elif capability == AgentCapability.IMAGE_RECOGNITION:
                results['image_recognition'] = self._recognize_image()
            elif capability == AgentCapability.SENTIMENT_ANALYSIS:
                results['sentiment'] = self._analyze_sentiment()

        return results

    def _analyze_text(self) -> Dict[str, Any]:
        """Analyze text content using AI."""
        # TODO: Implement text analysis
        return {}

    def _recognize_image(self) -> Dict[str, Any]:
        """Recognize image content using AI."""
        # TODO: Implement image recognition
        return {}

    def _analyze_sentiment(self) -> Dict[str, Any]:
        """Analyze sentiment using AI."""
        # TODO: Implement sentiment analysis
        return {}
