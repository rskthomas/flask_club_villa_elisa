from email import header
from flask import session
from src.core.auth import find_user


def get_header_info():
    """
    Retrieves a dictionary with the information about the authenticated user to be displayed in the header, or None if
    no authenticated user is found.
    """
    user_id_from_session = session.get("user")
    user = find_user(user_id_from_session)
    header_info = (
        None
        if user is None
        else {
            "full_name": f"{user.lastname}, {user.firstname}",
            "roles": map(lambda role: role.name, user.roles),
        }
    )
    return header_info
