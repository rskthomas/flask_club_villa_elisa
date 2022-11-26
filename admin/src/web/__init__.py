from os import environ, path
from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from src.web.config import config
from src.core import database
from src.web.helpers import handlers
from src.web.helpers.get_header_info import get_header_info

from src.core.commands import usersbp
from src.core.commands import databasebp
from src.core.commands import seedsbp

from src.web.controllers.auth import auth_blueprint
from src.web.controllers.discipline import discipline_blueprint
from src.web.controllers.users import users_blueprint
from src.web.controllers.system_config import system_config_blueprint
from src.web.controllers.members import member_blueprint
from src.web.controllers.payments import payments_blueprint
from src.web.controllers.profile import profile_blueprint
from src.web.controllers.cdn import cdn_blueprint
from flask_jwt_extended import JWTManager
from datetime import timedelta

#nested blueprints are not supported by flask-WTF csrf protection, so all should be registered here
from src.web.controllers.api.members import member_api_blueprint
from src.web.controllers.api.club import club_api_blueprint
from src.web.controllers.api.me import me_api_blueprint
from src.web.controllers.api.auth import auth_api_blueprint


UPLOAD_FOLDER = './private'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def create_app(static_folder="static", env="development"):
    app = Flask(__name__, static_folder=static_folder)
    app.secret_key = environ.get("FLASK_SECRET_KEY", "this is just a secret")

    print("Environment: {}".format(env))
    app.config.from_object(config[env])
    app.config['UPLOAD_FOLDER'] = path.abspath(UPLOAD_FOLDER)

    # Here you can globally configure all the ways you want to allow JWTs to
    # be sent to your web application. By default, this will be only headers.
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    # If true this will only allow the cookies that contain your JWTs to be sent
    # over https. In production, this should always be set to True
    app.config["JWT_COOKIE_SECURE"] = False
    # Change this in your code!
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    jwt = JWTManager(app)

    app.logger.info('upload folder: ' + app.config['UPLOAD_FOLDER'])
    database.init_app(app)
    app.secret_key = environ.get("FLASK_SECRET_KEY", "this is just a secret")

    @app.get("/")
    def home():
        return render_template("home.html", header_info=get_header_info())

    csrf = CSRFProtect(app)
    csrf.init_app(app)
    
    app.register_blueprint(usersbp)
    app.register_blueprint(databasebp)
    app.register_blueprint(seedsbp)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(discipline_blueprint)
    app.register_blueprint(system_config_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(member_blueprint)

    #csrf protection on the endpoints are handled by the jwt library
    csrf.exempt(member_api_blueprint)
    csrf.exempt(club_api_blueprint)
    csrf.exempt(me_api_blueprint)
    csrf.exempt(auth_api_blueprint)
    
    
    app.register_blueprint(member_api_blueprint)
    app.register_blueprint(club_api_blueprint)
    app.register_blueprint(me_api_blueprint)
    app.register_blueprint(auth_api_blueprint)


    
    app.register_blueprint(cdn_blueprint)

    app.register_blueprint(payments_blueprint)
    app.register_blueprint(profile_blueprint)

    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)
    
    
    
    return app

