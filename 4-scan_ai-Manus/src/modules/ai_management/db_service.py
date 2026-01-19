"""
from flask import g
خدمة قاعدة البيانات لإدارة الذكاء الصناعي
توفر هذه الوحدة خدمات للتعامل مع قاعدة بيانات وكلاء الذكاء الصناعي وإحصائياتهم وإعداداتهم وصلاحياتهم
"""

from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
import os
import json
import logging
import random

from .db_models import (
    Base, Agent, AgentStat, AISettings, Role, UserRole, AgentRole,
    AIUsageStats, DailyUsage, AIConversation, AIMessage,
    AgentStatus, AgentType, MessageType
)

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for repeated string literals
GPT_35_TURBO_MODEL = "gpt-3.5-turbo"

# إعداد اتصال قاعدة البيانات
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///ai_management.db')

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

# إنشاء الجداول إذا لم تكن موجودة


def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    try:
        Base.metadata.create_all(engine)
        logger.info("تم إنشاء جداول قاعدة البيانات بنجاح")

        # التحقق من وجود بيانات أولية وإضافتها إذا لم تكن موجودة
        session = Session()
        try:
            if session.query(Agent).count() == 0:
                init_default_data(session)
                logger.info("تم إضافة البيانات الافتراضية بنجاح")
        except Exception as e:
            logger.error("خطأ أثناء إضافة البيانات الافتراضية: %s", str(e))
            session.rollback()
        finally:
            session.close()

    except Exception as e:
        logger.error("خطأ أثناء إنشاء قاعدة البيانات: %s", str(e))

# إضافة بيانات افتراضية


def init_default_data(session):
    """إضافة بيانات افتراضية إلى قاعدة البيانات"""

    # إضافة الأدوار
    admin_role = Role(
        id="admin",
        name_ar="مدير",
        name_en="Admin",
        permissions=[
            "manage_agents",
            "view_stats",
            "manage_settings",
            "manage_permissions"])

    manager_role = Role(
        id="manager",
        name_ar="مشرف",
        name_en="Manager",
        permissions=["manage_agents", "view_stats"]
    )

    user_role = Role(
        id="user",
        name_ar="مستخدم",
        name_en="User",
        permissions=["view_agents", "use_agents"]
    )

    session.add_all([admin_role, manager_role, user_role])
    session.flush()

    # إضافة الوكلاء
    main_agent = Agent(
        id="agent1",
        name_ar="الوكيل الرئيسي",
        name_en="Main Agent",
        type=AgentType.SYSTEM,
        model="gpt-4",
        status=AgentStatus.ACTIVE,
        description_ar="الوكيل الرئيسي للنظام",
        description_en="Main system agent",
        avatar="🤖",
        cpu_usage=5,
        ram_usage=120,
        requests_per_minute=10,
        created_at=datetime.now() - timedelta(days=30),
        last_active=datetime.now()
    )

    diagnostic_agent = Agent(
        id="agent2",
        name_ar="وكيل التشخيص",
        name_en="Diagnostic Agent",
        type=AgentType.MODULE,
        model=GPT_35_TURBO_MODEL,
        status=AgentStatus.ACTIVE,
        description_ar="وكيل متخصص في تشخيص الأمراض النباتية",
        description_en="Agent specialized in diagnosing plant diseases",
        avatar="🔍",
        cpu_usage=3,
        ram_usage=80,
        requests_per_minute=5,
        created_at=datetime.now() - timedelta(days=20),
        last_active=datetime.now()
    )

    hybridization_agent = Agent(
        id="agent3",
        name_ar="وكيل التهجين",
        name_en="Hybridization Agent",
        type=AgentType.MODULE,
        model="gpt-4",
        status=AgentStatus.SUSPENDED,
        description_ar="وكيل متخصص في اقتراح عمليات التهجين",
        description_en="Agent specialized in suggesting hybridization processes",
        avatar="🧬",
        cpu_usage=0,
        ram_usage=0,
        requests_per_minute=0,
        created_at=datetime.now()
        - timedelta(
            days=15),
        last_active=datetime.now()
        - timedelta(
            hours=5))

    user_agent = Agent(
        id="agent4",
        name_ar="وكيل المستخدم",
        name_en="User Agent",
        type=AgentType.USER,
        model=GPT_35_TURBO_MODEL,
        status=AgentStatus.ACTIVE,
        description_ar="وكيل مخصص للمستخدم",
        description_en="User-specific agent",
        avatar="👤",
        cpu_usage=2,
        ram_usage=60,
        requests_per_minute=3,
        created_at=datetime.now() - timedelta(days=5),
        last_active=datetime.now()
    )

    session.add_all([main_agent, diagnostic_agent,
                    hybridization_agent, user_agent])
    session.flush()

    # إضافة أدوار المستخدمين
    user_roles = [
        UserRole(user_id="user1", role_id="admin"),
        UserRole(user_id="user2", role_id="manager"),
        UserRole(user_id="user3", role_id="user")
    ]

    session.add_all(user_roles)
    session.flush()

    # إضافة أدوار الوكلاء
    agent_roles = [
        AgentRole(agent_id="agent1", role_id="admin"),
        AgentRole(agent_id="agent2", role_id="manager"),
        AgentRole(agent_id="agent3", role_id="manager"),
        AgentRole(agent_id="agent4", role_id="user")
    ]

    session.add_all(agent_roles)
    session.flush()

    # إضافة إعدادات الذكاء الصناعي
    ai_settings = AISettings(
        default_model="gpt-4",
        memory_retention_days=30,
        log_level="info",
        resource_limits={
            "maxCpuPerAgent": 20,
            "maxRamPerAgent": 500,
            "maxRequestsPerMinute": 30
        },
        auto_suspend={
            "enabled": True,
            "cpuThreshold": 80,
            "ramThreshold": 90,
            "inactivityThreshold": 60
        }
    )

    session.add(ai_settings)
    session.flush()

    # إضافة إحصائيات استخدام الذكاء الصناعي
    ai_usage_stats = AIUsageStats(
        total_requests=15420,
        total_tokens=3250000,
        average_response_time=1.2,
        success_rate=98.5,
        model_usage={
            "gpt-4": 60,
            "gpt-3.5-turbo": 35,
            "other": 5
        }
    )

    session.add(ai_usage_stats)
    session.flush()

    # إضافة بيانات الاستخدام اليومي
    daily_usage_data = []
    for i in range(7):
        day = datetime.now() - timedelta(days=6 - i)
        requests = 2000 + (i * 100) if i < 6 else 1320
        tokens = 400000 + (i * 20000) if i < 6 else 430000

        daily_usage = DailyUsage(
            date=day,
            requests=requests,
            tokens=tokens
        )
        daily_usage_data.append(daily_usage)

    session.add_all(daily_usage_data)
    session.flush()

    # إضافة إحصائيات الوكلاء
    agent_stats = []
    for agent_id in ["agent1", "agent2", "agent4"]:
        for i in range(7):
            day = datetime.now() - timedelta(days=6 - i)
            requests = random.randint(100, 500)
            tokens = requests * 200
            response_time = round(random.uniform(0.5, 2.0), 2)
            success_rate = round(random.uniform(95, 100), 1)

            stat = AgentStat(
                agent_id=agent_id,
                date=day,
                requests=requests,
                tokens=tokens,
                average_response_time=response_time,
                success_rate=success_rate
            )
            agent_stats.append(stat)

    session.add_all(agent_stats)
    session.commit()

# خدمات الوكلاء


def get_all_agents():
    """الحصول على جميع وكلاء الذكاء الصناعي"""
    session = Session()
    try:
        agents = session.query(Agent).all()
        return [agent.to_dict() for agent in agents]
    except SQLAlchemyError:
        logger.error("Database error occurred")
        return []
    finally:
        session.close()


def get_agent_by_id(agent_id):
    """الحصول على وكيل محدد بواسطة المعرف"""
    session = Session()
    try:
        agent = session.query(Agent).filter(Agent.id == agent_id).first()
        return agent.to_dict() if agent else None
    except SQLAlchemyError:
        logger.error("خطأ أثناء استرجاع الوكيل %s", agent_id)
        return None
    finally:
        session.close()


def create_agent(agent_data):
    """إنشاء وكيل جديد"""
    session = Session()
    try:
        # إنشاء معرف فريد
        last_agent = session.query(Agent).order_by(desc(Agent.id)).first()
        last_agent_id = getattr(last_agent, 'id', None)
        if last_agent_id is not None and isinstance(last_agent_id, str) and last_agent_id.startswith('agent'):
            try:
                last_id = int(last_agent_id[5:])
                new_id = f"agent{last_id + 1}"
            except ValueError:
                new_id = f"agent{session.query(Agent).count() + 1}"
        else:
            new_id = "agent1"

        # تحويل النوع والحالة إلى تعدادات
        agent_type = AgentType(agent_data.get('type', 'system'))
        agent_status = AgentStatus(agent_data.get('status', 'active'))

        # إنشاء كائن الوكيل
        agent = Agent(
            id=new_id,
            name_ar=agent_data.get('nameAr', ''),
            name_en=agent_data.get('nameEn', ''),
            type=agent_type,
            model=agent_data.get('model', 'gpt-3.5-turbo'),
            status=agent_status,
            description_ar=agent_data.get('descriptionAr', ''),
            description_en=agent_data.get('descriptionEn', ''),
            avatar=agent_data.get('avatar', '🤖'),
            cpu_usage=0,
            ram_usage=0,
            requests_per_minute=0,
            created_at=datetime.now(),
            last_active=datetime.now()
        )

        session.add(agent)
        session.commit()

        return agent.to_dict()
    except SQLAlchemyError:
        session.rollback()
        logger.error("خطأ أثناء إنشاء وكيل جديد")
        return None
    finally:
        session.close()


def update_agent(agent_id, agent_data):
    """تحديث وكيل موجود"""
    session = Session()
    try:
        agent = session.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return None

        # تحديث البيانات
        if 'nameAr' in agent_data:
            agent.name_ar = agent_data['nameAr']
        if 'nameEn' in agent_data:
            agent.name_en = agent_data['nameEn']
        if 'type' in agent_data:
            setattr(agent, 'type', AgentType(agent_data['type']))
        if 'model' in agent_data:
            agent.model = agent_data['model']
        if 'status' in agent_data:
            setattr(agent, 'status', AgentStatus(agent_data['status']))
        if 'descriptionAr' in agent_data:
            agent.description_ar = agent_data['descriptionAr']
        if 'descriptionEn' in agent_data:
            agent.description_en = agent_data['descriptionEn']
        if 'avatar' in agent_data:
            agent.avatar = agent_data['avatar']
        if 'cpuUsage' in agent_data:
            agent.cpu_usage = agent_data['cpuUsage']
        if 'ramUsage' in agent_data:
            agent.ram_usage = agent_data['ramUsage']
        if 'requestsPerMinute' in agent_data:
            agent.requests_per_minute = agent_data['requestsPerMinute']
        if 'lastActive' in agent_data:
            setattr(agent, 'last_active', datetime.fromisoformat(agent_data['lastActive']))

        session.commit()

        return agent.to_dict()
    except SQLAlchemyError:
        session.rollback()
        logger.error("خطأ أثناء تحديث الوكيل %s", agent_id)
        return None
    finally:
        session.close()


def delete_agent(agent_id):
    """حذف وكيل"""
    session = Session()
    try:
        agent = session.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return None

        agent_dict = agent.to_dict()
        session.delete(agent)
        session.commit()

        return agent_dict
    except SQLAlchemyError:
        session.rollback()
        logger.error("خطأ أثناء حذف الوكيل %s", agent_id)
        return None
    finally:
        session.close()


def change_agent_status(agent_id, status):
    """تغيير حالة وكيل"""
    session = Session()
    try:
        agent = session.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return None

        # تحديث الحالة
        setattr(agent, 'status', AgentStatus(status))

        # تحديث استخدام الموارد بناءً على الحالة
        if status == 'active':
            setattr(agent, 'cpu_usage', random.randint(1, 10))
            setattr(agent, 'ram_usage', random.randint(50, 200))
            setattr(agent, 'requests_per_minute', random.randint(1, 15))
            setattr(agent, 'last_active', datetime.now())
        else:
            setattr(agent, 'cpu_usage', 0)
            setattr(agent, 'ram_usage', 0)
            setattr(agent, 'requests_per_minute', 0)

        session.commit()

        return agent.to_dict()
    except SQLAlchemyError:
        session.rollback()
        logger.error("Database error occurred")
        return None
    finally:
        session.close()

# خدمات الإحصائيات


def get_ai_stats():
    """الحصول على إحصائيات الذكاء الصناعي"""
    session = Session()
    try:
        # الحصول على آخر إحصائيات
        stats = session.query(AIUsageStats).order_by(
            desc(AIUsageStats.date)).first()

        # الحصول على بيانات الاستخدام اليومي
        daily_usage = session.query(DailyUsage).order_by(DailyUsage.date).all()

        if not stats:
            return None

        # تجميع البيانات
        result = {
            "totalRequests": stats.total_requests,
            "totalTokens": stats.total_tokens,
            "averageResponseTime": stats.average_response_time,
            "successRate": stats.success_rate,
            "modelUsage": stats.model_usage,
            "dailyUsage": [usage.to_dict() for usage in daily_usage]
        }

        return result
    except SQLAlchemyError:
        logger.error("Database error occurred")
        return {}
    finally:
        session.close()


def get_model_stats():
    """الحصول على إحصائيات استخدام النماذج"""
    session = Session()
    try:
        stats = session.query(AIUsageStats).order_by(
            desc(AIUsageStats.date)).first()
        return stats.model_usage if stats else {}
    except SQLAlchemyError:
        logger.error("Database error occurred")
        return {}
    finally:
        session.close()


def get_daily_stats():
    """الحصول على إحصائيات الاستخدام اليومي"""
    session = Session()
    try:
        daily_usage = session.query(DailyUsage).order_by(DailyUsage.date).all()
        return [usage.to_dict() for usage in daily_usage]
    except SQLAlchemyError:
        logger.error("Database error occurred")
        return {}
    finally:
        session.close()


def get_agent_stats(agent_id):
    """الحصول على إحصائيات وكيل محدد"""
    session = Session()
    try:
        stats = session.query(AgentStat).filter(
            AgentStat.agent_id == agent_id).order_by(
            AgentStat.date).all()
        return [stat.to_dict() for stat in stats]
    except SQLAlchemyError:
        logger.error("خطأ أثناء استرجاع إحصائيات الوكيل %s", agent_id)
        return []
    finally:
        session.close()

# خدمات الإعدادات


def get_ai_settings():
    """الحصول على إعدادات الذكاء الصناعي"""
    session = Session()
    try:
        settings = session.query(AISettings).first()
        return settings.to_dict() if settings else None
    except SQLAlchemyError:
        logger.error("Database error occurred")
        return {}
    finally:
        session.close()


def update_ai_settings(settings_data):
    """تحديث إعدادات الذكاء الصناعي"""
    session = Session()
    try:
        settings = session.query(AISettings).first()

        if not settings:
            # إنشاء إعدادات جديدة إذا لم تكن موجودة
            settings = AISettings(
                default_model=settings_data.get(
                    'defaultModel',
                    'gpt-3.5-turbo'),
                memory_retention_days=settings_data.get(
                    'memoryRetentionDays',
                    30),
                log_level=settings_data.get(
                    'logLevel',
                    'info'),
                resource_limits=settings_data.get(
                    'resourceLimits',
                    {}),
                auto_suspend=settings_data.get(
                    'autoSuspend',
                    {}))
            session.add(settings)
        else:
            # تحديث الإعدادات الموجودة
            if 'defaultModel' in settings_data:
                settings.default_model = settings_data['defaultModel']
            if 'memoryRetentionDays' in settings_data:
                settings.memory_retention_days = settings_data['memoryRetentionDays']
            if 'logLevel' in settings_data:
                settings.log_level = settings_data['logLevel']
            if 'resourceLimits' in settings_data:
                settings.resource_limits = settings_data['resourceLimits']
            if 'autoSuspend' in settings_data:
                settings.auto_suspend = settings_data['autoSuspend']

            setattr(settings, 'updated_at', datetime.now())

        session.commit()

        return settings.to_dict()
    except SQLAlchemyError:
        session.rollback()
        logger.error("Database error occurred")
        return None
    finally:
        session.close()

# خدمات الصلاحيات


def get_all_permissions():
    """الحصول على جميع بيانات الصلاحيات"""
    session = Session()
    try:
        roles = session.query(Role).all()
        user_roles = session.query(UserRole).all()
        agent_roles = session.query(AgentRole).all()

        result = {
            "roles": [role.to_dict() for role in roles],
            "userRoles": [ur.to_dict() for ur in user_roles],
            "agentRoles": [ar.to_dict() for ar in agent_roles]
        }

        return result
    except SQLAlchemyError:
        logger.error("Database error occurred")
        return {}
    finally:
        session.close()


def get_roles():
    """الحصول على الأدوار"""
    session = Session()
    try:
        roles = session.query(Role).all()
        return [role.to_dict() for role in roles]
    except SQLAlchemyError:
        logger.error("Database error occurred")
        return {}
    finally:
        session.close()


def get_user_roles():
    """الحصول على أدوار المستخدمين"""
    session = Session()
    try:
        user_roles = session.query(UserRole).all()
        return [ur.to_dict() for ur in user_roles]
    except SQLAlchemyError:
        logger.error("Database error occurred")
        return {}
    finally:
        session.close()


def get_agent_roles():
    """الحصول على أدوار الوكلاء"""
    session = Session()
    try:
        agent_roles = session.query(AgentRole).all()
        return [ar.to_dict() for ar in agent_roles]
    except SQLAlchemyError:
        logger.error("Database error occurred")
        return {}
    finally:
        session.close()


def update_permissions(permissions_data):
    """تحديث بيانات الصلاحيات"""
    session = Session()
    try:
        # تحديث الأدوار
        if 'roles' in permissions_data:
            # حذف الأدوار الموجودة
            session.query(Role).delete()

            # إضافة الأدوار الجديدة
            for role_data in permissions_data['roles']:
                role = Role(
                    id=role_data['id'],
                    name_ar=role_data['nameAr'],
                    name_en=role_data['nameEn'],
                    permissions=role_data['permissions']
                )
                session.add(role)

        # تحديث أدوار المستخدمين
        if 'userRoles' in permissions_data:
            # حذف أدوار المستخدمين الموجودة
            session.query(UserRole).delete()

            # إضافة أدوار المستخدمين الجديدة
            for ur_data in permissions_data['userRoles']:
                user_role = UserRole(
                    user_id=ur_data['userId'],
                    role_id=ur_data['roleId']
                )
                session.add(user_role)

        # تحديث أدوار الوكلاء
        if 'agentRoles' in permissions_data:
            # حذف أدوار الوكلاء الموجودة
            session.query(AgentRole).delete()

            # إضافة أدوار الوكلاء الجديدة
            for ar_data in permissions_data['agentRoles']:
                agent_role = AgentRole(
                    agent_id=ar_data['agentId'],
                    role_id=ar_data['roleId']
                )
                session.add(agent_role)

        session.commit()

        return get_all_permissions()
    except SQLAlchemyError:
        session.rollback()
        logger.error("Database error occurred")
        return None
    finally:
        session.close()

# خدمات المحادثات


def get_user_conversations(user_id):
    """الحصول على محادثات مستخدم محدد"""
    session = Session()
    try:
        conversations = session.query(AIConversation).filter(
            AIConversation.user_id == user_id).order_by(
            desc(
                AIConversation.start_time)).all()
        return [conv.to_dict() for conv in conversations]
    except SQLAlchemyError:
        logger.error("خطأ أثناء استرجاع محادثات المستخدم %s: {str(e)}", user_id)
        return []
    finally:
        session.close()


def get_conversation(conversation_id):
    """الحصول على محادثة محددة"""
    session = Session()
    try:
        conversation = session.query(AIConversation).filter(
            AIConversation.id == conversation_id).first()
        return conversation.to_dict() if conversation else None
    except SQLAlchemyError:
        logger.error("خطأ أثناء استرجاع المحادثة %s: {str(e)}", conversation_id)
        return None
    finally:
        session.close()


def create_conversation(user_id, agent_id):
    """إنشاء محادثة جديدة"""
    session = Session()
    try:
        conversation = AIConversation(
            user_id=user_id,
            agent_id=agent_id,
            start_time=datetime.now()
        )

        session.add(conversation)
        session.commit()

        return conversation.to_dict()
    except SQLAlchemyError:
        session.rollback()
        logger.error("Database error occurred")
        return None
    finally:
        session.close()


def add_message(conversation_id, message_type, content, tokens=0):
    """إضافة رسالة إلى محادثة"""
    session = Session()
    try:
        message = AIMessage(
            conversation_id=conversation_id,
            message_type=MessageType(message_type),
            content=content,
            timestamp=datetime.now(),
            tokens=tokens
        )

        session.add(message)

        # تحديث وقت النشاط الأخير للوكيل
        conversation = session.query(AIConversation).filter(
            AIConversation.id == conversation_id).first()
        if conversation:
            agent = session.query(Agent).filter(
                Agent.id == conversation.agent_id).first()
            if agent:
                setattr(agent, 'last_active', datetime.now())

        session.commit()

        return message.to_dict()
    except SQLAlchemyError:
        session.rollback()
        logger.error("Database error occurred")
        return None
    finally:
        session.close()


def end_conversation(conversation_id):
    """إنهاء محادثة"""
    session = Session()
    try:
        conversation = session.query(AIConversation).filter(
            AIConversation.id == conversation_id).first()
        if not conversation:
            return None

        setattr(conversation, 'end_time', datetime.now())
        session.commit()

        return conversation.to_dict()
    except SQLAlchemyError:
        session.rollback()
        logger.error("Database error occurred")
        return None
    finally:
        session.close()

# تحديث الإحصائيات


def update_agent_stats(
        agent_id,
        requests=0,
        tokens=0,
        response_time=0,
        success=True):
    """تحديث إحصائيات وكيل"""
    session = Session()
    try:
        # البحث عن إحصائيات اليوم
        today = datetime.now().date()
        stat = session.query(AgentStat).filter(
            AgentStat.agent_id == agent_id,
            func.date(AgentStat.date) == today
        ).first()

        if not stat:
            # إنشاء إحصائيات جديدة
            stat = AgentStat(
                agent_id=agent_id,
                date=datetime.now(),
                requests=requests,
                tokens=tokens,
                average_response_time=response_time,
                success_rate=100 if success else 0
            )
            session.add(stat)
        else:
            # تحديث الإحصائيات الموجودة
            total_requests = stat.requests + requests
            total_tokens = stat.tokens + tokens

            # حساب متوسط وقت الاستجابة الجديد
            if requests > 0:
                new_avg_time = ((stat.average_response_time * stat.requests)
                                + (response_time * requests)) / total_requests
                setattr(stat, 'average_response_time', new_avg_time)

            # تحديث معدل النجاح
            if success:
                success_count = (
                    stat.success_rate * stat.requests / 100) + requests
                setattr(stat, 'success_rate', (success_count / total_requests) * 100)
            else:
                success_count = (stat.success_rate * stat.requests / 100)
                setattr(stat, 'success_rate', (success_count / total_requests) * 100)

            setattr(stat, 'requests', total_requests)
            setattr(stat, 'tokens', total_tokens)

        # تحديث إحصائيات الاستخدام العامة
        update_global_stats(requests, tokens, response_time, success)

        session.commit()

        return stat.to_dict()
    except SQLAlchemyError:
        session.rollback()
        logger.error("Database error occurred")
        return None
    finally:
        session.close()


def update_global_stats(requests=0, tokens=0, response_time=0, success=True):
    """تحديث الإحصائيات العامة"""
    session = Session()
    try:
        # تحديث إحصائيات الاستخدام اليومي
        today = datetime.now().date()
        daily_usage = session.query(DailyUsage).filter(
            func.date(DailyUsage.date) == today
        ).first()

        if not daily_usage:
            # إنشاء إحصائيات جديدة
            daily_usage = DailyUsage(
                date=datetime.now(),
                requests=requests,
                tokens=tokens
            )
            session.add(daily_usage)
        else:
            # تحديث الإحصائيات الموجودة
            setattr(daily_usage, 'requests', daily_usage.requests + requests)
            setattr(daily_usage, 'tokens', daily_usage.tokens + tokens)

        # تحديث إحصائيات الاستخدام العامة
        stats = session.query(AIUsageStats).order_by(
            desc(AIUsageStats.date)).first()

        if not stats:
            # إنشاء إحصائيات جديدة
            stats = AIUsageStats(
                total_requests=requests,
                total_tokens=tokens,
                average_response_time=response_time,
                success_rate=100 if success else 0,
                model_usage={}
            )
            session.add(stats)
        else:
            # تحديث الإحصائيات الموجودة
            total_requests = stats.total_requests + requests
            total_tokens = stats.total_tokens + tokens

            # حساب متوسط وقت الاستجابة الجديد
            if requests > 0:
                new_avg_time = (
                    (stats.average_response_time * stats.total_requests) + (
                        response_time * requests)) / total_requests
                setattr(stats, 'average_response_time', new_avg_time)

            # تحديث معدل النجاح
            if success:
                success_count = (
                    stats.success_rate * stats.total_requests / 100) + requests
                setattr(stats, 'success_rate', (success_count / total_requests) * 100)
            else:
                success_count = (
                    stats.success_rate * stats.total_requests / 100)
                setattr(stats, 'success_rate', (success_count / total_requests) * 100)

            setattr(stats, 'total_requests', total_requests)
            setattr(stats, 'total_tokens', total_tokens)

        session.commit()

        return True
    except SQLAlchemyError:
        session.rollback()
        logger.error("خطأ أثناء تحديث الإحصائيات العامة")
        return False
    finally:
        session.close()


def update_model_usage(model, requests=1):
    """تحديث إحصائيات استخدام النماذج"""
    session = Session()
    try:
        stats = session.query(AIUsageStats).order_by(
            desc(AIUsageStats.date)).first()

        if not stats:
            # إنشاء إحصائيات جديدة
            model_usage = {model: 100}
            stats = AIUsageStats(
                total_requests=requests,
                total_tokens=0,
                average_response_time=0,
                success_rate=100,
                model_usage=model_usage
            )
            session.add(stats)
        else:
            # تحديث إحصائيات استخدام النماذج
            model_usage = stats.model_usage
            if isinstance(model_usage, dict):
                pass
            elif isinstance(model_usage, str):
                model_usage = json.loads(model_usage)
            elif isinstance(model_usage, bytes):
                model_usage = json.loads(model_usage.decode('utf-8'))
            elif model_usage is None:
                model_usage = {}
            else:
                # fallback: set to empty dict
                model_usage = {}
            # Build a new dict with int values only
            new_model_usage = {}
            for k, v in model_usage.items():
                try:
                    if isinstance(v, bytes):
                        new_model_usage[k] = int(v.decode('utf-8'))
                    else:
                        new_model_usage[k] = int(v)
                except Exception:
                    new_model_usage[k] = 0
            model_usage = new_model_usage

            if model in model_usage:
                model_usage[model] = int(model_usage[model]) + int(requests)
            else:
                model_usage[model] = int(requests)

            # حساب النسب المئوية
            total = sum(model_usage.values())
            for m in model_usage:
                try:
                    model_usage[m] = int(round((model_usage[m] / total) * 100))
                except Exception:
                    model_usage[m] = 0

            setattr(stats, 'model_usage', model_usage)

        session.commit()

        return model_usage
    except SQLAlchemyError:
        session.rollback()
        logger.error("Database error occurred")
        return None
    finally:
        session.close()


# تهيئة قاعدة البيانات
init_db()
