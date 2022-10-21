from src.core.database import db
from sqlalchemy import ForeignKey
from datetime import datetime


class RolePermission(db.Model):
    """RolePermission Model that links a role to a permission"""

    __tablename__ = "role_permissions"
    permission_id = db.Column(
        db.Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
    )
    role_id = db.Column(
        db.Integer, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True
    )
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.now())
