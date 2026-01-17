import sys
import os

# Ensure backend imports work
sys.path.append('backend')
sys.path.append('backend/src')

from app import create_app  # type: ignore
from src.database import db  # type: ignore

try:
    from src.models.user_unified import User, Role  # type: ignore
except Exception as e:  # noqa
    print(f"IMPORT_ERROR: {e}")
    raise


def main():
    app = create_app()
    with app.app_context():
        # Ensure default 'user' role exists if using unified models
        role_id_value = None
        try:
            # If Role table exists, ensure 'user' role
            default_role = None
            try:
                default_role = Role.query.filter_by(name='user').first()  # type: ignore[attr-defined]
            except Exception:
                default_role = None
            if default_role is None:
                try:
                    r = Role(name='user', display_name='User', description='Normal user')  # type: ignore[call-arg]
                    db.session.add(r)
                    db.session.commit()
                    role_id_value = r.id
                except Exception:
                    db.session.rollback()
                    role_id_value = None
            else:
                role_id_value = default_role.id
        except Exception:
            role_id_value = None

        # Check existing user
        existing = User.query.filter_by(username='gaara').first()  # type: ignore[attr-defined]
        if existing:
            print('EXISTS')
            return 0

        # Create user
        user = User()  # type: ignore[call-arg]
        user.username = 'gaara'  # type: ignore[assignment]
        # Optional fields if model supports them
        for attr, val in [('email',''), ('full_name',''), ('phone','')]:
            if hasattr(user, attr):
                setattr(user, attr, val)
        if hasattr(user, 'is_active'):
            user.is_active = True  # type: ignore[assignment]

        # Assign role
        if role_id_value is not None and hasattr(user, 'role_id'):
            user.role_id = role_id_value  # type: ignore[assignment]
        elif hasattr(user, 'role'):
            user.role = 'user'  # type: ignore[assignment]

        # Set password
        user.set_password('456789+9')  # type: ignore[attr-defined]

        db.session.add(user)
        db.session.commit()
        print('CREATED')
        return 0


if __name__ == '__main__':
    raise SystemExit(main())

