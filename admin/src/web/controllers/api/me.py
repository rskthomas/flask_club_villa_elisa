from flask import Blueprint, request, make_response, jsonify, Flask
from src.core.member import get_member_disciplines, find_member
from src.core.payments import unpaid_invoices, pay_invoice as pay__invoice, member_payments, member_invoices
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.web.controllers.api.auth import getMemberId, BAD_MEMBER_RESPONSE
from src.web.controllers.api import apply_CORS
from src.core import auth
from src.core import member

me_api_blueprint = Blueprint("me_api", __name__, url_prefix="/api/me")



def payment_as_json(payment):
    """Converts a payment to json and returns it"""
    return {
        'id': payment.id,
        'month': payment.invoice.month,
        'amount': payment.amount,
        'payment_date': payment.payment_date,
        'paid': payment.invoice.paid
    }


@me_api_blueprint.get("/disciplines")
@jwt_required()
def disciplines():
    """Returns a list of all disciplines (JSON) of currently logged member"""
    
    id = getMemberId( get_jwt_identity() )
    if not id:
        return jsonify(BAD_MEMBER_RESPONSE), 401
        #TODO?: IF USER IS NOT A MEMBER, AND AN ADMIN IS LOGGED IN, THEN LOG OUT?
        #MAYBE THIS CAN BE DONE ON THE JWT_REQUIRED DECORATOR?
    
    response = make_response(
        jsonify([discipline.serialize() for discipline in get_member_disciplines(id)]),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response


@me_api_blueprint.get("/payments")
@jwt_required()
def payments():
    """Returns a list of all payments (JSON) of currently logged member"""
    id = getMemberId( get_jwt_identity() )
    print("id: ", id)
    if not id:
        return jsonify(BAD_MEMBER_RESPONSE), 401
    
    response = make_response(
        jsonify([invoice.serialize() for invoice in member_invoices(id)]), 200
    )

    return response


@me_api_blueprint.get("/profile")
@jwt_required()
def profile():
    """Returns a JSON with the logged member's profile"""

    id = getMemberId( get_jwt_identity() )
    if not id:
        return jsonify(BAD_MEMBER_RESPONSE), 401
    
    member = find_member(id)
    response = make_response(jsonify(member.serialize()), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@me_api_blueprint.post("/payments")
@jwt_required()
def pay_invoice():
    
    id = getMemberId( get_jwt_identity() )
    print(id)

    content = request.json
    invoiceId = content['invoiceId']

    if not id:
        return jsonify(BAD_MEMBER_RESPONSE), 401
    
    payment= pay__invoice(invoiceId)
    response = make_response(jsonify({"amount": payment.amount}), 200)

    response.headers["Content-Type"] = "application/json"

    return response


@me_api_blueprint.get("/license")
@jwt_required()
def license():

    id = getMemberId( get_jwt_identity() )
    if not id:
        return jsonify(BAD_MEMBER_RESPONSE), 401
    
    member = find_member(id)
    response = make_response(jsonify(
        status= member.readable_membership_state(),
        description = member.readable_membership_description(),
        profile= member.serialize()
        ), 200)
            
    return response

@me_api_blueprint.after_request
def cors_HEADERS(response):
    return apply_CORS(response)