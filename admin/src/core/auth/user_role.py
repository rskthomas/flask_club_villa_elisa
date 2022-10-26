from src.core.database import db
from sqlalchemy import ForeignKey
from datetime import datetime


class UserRole(db.Model):
    """UserRole Model that links a user to a role"""

    __table_name__ = "user_roles"
    user_id = db.Column(
        db.Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    role_id = db.Column(
        db.Integer, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        onupdate=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.now())
