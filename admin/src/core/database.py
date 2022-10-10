from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    config_db(app)


def config_db(app):
    @app.before_first_request
    def init_database():
        db.create_all()

    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()


def reset_db():
    print('Dropping all tables!')
    db.drop_all()
    print('Creating all tables!')
    db.create_all()
    print('Database reset!')

def create_tables():
    db.create_all()

def drop_db():
    print('Dropping all tables!')
    db.drop_all()