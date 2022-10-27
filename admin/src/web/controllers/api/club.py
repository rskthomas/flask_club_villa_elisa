from flask import Blueprint, request
from src.web.helpers.handlers import bad_request
from src.core.discipline import get_disciplines


club_api_blueprint = Blueprint("club_api", __name__, url_prefix="/club")


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
def index():
    disciplines = get_disciplines()
    return {"disciplines": list(map(discipline_as_json, disciplines))}
