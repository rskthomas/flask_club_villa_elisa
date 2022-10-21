from unicodedata import category
from src.core.database import db

class Discipline(db.Model):
    """Discipline model"""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    coach = db.Column(db.String(50), nullable=True)
    schedule = db.Column(db.String(50), nullable=True)
    monthly_price = db.Column(db.String(50), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=True)
    created_at = db.Column(db.DateTime(), default=db.func.now())
    members = db.relationship("Member", secondary='member_discipline',passive_deletes=True)