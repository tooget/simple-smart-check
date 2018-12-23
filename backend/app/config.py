import os

class Config(object):

    # -----------------[ app.config.from_object Parameters in app.__init__.py ]-----------------
    # Pure flask app.config
    # Parameters : http://flask.pocoo.org/docs/1.0/config/
    # If not set fall back to production for safety
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    # flask_sqlalchemy app.config
    # Set SQLALCHEMY env on your production Environment
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    # flask_jwt_extended app.config
    # Set JWT_SECRET env on your production Environment
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    JWT_BLACKLIST_ENABLED = os.getenv('JWT_BLACKLIST_ENABLED', True)
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS', ['access', 'refresh'])
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.__init__.py ]--------------------------
    CORS_ORIGIN = ['https://frontend.smartcheck.ml']
    # ------------------------------------------------------------------------------------------