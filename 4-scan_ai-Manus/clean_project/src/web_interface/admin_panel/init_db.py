from app import app, db
from models import User, SystemSettings


def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if setup is already completed
        if not SystemSettings.query.first():
            print("Database initialized successfully!")
            print("Please run the Flask application to start the setup wizard.")
        else:
            print("Setup has already been completed.")


if __name__ == '__main__':
    init_db()
