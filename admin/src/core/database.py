from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from src.core import seeds

db = SQLAlchemy()


def init_app(app):
    """Initializes the database"""
    db.init_app(app)
    config_db(app)


def config_db(app):
    """Configures the database"""

    @app.before_first_request
    def init_database():
        db.create_all()
        """If server is on dev mode, initialize the database with some data"""
        if current_app.config["ENV"] == "development":
            seeds.run()
        print("Database initialized!")
        

    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()


def reset_db():
    """Resets the database"""
    print("Dropping all tables!")
    db.drop_all()
    print("Creating all tables!")
    db.create_all()
    print("Database reset!")


def create_tables():
    """Creates the database tables"""
    db.create_all()


def drop_db():
    """Drops all tables from the database"""
    print("Dropping all tables!")
    db.drop_all()

