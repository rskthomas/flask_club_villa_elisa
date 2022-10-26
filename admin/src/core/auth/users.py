from datetime import datetime
from src.core.database import db


class User(db.Model):
    """User Model representing a user in the system"""

    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship(
        "Role",
        secondary="user_role",
        passive_deletes=True)
    password = db.Column(db.String(50))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        onupdate=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.now())

    def has_role(self, role_id):
        """Checks if the user instance as received role already associated

        Args:
            role_id (int): if of the role to check

        Returns:
            bool: determines if user has the role associated
        """
        matched = None
        for role in self.roles:
            if role.id == role_id:
                matched = role

        return matched is not None
