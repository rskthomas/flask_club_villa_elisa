from datetime import datetime
from email.policy import default
from src.core.database import db


class SystemConfig(db.Model):
    """SystemConfig Model represents the global system config in the system"""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    items_qty_for_grids = db.Column(db.Integer, default=1)
    public_payments_available = db.Column(db.Boolean(), default=False)
    public_contact_info_available = db.Column(db.Boolean(), default=False)
    payment_header_text = db.Column(db.String(250), nullable=True)
    base_monthly_fee = db.Column(db.Numeric, default=120)
    delayed_payment_interests_rate = db.Column(db.Numeric, default=0.1)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        onupdate=datetime.now())
    inserted_at = db.Column(db.DateTime, default=datetime.now())
