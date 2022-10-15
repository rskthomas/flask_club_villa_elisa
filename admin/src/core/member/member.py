from datetime import datetime
from src.core.database import db
from src.core.payments import invoice as Invoice

class Member(db.Model):
    id                  = db.Column(db.Integer, primary_key=True, unique=True)
    first_name          = db.Column(db.String(50), nullable=True)
    last_name           = db.Column(db.String(50), nullable=True)
    personal_id_type    = db.Column(db.Integer, nullable=False)
    personal_id         = db.Column(db.Integer, nullable=False)
    gender              = db.Column(db.String(50), nullable=True)
    member_number       = db.Column(db.Integer, nullable=True)
    address             = db.Column(db.String(255), nullable=True)
    membership_state    = db.Column(db.Boolean(), default=True)
    phone_number        = db.Column(db.Integer, nullable=True)
    email               = db.Column(db.String(50), unique=True)
    activation_date     = db.Column(db.DateTime, default=datetime.now())
    invoices            = db.relationship("Invoice", backref="member", lazy=True, cascade="all, delete-orphan", single_parent=True)

