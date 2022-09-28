from unicodedata import name
from flask import Flask
from flask import render_template
from src.core.commands import usersbp
from src.core.commands import databasebp

from src.core import database

from src.web.helpers import handlers
from src.web.controllers.issues import issue_blueprint


def create_app(static_folder="static"):
    app = Flask(__name__, static_folder=static_folder)

    @app.get("/")
    def home():
        return render_template("home.html")

    database.init_app(app)

    app.register_blueprint(issue_blueprint)
    app.register_blueprint(usersbp)
    app.register_blueprint(databasebp)

    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)

   
   

    return app
