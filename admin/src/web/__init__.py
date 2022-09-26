from flask import Flask
from flask import render_template
from src.web.helpers import handlers
from src.web.controllers.issues import issue_blueprint

def create_app(static_folder = 'static'):
  app = Flask(__name__, static_folder=static_folder)

  @app.get("/")
  def home():
      return render_template('home.html')


  app.register_blueprint(issue_blueprint)

  app.register_error_handler(404, handlers.not_found_error)
  app.register_error_handler(500, handlers.internal_server_error)

  return app
