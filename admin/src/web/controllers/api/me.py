from flask import Blueprint, request, make_response, jsonify, Flask 
from flask_wtf.csrf import CSRFProtect
from src.web.controllers.api.auth import csrf
from src.core.member import get_member_disciplines, find_member
from src.core.payments import unpaid_invoices, pay_invoice, member_payments

me_api_blueprint = Blueprint("me_api", __name__, url_prefix="/api/me")


@me_api_blueprint.get("/disciplines")
def disciplines():

    id = request.headers["Authorization"]
    if not id:
        return BAD_REQUEST

    response = make_response(
        jsonify([discipline.serialize() for discipline in get_member_disciplines(id)]),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response


@csrf.exempt
@me_api_blueprint.get("/payments")
def payments():
    # TODO: error if id is not found
    id = request.headers["Authorization"]

    if id == "":
        return

    response = make_response(
        jsonify([payment.serialize() for payment in member_payments(id)]), 200
    )
    response.headers["Content-Type"] = "application/json"

    return response


@me_api_blueprint.get("/profile")
def profile():

    id = request.headers["Authorization"]
    member = find_member(id)
    response = make_response(jsonify(member.serialize()), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@me_api_blueprint.post("/payments")
@csrf.exempt
def pay_invoice():
    id = request.headers["Authorization"]
    least_recent_unpaid_invoice = unpaid_invoices(id).first()
    pay_invoice(least_recent_unpaid_invoice)
    amount = least_recent_unpaid_invoice.amount
    response = make_response(jsonify({"amount": amount}), 200)
    response.headers["Content-Type"] = "application/json"

    return response

    def _bad_request(self, msg):
        return jsonify({"msg": msg}), 400
