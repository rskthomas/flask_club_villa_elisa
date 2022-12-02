import os.path
import re
from flask import Blueprint, request, make_response, jsonify, current_app
from src.core.member import get_member_disciplines, find_member
from src.core.payments import pay_invoice_with_receipt as pay_invoice_with_receipt, member_invoices
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.web.controllers.api.auth import getMemberId, BAD_MEMBER_RESPONSE
from src.web.controllers.api import apply_CORS
from werkzeug.utils import secure_filename

me_api_blueprint = Blueprint("me_api", __name__, url_prefix="/api/me")


NOT_FILE_RESPONSE = {"msg": "The file was not provided"}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILE_EXT_NOT_ALLOW_RESPONSE = {"msg": "The file extension is not allowed"}


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


@me_api_blueprint.post("/makepayment")
@jwt_required()
def pay_invoice():
 
    # Get member Id and check if exist
    id = getMemberId( get_jwt_identity() )
    if not id:
        return jsonify(BAD_MEMBER_RESPONSE), 401
  
    # check if the post request has the file part    
    if 'file' not in request.files:
         return jsonify(NOT_FILE_RESPONSE), 404  

    # Get from reques the file of receipt payment and invoice id
    file = request.files['file']
    invoiceId = request.form['invoiceId']    

    # Check If the user does not select a file
    if file.filename == '':
        return jsonify(NOT_FILE_RESPONSE), 404  
 
    file_extension_regex_match = re.search('.*(\.jpg|\.png|\.jpeg)$', file.filename)
    if file_extension_regex_match is None:
        return jsonify(FILE_EXT_NOT_ALLOW_RESPONSE), 404  

    # Generate secure filename and save the image in CDN 
    filename = secure_filename(f"receipt-payment-{invoiceId}{file_extension_regex_match.group(1)}")
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    # Do payment and save filename
    payment = pay_invoice_with_receipt(invoiceId, filename)

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS    


@me_api_blueprint.after_request
def cors_HEADERS(response):
    return apply_CORS(response)