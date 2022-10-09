from src.core.database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship("Role", secondary='user_role',passive_deletes=True)
    password = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.now())

    def has_role(self, role_id):
        matched = None
        for role in self.roles:
            if role.id == role_id:
                matched = role

        return matched != None