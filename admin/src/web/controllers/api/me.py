from flask import Blueprint, request, make_response, jsonify
from src.web.helpers.handlers import bad_request
from src.core.member import get_member_disciplines, find_member
from src.core.payments import unpaid_invoices, pay_invoice
from src.web.controllers.api.club import discipline_as_json
from src.web.controllers.api.members import member_as_json
from src.core.payments import member_payments

me_api_blueprint = Blueprint("me_api", __name__, url_prefix="/me")

def payment_as_json(payment):
    """Converts a payment to json and returns it"""
    return {
        'id': payment.id,
        'month': payment.invoice.month,
        'amount': payment.amount,
        'payment_date': payment.payment_date,
    }


@me_api_blueprint.get('/disciplines')
def disciplines():
    
    id = request.headers['Authorization']
    disciplines = get_member_disciplines(id)
    response = make_response(jsonify({'disciplines': list(map(discipline_as_json, disciplines))}), 200)
    response.headers['Content-Type'] = 'application/json'

    return response


@me_api_blueprint.get('/payments')
def payments():
    id = request.headers['Authorization']
    payments = member_payments(id)
    response = make_response(jsonify({'payments': list(map(payment_as_json, payments))}), 200)
    response.headers['Content-Type'] = 'application/json'

    return response

@me_api_blueprint.get('/profile')
def profile():
    
    id = request.headers['Authorization']
    member = find_member(id)
    response = make_response(jsonify({'member': member_as_json(member)}), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@me_api_blueprint.post('/payments')
def pay_invoice():
    id = request.headers['Authorization']
    least_recent_unpaid_invoice = unpaid_invoices(id).first()
    pay_invoice(least_recent_unpaid_invoice)
    amount= least_recent_unpaid_invoice.amount
    response = make_response(jsonify({'amount': amount}), 200)
    response.headers['Content-Type'] = 'application/json'

    return response
