from src.core.database import db
from datetime import datetime


class Permission(db.Model):
    """Permission Model representing a permission in the system"""

    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=True, unique=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        onupdate=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.now())
