"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

import json
from datetime import datetime
from flask import request
from flask_restplus import Resource

from .controllers.security import require_auth
from . import api_rest

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]


@api_rest.route('/resource/<string:resource_id>')
@api_rest.doc(params={'resource_id': 'An ID'})
class ResourceOne(Resource):
    """ Unsecure Resource Class: Inherit from Resource """
    
    @api_rest.param('resource_id', 'Class-wide description')
    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}

    def post(self, resource_id):
        json_payload = request.json
        return {'timestamp': json_payload}, 201


@api_rest.route('/secure-resource/<string:resource_id>')
@api_rest.param('resource_id', 'Class-wide description')
@api_rest.doc(params={'resource_id': 'An ID'})
class SecureResourceOne(SecureResource):
    """ Secure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}


        