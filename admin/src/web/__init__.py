from os import environ
from flask import Flask
from flask import render_template

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
from src.web.controllers.api import api_blueprint
from src.web.controllers.payments import payments_blueprint
from src.web.controllers.profile import profile_blueprint


def create_app(static_folder="static", env="development"):
    app = Flask(__name__, static_folder=static_folder)
    app.secret_key = environ.get("FLASK_SECRET_KEY", "this is just a secret")

    print("Environment: {}".format(env))
    app.config.from_object(config[env])
    database.init_app(app)

    @app.get("/")
    def home():
        return render_template("home.html", header_info=get_header_info())

    app.register_blueprint(usersbp)
    app.register_blueprint(databasebp)
    app.register_blueprint(seedsbp)

    app.register_blueprint(auth_blueprint)

    app.register_blueprint(discipline_blueprint)
    app.register_blueprint(system_config_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(member_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(payments_blueprint)
    app.register_blueprint(profile_blueprint)

    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)

    return app
