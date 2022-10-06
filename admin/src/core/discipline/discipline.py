from unicodedata import category
from src.core.database import db

class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    instructors_name = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(50), nullable=True)
    cost = db.Column(db.String(50), nullable=True)
    enabled = db.Column(db.Boolean(), default=True)