""" API Blueprint Application """

from flask import Blueprint, current_app
from flask_restplus import Api

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp, version='1.0', title='simple-smart-check API',
            description='Back-End API for simple-smart-check Project')


@api_bp.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


# Import resources to ensure view is registered
from .resources import * # NOQA
from .controllers.auth import *