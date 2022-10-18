from flask import Blueprint
from src.core import member
from src.web.controllers.api.members import member_api_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(member_api_blueprint)
