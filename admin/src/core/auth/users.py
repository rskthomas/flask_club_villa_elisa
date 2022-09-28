from src.core import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    document_number = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('male', 'female', 'other', name='varchar'))
    address = db.Column(db.String(100), unique=True, optional=True)
    active= db.Column(db.Boolean(), default=False)
    phone = db.Column(db.String(50), nullable=False, optional=True)
    email = db.Column(db.String(50), unique=True, optional=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    

