from os import environ

class Config(object):
    """Default configuration"""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   
class ProductionConfig(Config):
    DB_USER = environ.get('DB_USER')
    DB_PASS = environ.get('DB_PASS')
    DB_HOST = environ.get('DB_HOST')
    DB_NAME = environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

class DevelopmentConfig(Config):
    
    DEBUG = True
    TESTING = True
    DB_USER = environ.get('DB_USER',"root")
    DB_PASS = environ.get('DB_PASS',"root")
    DB_HOST = environ.get('DB_HOST',"localhost")
    DB_NAME = environ.get('DB_NAME', "grupo30")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True