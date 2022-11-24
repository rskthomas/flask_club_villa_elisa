from flask import Blueprint, request, jsonify
from src.web.helpers.handlers import bad_request
from src.core.member import list_members
from src.core.discipline import enrollment_by_discipline
from src.core.payments import last_year_invoices

statistics_api_blueprint = Blueprint(
    "statistics",
    __name__,
    url_prefix="/estadisticas")

@statistics_api_blueprint.get('/disciplinas')
def disciplines_enrollment():
    return jsonify(enrollment_by_discipline())

@statistics_api_blueprint.get('/facturacion')
def invoices_data():
    return jsonify(last_year_invoices())
