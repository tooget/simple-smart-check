import os
from datetime import timedelta
from functools import update_wrapper
from flask import Flask, current_app, send_file, make_response
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Create Flask app + CORS + configs
app = Flask(__name__)
CORS(app, origins=['https://frontend.smartcheck.ml'])

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

# Connect to DB with flask_sqlalchemy
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Create authentificated session with JWT 
from .models import RevokedTokenModel
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

# Register modules to URL with Blueprint
from .api import api_bp
from .client import client_bp

app.register_blueprint(api_bp)
# app.register_blueprint(client_bp)
