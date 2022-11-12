from datetime import datetime
from src.core.database import db
from src.core.payments import invoice as Invoice


class Member(db.Model):
    """Member Model representing a club member"""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    personal_id_type = db.Column(db.String(25), nullable=False)
    personal_id = db.Column(db.String(25), nullable=False)
    gender = db.Column(db.String(25), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    membership_state = db.Column(db.Boolean(), default=False)
    phone_number = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(50), unique=True)
    activation_date = db.Column(db.DateTime, default=datetime.now())
    invoices = db.relationship(
        "Invoice",
        back_populates="member",
        lazy=True,
        cascade="all, delete-orphan",
        single_parent=True)
    payments = db.relationship("Payment")
    disciplines = db.relationship(
        "Discipline",
        secondary='member_discipline',
        passive_deletes=True,
        back_populates="members")
    profile_photo_name = db.Column(db.String(50), unique=True)

    def fullname(self):
        return self.first_name + " " + self.last_name

    def readable_personal_id(self):
        return self.personal_id_type + ": " + self.personal_id

    def readable_membership_state(self):
        return 'Activo' if self.membership_state else 'Inactivo'
