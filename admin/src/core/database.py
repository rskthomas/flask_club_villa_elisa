from flask_sqlalchemy import SQLAlchemy

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

    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()


def reset_db():
    """Resets the database"""
    print('Dropping all tables!')
    db.drop_all()
    print('Creating all tables!')
    db.create_all()
    print('Database reset!')

def create_tables():
    """Creates the database tables"""
    db.create_all()

def drop_db():
    """Drops all tables from the database"""
    print('Dropping all tables!')
    db.drop_all()