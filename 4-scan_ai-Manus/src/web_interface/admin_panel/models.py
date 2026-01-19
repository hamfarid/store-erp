from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'


class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(10), nullable=False, default='ar')
    timezone = db.Column(db.String(50), nullable=False, default='UTC')
    date_format = db.Column(db.String(20), nullable=False, default='%Y-%m-%d')
    session_timeout = db.Column(db.Integer, nullable=False, default=30)
    max_login_attempts = db.Column(db.Integer, nullable=False, default=5)
    password_expiry = db.Column(db.Integer, nullable=False, default=90)
    enable_2fa = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SystemSettings {self.system_name}>'

    @classmethod
    def get_settings(cls):
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings
