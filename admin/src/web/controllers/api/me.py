from flask import Blueprint, request, make_response, jsonify
from src.web.helpers.handlers import bad_request
from src.core.member import get_member_disciplines, find_member
from src.core.payments import unpaid_invoices, pay_invoice
from src.web.controllers.api.club import discipline_as_json
from src.web.controllers.api.members import member_as_json
from src.core.payments import member_payments
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.core import auth
from src.core import member

me_api_blueprint = Blueprint("me_api", __name__, url_prefix="/me")

def payment_as_json(payment):
    """Converts a payment to json and returns it"""
    return {
        'id': payment.id,
        'month': payment.invoice.month,
        'amount': payment.amount,
        'payment_date': payment.payment_date,
        'paid': payment.invoice.paid
    }


@me_api_blueprint.get('/disciplines')
def disciplines():
    id = request.headers['Authorization']
    disciplines = get_member_disciplines(id)
    response = make_response(jsonify({'disciplines': list(map(discipline_as_json, disciplines))}), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@me_api_blueprint.get('/payments')
@jwt_required()
def payments():
    # get identity to obtain the user logged
    current_user = get_jwt_identity()
    user = auth.find_user(current_user)
    if user:
        # With mail of user obtain the member
        email = user.email
        mem = member.find_member_by_mail(email)
        if mem:
            # With the member obtain all payments
            payments = member_payments(mem.id)
            response = make_response(
                jsonify([payment_as_json(payment) for payment in payments]), 200
            )
            response.headers['Content-Type'] = 'application/json'       
            return response
        else:
            return jsonify({"msg": "The user isn't a memeber"}), 401    
    else:
        return jsonify({"msg": "Bad username or password"}), 401    
    

@me_api_blueprint.get('/profile')
def profile():
    id = request.headers['Authorization']
    member = find_member(id)
    response = make_response(jsonify({'member': member_as_json(member)}), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@me_api_blueprint.post('/payments')
@jwt_required()
def pay_invoice():
    current_user = get_jwt_identity()
    print(current_user)
    id = current_user

    content = request.json
    file = content['file']
    invoiceId = content['invoiceId']
    print(invoiceId)


    '''least_recent_unpaid_invoice = unpaid_invoices(id).first()
    pay_invoice(least_recent_unpaid_invoice)
    amount= least_recent_unpaid_invoice.amount
    '''
    response = make_response(jsonify({'amount': 200}), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
