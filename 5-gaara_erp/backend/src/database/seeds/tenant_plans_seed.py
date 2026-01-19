"""
Tenant Plans Seed Data
بيانات بذرة خطط المستأجرين

This script seeds the default subscription plans for Gaara ERP.

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17

Usage:
    python -m src.database.seeds.tenant_plans_seed
"""

from __future__ import annotations

import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


# Default plans configuration
DEFAULT_PLANS = [
    {
        "code": "free",
        "name": "Free",
        "name_ar": "مجاني",
        "plan_type": "free",
        "max_users": 5,
        "max_storage_gb": 1,
        "max_api_calls_per_day": 1000,
        "max_modules": 5,
        "features": {
            "basic_accounting": True,
            "basic_inventory": True,
            "basic_sales": True,
            "basic_reports": True,
            "email_support": True,
            "api_access": False,
            "custom_domain": False,
            "advanced_reports": False,
            "ai_features": False,
            "priority_support": False,
        },
        "price_monthly": Decimal("0"),
        "price_yearly": Decimal("0"),
        "currency": "SAR",
        "is_active": True,
    },
    {
        "code": "basic",
        "name": "Basic",
        "name_ar": "أساسي",
        "plan_type": "basic",
        "max_users": 10,
        "max_storage_gb": 10,
        "max_api_calls_per_day": 5000,
        "max_modules": 10,
        "features": {
            "basic_accounting": True,
            "basic_inventory": True,
            "basic_sales": True,
            "basic_reports": True,
            "advanced_reports": True,
            "email_support": True,
            "api_access": True,
            "custom_domain": False,
            "ai_features": False,
            "priority_support": False,
        },
        "price_monthly": Decimal("99"),
        "price_yearly": Decimal("990"),
        "currency": "SAR",
        "is_active": True,
    },
    {
        "code": "pro",
        "name": "Professional",
        "name_ar": "احترافي",
        "plan_type": "pro",
        "max_users": 50,
        "max_storage_gb": 50,
        "max_api_calls_per_day": 50000,
        "max_modules": 50,
        "features": {
            "basic_accounting": True,
            "basic_inventory": True,
            "basic_sales": True,
            "basic_reports": True,
            "advanced_reports": True,
            "advanced_accounting": True,
            "advanced_inventory": True,
            "hr_module": True,
            "crm_module": True,
            "email_support": True,
            "phone_support": True,
            "api_access": True,
            "custom_domain": True,
            "ai_features": True,
            "priority_support": True,
        },
        "price_monthly": Decimal("499"),
        "price_yearly": Decimal("4990"),
        "currency": "SAR",
        "is_active": True,
    },
    {
        "code": "enterprise",
        "name": "Enterprise",
        "name_ar": "مؤسسي",
        "plan_type": "enterprise",
        "max_users": 9999,
        "max_storage_gb": 500,
        "max_api_calls_per_day": 500000,
        "max_modules": 999,
        "features": {
            "all_modules": True,
            "basic_accounting": True,
            "basic_inventory": True,
            "basic_sales": True,
            "basic_reports": True,
            "advanced_reports": True,
            "advanced_accounting": True,
            "advanced_inventory": True,
            "hr_module": True,
            "crm_module": True,
            "agricultural_modules": True,
            "ai_modules": True,
            "email_support": True,
            "phone_support": True,
            "dedicated_support": True,
            "api_access": True,
            "custom_domain": True,
            "white_label": True,
            "ai_features": True,
            "priority_support": True,
            "sla_guarantee": True,
            "custom_development": True,
        },
        "price_monthly": Decimal("1999"),
        "price_yearly": Decimal("19990"),
        "currency": "SAR",
        "is_active": True,
    },
]


def seed_plans(db_session=None):
    """
    Seed default subscription plans.

    Args:
        db_session: SQLAlchemy session (optional, will create if not provided)

    Returns:
        int: Number of plans created
    """
    try:
        # Import models
        from src.models.tenant_sqlalchemy import TenantPlan

        # Get or create session
        if db_session is None:
            from src.models.user import db
            db_session = db.session

        created_count = 0

        for plan_data in DEFAULT_PLANS:
            # Check if plan exists
            existing = db_session.query(TenantPlan).filter_by(code=plan_data["code"]).first()

            if existing:
                logger.info(f"Plan '{plan_data['code']}' already exists, skipping...")
                continue

            # Create new plan
            plan = TenantPlan(**plan_data)
            db_session.add(plan)
            created_count += 1
            logger.info(f"Created plan: {plan_data['name']} ({plan_data['code']})")

        db_session.commit()
        logger.info(f"Seeding complete. Created {created_count} plans.")

        return created_count

    except Exception as e:
        logger.error(f"Error seeding plans: {e}", exc_info=True)
        if db_session:
            db_session.rollback()
        raise


def delete_all_plans(db_session=None):
    """
    Delete all plans (use with caution!).

    Args:
        db_session: SQLAlchemy session
    """
    try:
        from src.models.tenant_sqlalchemy import TenantPlan

        if db_session is None:
            from src.models.user import db
            db_session = db.session

        count = db_session.query(TenantPlan).delete()
        db_session.commit()
        logger.info(f"Deleted {count} plans")
        return count

    except Exception as e:
        logger.error(f"Error deleting plans: {e}", exc_info=True)
        if db_session:
            db_session.rollback()
        raise


def get_plan_by_code(code: str, db_session=None):
    """
    Get a plan by its code.

    Args:
        code: Plan code (e.g., 'pro')
        db_session: SQLAlchemy session

    Returns:
        TenantPlan or None
    """
    try:
        from src.models.tenant_sqlalchemy import TenantPlan

        if db_session is None:
            from src.models.user import db
            db_session = db.session

        return db_session.query(TenantPlan).filter_by(code=code, is_active=True).first()

    except Exception as e:
        logger.error(f"Error getting plan: {e}")
        return None


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    print("=" * 50)
    print("Gaara ERP - Tenant Plans Seeder")
    print("=" * 50)

    try:
        count = seed_plans()
        print(f"\n✅ Successfully seeded {count} plans")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
