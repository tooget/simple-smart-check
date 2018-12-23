"""
Global Flask Application Setting

See `.flaskenv` for default settings.
 """

import os
from app import app


class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')
    # Set SQLALCHEMY env on your production Environment
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    # Set JWT_SECRET env on your production Environment
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    JWT_BLACKLIST_ENABLED = os.getenv('JWT_BLACKLIST_ENABLED', True)
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS', ['access', 'refresh'])

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)

app.config.from_object('app.config.Config')
