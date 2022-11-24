from flask import Blueprint
from src.web.controllers.api.members import member_api_blueprint
from src.web.controllers.api.club import club_api_blueprint
from src.web.controllers.api.me import me_api_blueprint
from src.web.controllers.api.auth import auth_api_blueprint
from src.web.controllers.api.statistics import statistics_api_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(member_api_blueprint)

api_blueprint.register_blueprint(club_api_blueprint)

api_blueprint.register_blueprint(me_api_blueprint)

api_blueprint.register_blueprint(auth_api_blueprint)

api_blueprint.register_blueprint(statistics_api_blueprint)
