from src.core.payments.invoice import Invoice
from src.core.payments.payment import Payment
from src.core.database import db


def user_invoices(user_id):
    """Get all invoices for a given user_id"""

    return (
        Invoice.query.filter_by(member_id=user_id)
        .order_by(Invoice.year.desc(), Invoice.month.desc())
        .all()
    )


def lastInvoice(user_id):
    """Get last invoice for a given user_id"""

    return (
        Invoice.query.filter_by(member_id=user_id)
        .order_by(Invoice.year.desc(), Invoice.month.desc())
        .last()
    )


def unpaidInvoices(user_id):
    """Get all unpaid invoices for a given user_id"""
    return Invoice.query.filter_by(paid=False).filter_by(member_id=user_id).all()


def generateInvoice(**kwargs):
    """Generate invoice"""
    inv = Invoice(**kwargs)
    db.session.add(inv)
    db.session.commit()


def payInvoice():
    #TODO: set invoice to paid and add payment to db
    pass
