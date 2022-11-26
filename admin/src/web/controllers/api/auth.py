from flask import Blueprint, request, jsonify, current_app, Flask, make_response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies
from src.core.auth import find_user, find_user_by_mail_and_pass
from src.core.member import find_member_by_email
from src.web.controllers.api import apply_CORS


auth_api_blueprint = Blueprint("auth_api", __name__, url_prefix="/api/auth")

BAD_MEMBER_RESPONSE = {"msg": "The user isn't a member"}


@auth_api_blueprint.post("/login")
def loginNew():
    content = request.json
    username = content["username"]
    password = content["password"]
    current_app.logger.info("Login attempt: " + username)

    user = find_user_by_mail_and_pass(username, password)

    if user:
        access_token = create_access_token(identity=user.id)
        
        response = make_response(
        jsonify({"msg": "login succesful"}), 200
        )
        set_access_cookies(response, access_token)
        return response
    
    else:
        return make_response(jsonify({"msg": "Bad username or password"}), 401)


"""
El @jwt_required() valida si el jwt esta seteado en la request o si existe la cookie cargada
luego con el metodo get_jwt_identity() obtiene el id de la entidad que se guardo en el JWT, si se guardaron mas campos se puede usar el get_jwt(), ejemplo:
    claims = get_jwt()
    return jsonify(foo=claims["foo"])
"""


@auth_api_blueprint.get("/user_jwt")
@jwt_required()
def user_jwt():
    current_user = get_jwt_identity()
    user = find_user(current_user)
    current_app.logger.info(jsonify({"id": user.id}))

    response = make_response(jsonify({
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "roles": list(map(lambda x: x.name, user.roles)),
            }), 200)
    return response

@auth_api_blueprint.get("/logout_jwt")
@jwt_required()
def logout_jwt():
    response = make_response(jsonify({"msg": "logout successful"}), 200)
    unset_jwt_cookies(response)
    return response


def getMemberId(jwt_identity):
    """If the logged user is a member, returns its id, otherwise returns None"""

    user = find_user(jwt_identity)
    if not user:
        return None

    member = find_member_by_email(user.email)
    if not member:
        return None

    return member.id

@auth_api_blueprint.after_request
def cors_HEADERS(response):
    return apply_CORS(response)