from flask import redirect
from flask import Flask
from flask import render_template
from os import environ

from src.web.config import config
from src.core import database
from src.web.helpers import handlers

from src.web.controllers.issues import issue_blueprint
from src.core.commands import usersbp
from src.core.commands import databasebp
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.users import users_blueprint
from src.web.controllers.system_config import system_config_blueprint

def create_app(static_folder="static", env="development"):
    app = Flask(__name__, static_folder=static_folder)

    app.secret_key = environ.get("FLASK_SECRET_KEY", 'this is just a secret')

    print("Environment: {}".format(env))
    app.config.from_object(config[env])
    database.init_app(app)

    @app.get("/")
    def home():
        return render_template("home.html")

    app.register_blueprint(issue_blueprint)
    app.register_blueprint(usersbp)
    app.register_blueprint(databasebp)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(system_config_blueprint)
    app.register_blueprint(users_blueprint)

    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)

    return app
