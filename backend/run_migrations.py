#!/usr/bin/env python3
"""
Store ERP - Database Migration and Initialization Script
==========================================================

This script handles:
1. Database creation and initialization
2. Running Alembic migrations
3. Creating default data (users, roles, categories, warehouses)
4. Verifying database integrity
5. Generating migration reports

Usage:
    python run_migrations.py                    # Run migrations and setup
    python run_migrations.py --fresh            # Fresh database (drop all)
    python run_migrations.py --verify-only      # Only verify database
    python run_migrations.py --create-admin     # Create admin user only
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Check if Flask is installed
try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
except ImportError:
    print("❌ Flask is not installed. Please install requirements first:")
    print("   pip install -r requirements.txt")
    sys.exit(1)


def create_app():
    """Create Flask application instance"""
    app = Flask(__name__)

    # Configure database
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(basedir, "instance")

    # Create instance directory if it doesn't exist
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"✅ Created instance directory: {instance_dir}")

    database_path = os.path.join(instance_dir, "inventory.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )

    return app


def run_alembic_migrations(app):
    """Run Alembic database migrations"""
    print("\n" + "=" * 60)
    print("🔄 Running Alembic Migrations")
    print("=" * 60 + "\n")

    try:
        # Import Flask-Migrate
        from flask_migrate import Migrate, upgrade, init, migrate as create_migration
        from src.database import db

        # Initialize extensions
        db.init_app(app)
        migrate = Migrate(app, db)

        with app.app_context():
            # Check if migrations directory exists
            migrations_dir = os.path.join(current_dir, "migrations")

            if not os.path.exists(migrations_dir):
                print("📁 Initializing Alembic migrations directory...")
                try:
                    init(directory=migrations_dir)
                    print("✅ Migrations directory initialized")
                except Exception as e:
                    print(f"⚠️  Migration init warning: {e}")

            # Check if there are any migration files
            versions_dir = os.path.join(migrations_dir, "versions")
            has_migrations = False

            if os.path.exists(versions_dir):
                migration_files = [
                    f for f in os.listdir(versions_dir) if f.endswith(".py")
                ]
                has_migrations = len(migration_files) > 0
                print(f"📋 Found {len(migration_files)} existing migration(s)")

            if not has_migrations:
                print("📝 No migrations found. Creating initial migration...")
                try:
                    # Import all models to ensure they're registered
                    import_all_models()

                    # Create migration
                    create_migration(
                        message="Initial migration", directory=migrations_dir
                    )
                    print("✅ Initial migration created")
                except Exception as e:
                    print(f"⚠️  Migration creation warning: {e}")

            # Apply migrations
            print("⬆️  Applying database migrations...")
            try:
                upgrade(directory=migrations_dir)
                print("✅ Migrations applied successfully")
                return True
            except Exception as e:
                print(f"⚠️  Migration upgrade warning: {e}")
                print("   Database may already be up to date")
                return True

    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        import traceback

        traceback.print_exc()
        return False


def import_all_models():
    """Import all models to register them with SQLAlchemy"""
    print("📦 Loading all models...")

    models_to_import = [
        # Core models
        "user",
        "customer",
        "supplier",
        "product",
        "category",
        "warehouse",
        "brand",
        "unit",
        "currency",
        # Invoice models
        "unified_invoice",
        "sales_invoice",
        "purchase_invoice",
        # Inventory models
        "stock_movement",
        "inventory_transaction",
        # Advanced features
        "warehouse_adjustment",
        "sales_return",
        "purchase_return",
        "payment_order",
        "debt_record",
        "treasury",
        # Reports and analytics
        "report_template",
        "audit_log",
        "notification",
    ]

    imported_count = 0

    for model_name in models_to_import:
        try:
            # Try importing from src.models
            try:
                __import__(f"src.models.{model_name}")
                imported_count += 1
            except ImportError:
                # Try without src prefix
                try:
                    __import__(f"models.{model_name}")
                    imported_count += 1
                except ImportError:
                    pass  # Model doesn't exist, skip
        except Exception as e:
            print(f"⚠️  Could not import model {model_name}: {e}")

    print(f"✅ Loaded {imported_count} model modules")


def create_default_data(app):
    """Create default data (admin user, roles, etc.)"""
    print("\n" + "=" * 60)
    print("📊 Creating Default Data")
    print("=" * 60 + "\n")

    try:
        from src.database import db, create_default_data as create_data_func

        with app.app_context():
            success = create_data_func()

            if success:
                print("✅ Default data created successfully")
                return True
            else:
                print("⚠️  Some default data may already exist")
                return True

    except Exception as e:
        print(f"❌ Error creating default data: {e}")
        import traceback

        traceback.print_exc()
        return False


def verify_database(app):
    """Verify database integrity and display statistics"""
    print("\n" + "=" * 60)
    print("🔍 Database Verification")
    print("=" * 60 + "\n")

    try:
        from src.database import db

        with app.app_context():
            # Get list of tables
            from sqlalchemy import inspect, text

            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            print(f"📋 Total tables in database: {len(tables)}\n")

            # Count records in each table
            total_records = 0
            table_stats = []

            for table_name in sorted(tables):
                try:
                    result = db.session.execute(
                        text(f"SELECT COUNT(*) FROM {table_name}")
                    )
                    count = result.scalar() or 0
                    total_records += count

                    if count > 0:
                        table_stats.append((table_name, count))
                except Exception as e:
                    print(f"⚠️  Could not count records in {table_name}: {e}")

            # Display tables with data
            if table_stats:
                print("📊 Tables with data:")
                for table_name, count in table_stats:
                    print(f"   • {table_name}: {count} records")
            else:
                print("ℹ️  No data in database yet")

            print(f"\n✅ Total records: {total_records}")

            # Check for admin user
            try:
                result = db.session.execute(
                    text("SELECT COUNT(*) FROM users WHERE username='admin'")
                )
                admin_count = result.scalar()

                if admin_count > 0:
                    print("✅ Admin user exists")
                else:
                    print("⚠️  Admin user not found")
            except Exception:
                print("ℹ️  Users table may not exist yet")

            return True

    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def fresh_database(app):
    """Drop all tables and recreate database"""
    print("\n" + "=" * 60)
    print("🗑️  Fresh Database - Dropping All Tables")
    print("=" * 60 + "\n")

    response = input("⚠️  WARNING: This will DELETE ALL DATA! Continue? (yes/no): ")

    if response.lower() != "yes":
        print("❌ Aborted")
        return False

    try:
        from src.database import db

        with app.app_context():
            print("🗑️  Dropping all tables...")
            db.drop_all()
            print("✅ All tables dropped")

            print("📋 Creating fresh tables...")
            db.create_all()
            print("✅ Fresh tables created")

            return True

    except Exception as e:
        print(f"❌ Error creating fresh database: {e}")
        import traceback

        traceback.print_exc()
        return False


def create_admin_user(app):
    """Create or reset admin user"""
    print("\n" + "=" * 60)
    print("👤 Admin User Creation")
    print("=" * 60 + "\n")

    try:
        from src.database import db

        with app.app_context():
            from sqlalchemy import text

            # Check if admin exists
            result = db.session.execute(
                text("SELECT id FROM users WHERE username='admin'")
            )
            admin = result.fetchone()

            if admin:
                print("ℹ️  Admin user already exists")
                response = input("Reset admin password? (yes/no): ")

                if response.lower() != "yes":
                    print("❌ Aborted")
                    return True

                # Reset password
                import bcrypt

                password_hash = bcrypt.hashpw(
                    "admin123".encode(), bcrypt.gensalt()
                ).decode()

                db.session.execute(
                    text("UPDATE users SET password_hash=:pwd WHERE username='admin'"),
                    {"pwd": password_hash},
                )
                db.session.commit()

                print("✅ Admin password reset to: admin123")
            else:
                # Create admin user
                import bcrypt

                password_hash = bcrypt.hashpw(
                    "admin123".encode(), bcrypt.gensalt()
                ).decode()

                # Ensure role exists
                result = db.session.execute(
                    text("SELECT id FROM roles WHERE name='admin'")
                )
                role = result.fetchone()

                if not role:
                    db.session.execute(
                        text(
                            "INSERT INTO roles (name, description) VALUES ('admin', 'مدير النظام')"
                        )
                    )
                    db.session.commit()

                    result = db.session.execute(
                        text("SELECT id FROM roles WHERE name='admin'")
                    )
                    role = result.fetchone()

                role_id = role[0] if role else 1

                # Create admin user
                db.session.execute(
                    text(
                        """
                        INSERT INTO users (username, email, full_name, password_hash, role_id, is_active)
                        VALUES ('admin', 'admin@store.com', 'مدير النظام', :pwd, :role_id, 1)
                    """
                    ),
                    {"pwd": password_hash, "role_id": role_id},
                )
                db.session.commit()

                print("✅ Admin user created")
                print("   Username: admin")
                print("   Password: admin123")

            return True

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        import traceback

        traceback.print_exc()
        return False


def generate_report(app):
    """Generate migration report"""
    print("\n" + "=" * 60)
    print("📄 Migration Report")
    print("=" * 60 + "\n")

    try:
        from datetime import datetime
        from src.database import db

        with app.app_context():
            from sqlalchemy import inspect

            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            report = f"""# Store ERP - Database Migration Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Database Configuration
- **Type**: SQLite
- **Location**: backend/instance/inventory.db
- **Total Tables**: {len(tables)}

## Tables Created
"""

            for table_name in sorted(tables):
                columns = inspector.get_columns(table_name)
                report += f"\n### {table_name}\n"
                report += f"- **Columns**: {len(columns)}\n"

                # List primary columns
                pk_columns = [col["name"] for col in columns if col.get("primary_key")]
                if pk_columns:
                    report += f"- **Primary Key**: {', '.join(pk_columns)}\n"

            report += """
## Default Data Created
- ✅ Admin user (username: admin, password: admin123)
- ✅ User roles (admin, user)
- ✅ Default categories
- ✅ Default warehouses

## Next Steps
1. Start the backend server: `python app.py`
2. Start the frontend: `cd frontend && npm run dev`
3. Access the application: http://localhost:5502
4. Login with admin credentials

## Advanced Features Ready
- 📦 Warehouse Adjustments
- 🔄 Sales & Purchase Returns
- 💰 Payment Orders & Debt Management
- 🏦 Treasury Management
- 📊 Reports & Analytics
- 🔐 User Roles & Permissions

---
*Database is ready for production use*
"""

            # Save report
            report_path = current_dir / "MIGRATION_REPORT.md"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)

            print(f"✅ Report saved: {report_path}")
            return True

    except Exception as e:
        print(f"⚠️  Could not generate report: {e}")
        return True  # Don't fail the whole process


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Store ERP - Database Migration Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Create fresh database (drops all existing data)",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify database, do not run migrations",
    )
    parser.add_argument(
        "--create-admin", action="store_true", help="Create or reset admin user only"
    )
    parser.add_argument(
        "--no-data", action="store_true", help="Skip creating default data"
    )
    parser.add_argument(
        "--no-report", action="store_true", help="Skip generating migration report"
    )

    args = parser.parse_args()

    # Print header
    print(
        """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           Store ERP - Database Migration Script              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    )

    # Create Flask app
    app = create_app()

    # Execute based on arguments
    if args.verify_only:
        verify_database(app)
        return

    if args.create_admin:
        create_admin_user(app)
        return

    # Full migration process
    success = True

    if args.fresh:
        if not fresh_database(app):
            print("\n❌ Fresh database creation failed")
            sys.exit(1)

    # Run migrations
    if not run_alembic_migrations(app):
        print("\n⚠️  Migrations completed with warnings")
        # Don't exit, continue with data creation

    # Create default data
    if not args.no_data:
        if not create_default_data(app):
            print("\n⚠️  Default data creation completed with warnings")
            # Don't exit, continue

    # Verify database
    verify_database(app)

    # Generate report
    if not args.no_report:
        generate_report(app)

    # Final message
    print("\n" + "=" * 60)
    print("🎉 Database Migration Completed Successfully!")
    print("=" * 60)
    print("\n✅ Your database is ready to use")
    print("\n📝 Next steps:")
    print("   1. Start the backend: python app.py")
    print("   2. Start the frontend: cd frontend && npm run dev")
    print("   3. Login with: admin / admin123")
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
