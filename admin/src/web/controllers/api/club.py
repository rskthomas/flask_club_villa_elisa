from flask import Blueprint, make_response, jsonify
from src.core.discipline import get_disciplines


club_api_blueprint = Blueprint("club_api", __name__, url_prefix="/api/club")

_EMAIL = "clubdeportivovillaelisa@gmail.com"
_PHONE = "0221 487-0193"


@club_api_blueprint.get("/disciplines")
def disciplines():
    """Returns a list of all disciplines (JSON)"""

    response = make_response(
        jsonify([discipline.serialize() for discipline in get_disciplines()]), 200
    )
    response.headers["Content-Type"] = "application/json"

    return response


@club_api_blueprint.get("/info")
def info():
    """Returns a JSON with the club's email and phone number."""
    response = make_response(jsonify({"email": _EMAIL, "phone": _PHONE}), 200)

    response.headers["Content-Type"] = "application/json"

    return response
