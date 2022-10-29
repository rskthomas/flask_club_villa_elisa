from flask import Blueprint, render_template, session
from src.core.auth import find_user
from src.web.controllers.auth import login_required
from src.web.helpers.get_header_info import get_header_info

profile_blueprint = Blueprint("profile", __name__, url_prefix="/profile")


@profile_blueprint.get("/")
@login_required()
def index():
    """Renders the profile page for the authenticated user."""

    user_id_from_session = session.get("user")
    user = find_user(user_id_from_session)
    print(user)

    return render_template(
        "profile/index.html",
        user=user,
        roles=map(lambda role: role.name, user.roles),
        header_info=get_header_info(),
    )
