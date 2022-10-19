from src.core.database import db
from datetime import date

class Invoice(db.Model):
    """Invoice model"""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    year = db.Column(db.Integer(), nullable=False, default=date.today().year)
    month = db.Column(db.Integer(), nullable=False, default=date.today().month)
    base_price = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.String(50), nullable=False)
    paid = db.Column(db.Boolean(), default=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    member = db.relationship("Member", back_populates="invoices")
    expired = db.Column(db.Boolean(), default=False)
    payments = db.relationship("Payment")
    extra_items = db.relationship("InvoiceExtraItem")

class InvoiceExtraItem(db.Model):
    """Invoice extra item model"""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    description = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.DateTime(), default=db.func.now())
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    