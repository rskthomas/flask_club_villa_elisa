from flask import Blueprint, jsonify, request, Flask


from functools import wraps
from src.web.controllers.api.members import member_api_blueprint
from src.web.controllers.api.club import club_api_blueprint
from src.web.controllers.api.me import me_api_blueprint
from src.web.controllers.api.auth import auth_api_blueprint



def id_required(argument=None):
    """Decorator to check if id header exists"""

    @wraps(argument)
    def argument_wrapper(function):
        @wraps(function)
        def id_checker(*args, **kwargs):
            if not request.headers.get("id"):
                return BAD_REQUEST
            return function(*args, **kwargs)

        return id_checker

    return argument_wrapper


