"""
تكامل الصلاحيات مع وكلاء الذكاء الاصطناعي

يوفر هذا الملف وظائف للتحقق من صلاحيات وكلاء الذكاء الاصطناعي وإدارتها.
"""

from typing import List

from sqlalchemy.orm import Session

from src.modules.ai_agent.schemas import AgentResponse
from src.modules.ai_agent.service import AgentService
from src.modules.permissions.schemas import PermissionResponse
from src.modules.permissions.service import PermissionService

PERMISSION_CREATE_AGENT = "agent:create"
PERMISSION_READ_AGENT = "agent:read"
PERMISSION_UPDATE_AGENT = "agent:update"
PERMISSION_EXECUTE_AGENT = "agent:execute"
PERMISSION_CONFIGURE_AGENT = "agent:configure"
PERMISSION_VIEW_LOGS = "agent:view_logs"
PERMISSION_MANAGE_MEMORY = "agent:manage_memory"
PERMISSION_MANAGE_TOOLS = "agent:manage_tools"

# قائمة الصلاحيات الكاملة
ALL_PERMISSIONS = [
    PERMISSION_CREATE_AGENT,
    PERMISSION_READ_AGENT,
    PERMISSION_UPDATE_AGENT,
    PERMISSION_EXECUTE_AGENT,
    PERMISSION_CONFIGURE_AGENT,
    PERMISSION_VIEW_LOGS,
    PERMISSION_MANAGE_MEMORY,
    PERMISSION_MANAGE_TOOLS
]


def _check_user_permissions(
    permission_service: PermissionService,
    user_id: str,
    permissions: List[str]
) -> List[str]:
    """
    التحقق من صلاحيات المستخدم

    المعلمات:
        permission_service (PermissionService): خدمة الصلاحيات
        user_id (str): معرف المستخدم
        permissions (List[str]): قائمة الصلاحيات للتحقق منها

    العوائد:
        List[str]: قائمة الصلاحيات التي يملكها المستخدم
    """
    return [
        permission for permission in permissions
        if permission_service.has_permission(user_id, permission)
    ]


def check_agent_permission(
    db: Session,
    user_id: str,
    agent_id: str,
    permission: str
) -> bool:
    """
    التحقق من صلاحية المستخدم على الوكيل

    المعلمات:
        db (Session): جلسة قاعدة البيانات
        user_id (str): معرف المستخدم
        agent_id (str): معرف الوكيل
        permission (str): الصلاحية المطلوبة

    العوائد:
        bool: True إذا كان المستخدم لديه الصلاحية، False إذا لم يكن لديه
    """
    permission_service = PermissionService(db)
    agent_service = AgentService(db)

    # التحقق من وجود الوكيل
    agent = agent_service.get_agent(agent_id)
    if not agent:
        return False

    # التحقق من ملكية الوكيل
    if agent.owner_id == user_id:
        return True

    # التحقق من الصلاحيات
    return permission_service.has_permission(
        user_id, permission)  # pylint: disable=no-member


def get_agent_permissions(
    db: Session,
    user_id: str,
    agent_id: str
) -> List[PermissionResponse]:
    """
    الحصول على صلاحيات المستخدم على الوكيل

    المعلمات:
        db (Session): جلسة قاعدة البيانات
        user_id (str): معرف المستخدم
        agent_id (str): معرف الوكيل

    العوائد:
        List[PermissionResponse]: قائمة الصلاحيات
    """
    permission_service = PermissionService(db)
    agent_service = AgentService(db)

    # التحقق من وجود الوكيل
    agent = agent_service.get_agent(agent_id)
    if not agent:
        return []

    # الحصول على الصلاحيات
    if agent.owner_id == user_id:
        permissions = ALL_PERMISSIONS
    else:
        permissions = _check_user_permissions(
            permission_service, user_id, ALL_PERMISSIONS)

    return [PermissionResponse(name=p) for p in permissions]


def grant_agent_permission(
    db: Session,
    user_id: str,
    agent_id: str,
    permission: str
) -> bool:
    """
    منح صلاحية للمستخدم على الوكيل

    المعلمات:
        db (Session): جلسة قاعدة البيانات
        user_id (str): معرف المستخدم
        agent_id (str): معرف الوكيل
        permission (str): الصلاحية المطلوبة

    العوائد:
        bool: True إذا تم منح الصلاحية بنجاح، False إذا لم يتم
    """
    permission_service = PermissionService(db)
    agent_service = AgentService(db)

    # التحقق من وجود الوكيل
    agent = agent_service.get_agent(agent_id)
    if not agent:
        return False

    # التحقق من ملكية الوكيل
    if agent.owner_id != user_id:
        return False

    # منح الصلاحية
    return permission_service.grant_permission(
        user_id, permission)  # pylint: disable=no-member


def revoke_agent_permission(
    db: Session,
    user_id: str,
    agent_id: str,
    permission: str
) -> bool:
    """
    إلغاء صلاحية المستخدم على الوكيل

    المعلمات:
        db (Session): جلسة قاعدة البيانات
        user_id (str): معرف المستخدم
        agent_id (str): معرف الوكيل
        permission (str): الصلاحية المطلوبة

    العوائد:
        bool: True إذا تم إلغاء الصلاحية بنجاح، False إذا لم يتم
    """
    permission_service = PermissionService(db)
    agent_service = AgentService(db)

    # التحقق من وجود الوكيل
    agent = agent_service.get_agent(agent_id)
    if not agent:
        return False

    # التحقق من ملكية الوكيل
    if agent.owner_id != user_id:
        return False

    # إلغاء الصلاحية
    return permission_service.revoke_permission(
        user_id, permission)  # pylint: disable=no-member


def get_agent_users(
    db: Session,
    agent_id: str
) -> List[str]:
    """
    الحصول على قائمة المستخدمين الذين لديهم صلاحيات على الوكيل

    المعلمات:
        db (Session): جلسة قاعدة البيانات
        agent_id (str): معرف الوكيل

    العوائد:
        List[str]: قائمة معرفات المستخدمين
    """
    permission_service = PermissionService(db)
    agent_service = AgentService(db)

    # التحقق من وجود الوكيل
    agent = agent_service.get_agent(agent_id)
    if not agent:
        return []

    # الحصول على المستخدمين
    users = [agent.owner_id]
    for permission in ALL_PERMISSIONS:
        users.extend(permission_service.get_users_with_permission(permission))

    return list(set(users))


def get_user_agents(
    db: Session,
    user_id: str
) -> List[AgentResponse]:
    """
    الحصول على قائمة الوكلاء التي لدى المستخدم صلاحيات عليها

    المعلمات:
        db (Session): جلسة قاعدة البيانات
        user_id (str): معرف المستخدم

    العوائد:
        List[AgentResponse]: قائمة الوكلاء
    """
    agent_service = AgentService(db)

    # الحصول على الوكلاء التي يملكها المستخدم
    owned_agents = agent_service.get_user_agents(user_id)

    # الحصول على الوكلاء التي لدى المستخدم صلاحيات عليها
    permission_service = PermissionService(db)
    agents_with_permissions = []
    for agent in agent_service.get_all_agents():
        if any(permission_service.has_permission(user_id, permission)
               for permission in ALL_PERMISSIONS):  # pylint: disable=no-member
            agents_with_permissions.append(agent)

    # دمج القوائم وإزالة التكرار
    all_agents = owned_agents + agents_with_permissions
    return list({agent.id: agent for agent in all_agents}.values())
