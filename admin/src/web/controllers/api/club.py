from flask import Blueprint, request, make_response, jsonify
from src.web.helpers.handlers import bad_request
from src.core.discipline import get_disciplines


club_api_blueprint = Blueprint("club_api", __name__, url_prefix="/club")

email= "clubdeportivovillaelisa@gmail.com"
phone= "0221 487-0193"

def discipline_as_json(discipline):
    """Converts a discipline to json and returns it"""
    return {
        "id": discipline.id,
        "category": discipline.category,
        "coach": discipline.coach,
        "schedule": discipline.schedule,
        "monthly_price": discipline.monthly_price,
        "active": discipline.active,
        "created_at": discipline.created_at,
    }


@club_api_blueprint.get("/disciplines")
def disciplines():
    disciplines = get_disciplines()
    response = make_response(jsonify({"disciplines": list(map(discipline_as_json, disciplines))}), 200)
    response.headers['Content-Type'] = 'application/json'

    return response

@club_api_blueprint.get("/info")
def info():
    response = make_response(jsonify({"email": email, "phone": phone}), 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Schema'] = """asdasd"""


    return response

