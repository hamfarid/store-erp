"""Check users in database"""

from app import create_app
from src.models.user import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"\n=== USER CHECK ===")
    print(f"Total users: {len(users)}")
    for u in users:
        print(
            f'User: {u.username}, Email: {u.email}, Active: {u.is_active}, Role: {u.role.name if u.role else "None"}'
        )
