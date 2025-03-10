import decimal
from datetime import date
from operator import inv
from re import A, M
from webbrowser import get
from sqlalchemy import select, func, asc
from src.web.controllers.payments import invoices
from src.core.payments.invoice import Invoice
from src.core.payments.invoice import InvoiceExtraItem
from src.core.payments.payment import Payment
from src.core.database import db
from src.core.system_config import get_recharge_percentage
from src.core.system_config import get_monthly_fee

EXPIRATION_DAY = 10


def member_invoices(member_id: int):
    """Returns a list of invoices for a given member_id

    Args:
        member_id (int): id of the member

    Returns:
        list: Invoices associated to the member
    """
    return (
        Invoice.query.filter(Invoice.member_id == member_id)
        .order_by(Invoice.year.desc(), Invoice.month.desc())
        .all()
    )


def last_invoice(user_id: int):
    """Returns most recent invoice for a given user_id

    Args:
        user_id (int): if of the user

    Returns:
        Invoice: last invoice created for the user
    """
    return (
        Invoice.query.filter(Invoice.member_id == user_id)
        .order_by(Invoice.year.asc(), Invoice.month.asc())
        .first()
    )


def unpaid_invoices(user_id: int):
    """Returns a list of all unpaid invoices for a given user_id

    Args:
        user_id (int): id of the user

    Returns:
        list: list of Invoices that are not paid yet
    """
    invoices =(Invoice.query.filter_by(
            paid=False).filter(
            Invoice.member_id == user_id).order_by("year", "month").desc().all())
    return invoices

def get_invoice(invoice_id: int):
    """looks up for an invoice based on received id

    Args:
        invoice_id (int): if of the invoice

    Returns:
        Invoice: Invoice from the DB
    """

    inv = Invoice.query.get(invoice_id)
    _check_recharge(inv)
    return inv


def _check_recharge(invoice):
    """Checks if the invoice needs to be recharged and updates it if needed

    Args:
        invoice (Invoice): Invoice to be evaluated
    """
    if date.today().day > EXPIRATION_DAY and not invoice.expired:
        invoice.expired = True
        amount = invoice.total_price * float(get_recharge_percentage())
        description = f"Recargo de {amount} por vencimiento de factura {invoice.month}/{invoice.year}"
        create_extraItem(
            invoice_id=invoice.id,
            amount=amount,
            description=description)
        invoice.total_price = invoice.total_price + amount
        db.session.commit()


def create_invoice(member):
    """Creates a new invoice in the database, adding all disciplines of the member as extra_items

    Args:
        member (Member): member object

    Returns: new_invoice(Invoice)
    """
    base_price = get_monthly_fee()
    invoice = Invoice(
        base_price=base_price,
        member_id=member.id,
        total_price=0)
    db.session.add(invoice)

    total_price = base_price + _calculate_extra_items(member, invoice)
    update_invoice(invoice, total_price=total_price)
    db.session.commit()
    return inv


def _calculate_extra_items(member, invoice):
    """Adds extra items for a given invoice, and returns the total price of the invoice

    Args:
        member (Member): member owner of the invoice
        invoice (Invoice): invoice to be evaluated

    Returns:
       float: amount representing extra fees of the invoice
    """
    sum = 0
    for discipline in member.disciplines:
        if discipline.active:
            amount = discipline.monthly_price
            description = f"Cuota de {discipline.name} por el monto de {amount}"
            create_extraItem(
                discipline_id=discipline.id,
                invoice_id=invoice.id,
                amount=amount,
                description=description)
            sum += int(amount)
    return sum


def create_extraItem(**kwargs):
    """Creates a new extra item for an invoice

    Args:
        invoice_id(int): id of the invoice
        description(string): description of the extra item
        amount(int): amount of the extra item
        discipline_id(int): (optional) id of the discipline

    Returns: new_extra_item(InvoiceExtraItem)
    """
    extra_item = InvoiceExtraItem(**kwargs)
    db.session.add(extra_item)
    db.session.commit()
    return extra_item


def pay_invoice(invoice_id):
    """Creates a new payment for an invoice

    Args:
        invoice(int): id of the invoice

    Returns: new_payment(Payment)
    """
    invoice = get_invoice(invoice_id)
    if invoice.paid:
        return False
    invoice.paid = True
    payment = Payment(
        amount=invoice.total_price,
        invoice_id=invoice.id,
        member_id=invoice.member_id)
    invoice = update_invoice(invoice, paid=True, payment=payment.id)
    db.session.add(payment)
    db.session.commit()
    return payment

def pay_invoice_with_receipt(invoice_id, filename):
    """Creates a new payment for an invoice

    Args:
        invoice_id(int): id of the invoice
        receipt(largeBinary): image of receipt

    Returns: new_payment(Payment)
    """
    invoice = get_invoice(invoice_id)
    if invoice.paid:
        return False
    invoice.paid = True
    payment = Payment(
        amount=invoice.total_price,
        invoice_id=invoice.id,
        member_id=invoice.member_id)
    invoice = update_invoice(invoice, paid=True, payment=payment.id, receipt_photo_name=filename)
    db.session.add(payment)
    db.session.commit()
    return payment    


def amount_paid(invoice_id):
    """Returns the sum of all payments of an invoice for a given invoice_id

    Args:
        invoice_id (int): if of the invoice

    Returns:
        float: amount paid for the given invoice
    """
    return (
        db.session.query(db.func.sum(Payment.amount))
        .filter(Payment.invoice_id == invoice_id)
        .scalar()
    )


def update_invoice(invoice, **kwargs):
    """Updates an invoice given an invoice and a dictionary of parameters

    Args:
        invoice (Invoice): invoice object
        kwargs (dict): dictionary of parameters to update

    Returns:
        Invoice: invoice object
    """
    for key, value in kwargs.items():
        setattr(invoice, key, value)
    db.session.commit()
    return invoice


def member_payments(member_id):
    """Returns a list of payments for a given member_id

    Args:
        member_id (int): if of the member

    Returns:
        list: payments of the received member
    """

    return (
        Payment.query.filter(Payment.member_id == member_id)
        .order_by(Payment.payment_date.desc())
        .all()
    )

def last_year_invoices():
    db_rows = db.session.execute(select(Invoice.month,Invoice.paid, func.count())
        .where(Invoice.year==date.today().year)
        .group_by(Invoice.month, Invoice.paid)
        .order_by(asc(Invoice.month)))

    result = []
    last_month = 0
    for row in db_rows:
        month = row[0]
        paid = row[1]
        count = row[2]
        result.append({ 'month': month, 'paid': paid, 'count': count})
    return result


def get_payment(invoice: int):
    """looks up for an invoice based on received id

    Args:
        invoice_id (int): if of the invoice

    Returns:
        Invoice: Invoice from the DB
    """

    payment = Payment.query.filter(Payment.invoice_id == invoice).first()
    return payment    