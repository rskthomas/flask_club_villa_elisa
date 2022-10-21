from flask import Blueprint, request
from src.web.helpers.handlers import bad_request
from src.core.member import get_member_disciplines
from src.web.controllers.api.club import discipline_as_json

from src.core.payments import member_payments



me_api_blueprint = Blueprint("me_api", __name__, url_prefix="/me")

def discipline_as_json(discipline):
    return {
        'id': discipline.id,
        'category': discipline.category,
        'coach' : discipline.coach,
        'schedule': discipline.schedule,
        'monthly_price': discipline.monthly_price,
        'active': discipline.active,
        'created_at': discipline.created_at
    }

def payment_as_json(payment):
    return {
        'id': payment.id,
        'month': payment.invoice.month,
        'amount' : payment.amount,
        'payment_date' : payment.payment_date,
    }

@me_api_blueprint.get('/disciplines')
def disciplines():
    #get id of auth member
    id = 1
    disciplines = get_member_disciplines(1)
    return { 'disciplines': list(map(discipline_as_json, disciplines))}

@me_api_blueprint.get('/payments')
def payments():
    #get id of auth member
    id = 1
    payments = member_payments(1)
    return { 'payments': list(map(payment_as_json, payments))}

