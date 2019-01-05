import os


class Config(object):

    # -----------------[ app.config.from_object Parameters in app.__init__.py ]-----------------
    # Pure flask app.config for Flask(__name__)
    # Parameters : http://flask.pocoo.org/docs/1.0/config/
    # If not set fall back to production for safety
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    # flask_sqlalchemy app.config for db.init_app()
    # Set SQLALCHEMY env on your production Environment
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    SQLALCHEMY_BINDS = os.getenv('SQLALCHEMY_BINDS', {  
        'sqlite': 'sqlite:///app.db',
        'mysql': 'mysql+pymysql://kisa:kisakisakisakisa!@rds-simplesmartcheck-mysql8.c4bcyomq603x.ap-northeast-2.rds.amazonaws.com:3306/simplesmartcheck?charset=utf8'
    })
    # flask_jwt_extended app.config for jwt.init_app()
    # Set JWT_SECRET env on your production Environment
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    JWT_BLACKLIST_ENABLED = os.getenv('JWT_BLACKLIST_ENABLED', True)
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS', ['access'])
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.__init__.py ]--------------------------
    # app.Config for cors.init_app()
    CORS_ORIGIN = ['http://0.0.0.0:7000']
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.api.__init__.py ]----------------------
    # app.Config for API Blueprint
    API_URI_PREFIX = '/api'
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.api.__init__.py ]----------------------
    # Hash Parameters for app.api.users.py
    SALT_KEYWORD = 'kisa'
    SALT_SIZE = 256/32
    SALT_ROUNDS = 1
    # ------------------------------------------------------------------------------------------