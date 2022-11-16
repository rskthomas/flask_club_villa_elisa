from flask import Flask
from flask import Blueprint, request, jsonify
from src.core import auth

from flask_jwt_extended import create_access_token 
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies

auth_api_blueprint = Blueprint("auth_api", __name__, url_prefix="/auth")


@auth_api_blueprint.post("/login")
def loginNew():
   content = request.json
   username = content['username']
   password = content['password']

   user = auth.find_user_by_mail_and_pass(username, password)
    
   if user:
       access_token = create_access_token(identity=user.id)
       response = jsonify({"msg": "login successful"})
       set_access_cookies(response, access_token)
       return response, 201
   else:
        return jsonify({"msg": "Bad username or password"}), 401


'''
El @jwt_required() valida si el jwt esta seteado en la request o si existe la cookie cargada
luego con el metodo get_jwt_identity() obtiene el id de la entidad que se guardo en el JWT, si se guardaron mas campos se puede usar el get_jwt(), ejemplo:
    claims = get_jwt()
    return jsonify(foo=claims["foo"])
'''
@auth_api_blueprint.get('/user_jwt')
@jwt_required()
def user_jwt():
    current_user = get_jwt_identity()
    user = auth.find_user(current_user)
    response = jsonify(user.id)
    return response, 200       


@auth_api_blueprint.get('/logout_jwt')
@jwt_required()
def logout_jwt():
  response = jsonify({"msg": "logout successful"})
  unset_jwt_cookies(response)
  return response, 200

