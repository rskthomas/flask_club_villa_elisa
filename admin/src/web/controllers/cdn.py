from flask import send_from_directory, current_app
from flask import Blueprint
from src.web.controllers.auth import login_required

cdn_blueprint = Blueprint(
    "cdn",
    __name__,
    url_prefix="/cdn")


@cdn_blueprint.get('/<path:filename>')
@login_required()
def file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
