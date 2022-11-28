from flask import Blueprint, request, make_response, jsonify
from src.core.member import list_members
from src.web.controllers.api import apply_CORS


member_api_blueprint = Blueprint(
    "members_api",
    __name__,
    url_prefix="/api/members")

@member_api_blueprint.get('')
def index():
    members = list_members({'personal_id': request.args.get('q')})

    response = make_response(
        jsonify([member.serialize() for member in members]), 200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@member_api_blueprint.after_request
def cors_HEADERS(response):
    return apply_CORS(response)