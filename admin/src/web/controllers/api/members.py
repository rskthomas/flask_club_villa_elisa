from flask import Blueprint, request
from src.web.helpers.handlers import bad_request
from src.core.member import list_members


member_api_blueprint = Blueprint(
    "members_api",
    __name__,
    url_prefix="/miembros")


def member_as_json(member):
    """Converts a member to json and returns it"""
    return {
        'id': member.id,
        'first_name': member.first_name,
        'last_name': member.last_name,
        'personal_id_type': member.personal_id_type,
        'personal_id': member.personal_id
    }


@member_api_blueprint.get('')
def index():
    members = list_members({'personal_id': request.args.get('q')})
    return {'members': list(map(member_as_json, members))}
