from flask import Blueprint, request, jsonify
from src.web.helpers.handlers import bad_request
from src.core.member import member_count_by_gender
from src.core.discipline import enrollment_by_discipline
from src.core.payments import last_year_invoices
from src.web.controllers.api import apply_CORS
statistics_api_blueprint = Blueprint(
    "statistics",
    __name__,
    url_prefix="/api/estadisticas")

@statistics_api_blueprint.get('/disciplinas')
def disciplines_enrollment():
    return jsonify(enrollment_by_discipline())

@statistics_api_blueprint.get('/facturacion')
def invoices_data():
    return jsonify(last_year_invoices())

@statistics_api_blueprint.get('/miembros_por_genero')
def members_by_gender():
    return jsonify(member_count_by_gender())

@statistics_api_blueprint.after_request
def cors_HEADERS(response):
    return apply_CORS(response)