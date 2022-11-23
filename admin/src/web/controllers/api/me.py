from flask import Blueprint, request, make_response, jsonify, Flask
from src.core.member import get_member_disciplines, find_member
from src.core.payments import unpaid_invoices, pay_invoice, member_payments
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.web.controllers.api.auth import getMemberId, BAD_MEMBER_RESPONSE

me_api_blueprint = Blueprint("me_api", __name__, url_prefix="/api/me")

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
    if not id:
        return jsonify(BAD_MEMBER_RESPONSE), 401
    
    response = make_response(
        jsonify([payment.serialize() for payment in member_payments(id)]), 200
    )
    response.headers["Content-Type"] = "application/json"

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
    if not id:
        return jsonify(BAD_MEMBER_RESPONSE), 401
    
    least_recent_unpaid_invoice = unpaid_invoices(id).first()
    pay_invoice(least_recent_unpaid_invoice)
    amount = least_recent_unpaid_invoice.amount
    response = make_response(jsonify({"amount": amount}), 200)
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
            
    response.headers["Content-Type"] = "application/json"
    return response
