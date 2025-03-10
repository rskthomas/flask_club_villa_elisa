from operator import inv
from src.core.database import db


class Payment(db.Model):
    """Payment model"""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    invoice_id = db.Column(
        db.Integer,
        db.ForeignKey('invoice.id'),
        nullable=False)
    invoice = db.relationship("Invoice", back_populates="payment")
    member_id = db.Column(
        db.Integer,
        db.ForeignKey('member.id'),
        nullable=False)
    amount = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.DateTime(), default=db.func.now())

    def serialize(self): return {
        'id': self.id,
        'month': self.invoice.month,
        'amount': self.amount,
        'payment_date': self.payment_date,
    }