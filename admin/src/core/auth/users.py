from src.core.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    active = db.Column(db.Boolean(), default=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
