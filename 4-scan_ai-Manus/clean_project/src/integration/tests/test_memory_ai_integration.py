"""
Unit tests for memory and AI integration in Gaara ERP system.
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch

from src.modules.memory.models import (
    Memory,
    MemoryType,
    MemoryCategory,
    MemoryAccessLevel
)
from src.modules.ai_agent.models import AIAgent, AgentType, AgentCapability
from src.modules.memory.services import MemoryService
from src.modules.ai_agent.services import AIAgentService
from src.integration.memory_ai_integration import MemoryAIIntegration

@pytest.fixture
def mock_memory_service():
    """Create a mock memory service."""
    service = Mock(spec=MemoryService)
    return service

@pytest.fixture
def mock_ai_agent_service():
    """Create a mock AI agent service."""
    service = Mock(spec=AIAgentService)
    return service

@pytest.fixture
def integration_service(mock_memory_service, mock_ai_agent_service):
    """Create an integration service instance."""
    return MemoryAIIntegration(mock_memory_service, mock_ai_agent_service)

@pytest.fixture
def test_memory():
    """Create a test memory instance."""
    return Memory(
        id=1,
        content="Test memory content",
        memory_type=MemoryType.KNOWLEDGE_BASE,
        category=MemoryCategory.PERSONAL,
        access_level=MemoryAccessLevel.PRIVATE,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

@pytest.fixture
def test_agent():
    """Create a test AI agent instance."""
    return AIAgent(
        id=1,
        name="Test Agent",
        agent_type=AgentType.SYSTEM,
        capabilities=[AgentCapability.TEXT_ANALYSIS],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

@pytest.mark.asyncio
async def test_query_memory_with_ai(integration_service, mock_memory_service, mock_ai_agent_service):
    """اختبار استعلام الذاكرة باستخدام الذكاء الاصطناعي"""
    # تنفيذ الاختبار
    result = await integration_service.query_memory_with_ai(
        query="ما هي أنواع المحاصيل المناسبة للتربة الطينية؟",
        agent_id="agent1",
        user_id="user1"
    )

    # التحقق من النتائج
    assert result is not None
    assert "memories" in result
    assert "ai_response" in result
    assert len(result["memories"]) > 0
    assert result["ai_response"]["result"] == "معلومات عن المحاصيل الزراعية"

    # التحقق من استدعاء الدوال المتوقعة
    mock_memory_service.search_memories.assert_called_once()
    mock_ai_agent_service.check_agent_capability.assert_called_once_with("agent1", AgentCapability.MEMORY_ACCESS)
    mock_ai_agent_service.process_agent_query.assert_called_once()


@pytest.mark.asyncio
async def test_store_ai_generated_memory(integration_service, mock_memory_service, mock_ai_agent_service):
    """اختبار تخزين ذاكرة منشأة بواسطة الذكاء الاصطناعي"""
    # تنفيذ الاختبار
    memory = await integration_service.store_ai_generated_memory(
        content="المحاصيل المناسبة للتربة الطينية هي القمح والذرة والشعير",
        memory_type=MemoryType.KNOWLEDGE_BASE,
        agent_id="agent1",
        user_id="user1",
        tags=["تربة طينية", "محاصيل"]
    )

    # التحقق من النتائج
    assert memory is not None
    assert memory.id == "mem1"
    assert memory.content == "المحاصيل المناسبة للتربة الطينية هي القمح والذرة والشعير"
    assert memory.memory_type == MemoryType.KNOWLEDGE_BASE

    # التحقق من استدعاء الدوال المتوقعة
    mock_ai_agent_service.check_agent_capability.assert_called_once_with("agent1", AgentCapability.MEMORY_ACCESS)
    mock_memory_service.create_memory.assert_called_once()


@pytest.mark.asyncio
async def test_retrieve_relevant_memories(integration_service, mock_memory_service):
    """اختبار استرجاع الذكريات ذات الصلة"""
    # تنفيذ الاختبار
    memories = await integration_service.retrieve_relevant_memories(
        query="معلومات عن الزراعة والتربة",
        limit=5,
        memory_types=[MemoryType.KNOWLEDGE_BASE, MemoryType.LONG_TERM]
    )

    # التحقق من النتائج
    assert memories is not None
    assert len(memories) == 3
    assert memories[0].id == "mem1"
    assert memories[2].id == "mem3"

    # التحقق من استدعاء الدوال المتوقعة
    mock_memory_service.search_memories.assert_called_once()


@pytest.mark.asyncio
async def test_update_memory_with_ai_insights(integration_service, mock_memory_service, mock_ai_agent_service):
    """اختبار تحديث الذاكرة برؤى الذكاء الاصطناعي"""
    # تنفيذ الاختبار
    updated_memory = await integration_service.update_memory_with_ai_insights(
        memory_id="mem1",
        agent_id="agent1",
        user_id="user1"
    )

    # التحقق من النتائج
    assert updated_memory is not None
    assert updated_memory.id == "mem1"

    # التحقق من استدعاء الدوال المتوقعة
    mock_memory_service.get_memory.assert_called_once_with("mem1")
    mock_ai_agent_service.check_agent_capability.assert_called_once_with("agent1", AgentCapability.MEMORY_ACCESS)
    mock_ai_agent_service.process_agent_query.assert_called_once()
    mock_memory_service.update_memory.assert_called_once()


@pytest.mark.asyncio
async def test_verify_memory_access_permission(integration_service, mock_memory_service, mock_ai_agent_service):
    """اختبار التحقق من صلاحية الوصول إلى الذاكرة"""
    # تهيئة سلوك الدالة الوهمية
    mock_ai_agent_service.check_agent_capability.return_value = True

    # تنفيذ الاختبار
    has_permission = await integration_service.verify_memory_access_permission(
        agent_id="agent1",
        memory_id="mem1",
        user_id="user1",
        access_type="read"
    )

    # التحقق من النتائج
    assert has_permission is True

    # التحقق من استدعاء الدوال المتوقعة
    mock_memory_service.get_memory.assert_called_once_with("mem1")
    mock_ai_agent_service.check_agent_capability.assert_called_once_with("agent1", AgentCapability.MEMORY_ACCESS)


@pytest.mark.asyncio
async def test_get_agent_memory_statistics(integration_service, mock_memory_service, mock_ai_agent_service):
    """اختبار الحصول على إحصائيات ذاكرة الوكيل"""
    # تنفيذ الاختبار
    stats = await integration_service.get_agent_memory_statistics(
        agent_id="agent1",
        user_id="user1"
    )

    # التحقق من النتائج
    assert stats is not None
    assert "total_memories" in stats
    assert "memory_types" in stats
    assert "recent_activity" in stats

    # التحقق من استدعاء الدوال المتوقعة
    mock_ai_agent_service.get_agent.assert_called_once_with("agent1")
    mock_memory_service.search_memories.assert_called_once()


@pytest.mark.asyncio
async def test_sync_agent_memories(integration_service, mock_memory_service, mock_ai_agent_service):
    """اختبار مزامنة ذكريات الوكيل"""
    # تنفيذ الاختبار
    sync_result = await integration_service.sync_agent_memories(
        source_agent_id="agent1",
        target_agent_id="agent2",
        user_id="user1",
        memory_types=[MemoryType.KNOWLEDGE_BASE]
    )

    # التحقق من النتائج
    assert sync_result is not None
    assert "synced_count" in sync_result
    assert "source_agent" in sync_result
    assert "target_agent" in sync_result
    assert sync_result["synced_count"] > 0

    # التحقق من استدعاء الدوال المتوقعة
    mock_ai_agent_service.get_agent.assert_any_call("agent1")
    mock_ai_agent_service.get_agent.assert_any_call("agent2")
    mock_ai_agent_service.check_agent_capability.assert_any_call("agent1", AgentCapability.MEMORY_ACCESS)
    mock_ai_agent_service.check_agent_capability.assert_any_call("agent2", AgentCapability.MEMORY_ACCESS)
    mock_memory_service.search_memories.assert_called_once()
    assert mock_memory_service.create_memory.call_count > 0
