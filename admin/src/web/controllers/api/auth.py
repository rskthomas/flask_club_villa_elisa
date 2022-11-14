from flask import Flask
from flask import Blueprint, request, make_response, jsonify, Response
from src.web.helpers.handlers import bad_request
from src.core import auth
import datetime, jwt
from flask_api.exceptions import AuthenticationFailed
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

auth_api_blueprint = Blueprint("auth_api", __name__, url_prefix="/auth")


@auth_api_blueprint.post("/login")
@cross_origin()
def login():
    content = request.json
    username = content['username']
    password = content['password']

    print(username)
    print(password)

    user = auth.find_user_by_mail_and_pass(username, password)

    if user is None:
        raise AuthenticationFailed('El usuario o la clave son incorrectos.')

    expired = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': expired,
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, "secret", algorithm="HS256")

    response = make_response() 
    response.set_cookie(key='jwt', value=token, httponly=True)
    response = jsonify({"jwt": token})

    return response



@auth_api_blueprint.post("/logout")
@cross_origin()
def validateLogin():
    """Confirm the update member and redirect to member index page."""
    content = request.json
    username = content['username']
    password = content['password']
    if not username:
        return bad_request("No se ha enviado ningún formulario")
   
    response = make_response({"jwt": "JOJO"}, 200)

    return response



