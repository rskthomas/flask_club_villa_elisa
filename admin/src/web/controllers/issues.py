from flask import Blueprint, render_template
from src.web.helpers.get_header_info import get_header_info

issue_blueprint = Blueprint("issues", __name__, url_prefix="/consultas")


@issue_blueprint.get("/")
def issue_index():
    issues = []
    return render_template(
        "issues/index.html", issues=issues, header_info=get_header_info()
    )
