from app.api import apiRestful
from app.api.security import require_auth
from app.ormmodels import CurriculumsModel
from datetime import datetime
from flask import request
from flask_restplus import Resource, reqparse     # Reference : http://flask-restplus.readthedocs.io


# ---------------------------[ SecureResource ]----------------------------------
# Calls require_auth decorator on all requests
class SecureResource(Resource):
    method_decorators = [require_auth]
# -------------------------------------------------------------------------------


# --------------------[ API SAMPLE without SecureResources ]---------------------
@apiRestful.route('/resource/<string:resource_id>')
@apiRestful.param('resource_id', 'Class-wide description')
class ResourceOne(Resource):
# Unsecure Resource Class: Inherit from Resource
    
    @apiRestful.doc(params= {
                        'smaple_get_params1': 'get param1 samples',
                        'smaple_get_params2': 'get param2 samples',})
    def get(self, resource_id):
        checkParamsFromHttpReq(['smaple_get_params1'])
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}

    @apiRestful.doc(params= {
                        'smaple_post_params1': 'post param1 samples',
                        'smaple_post_params2': 'post param2 samples',})
    @apiRestful.expect()
    def post(self, resource_id):
        requestBody = request.form.to_dict()
        return {'smaple_params': data}, 201
# -------------------------------------------------------------------------------


# ----------------[ API SAMPLE with Applying SecureResources ]-------------------
@apiRestful.route('/secure-resource/<string:resource_id>')
@apiRestful.param('resource_id', 'Class-wide description')
class SecureResourceOne(SecureResource):
    """ Secure Resource Class: Inherit from Resource """

    @apiRestful.doc(params= {'resource_id': 'An ID'})
    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
# -------------------------------------------------------------------------------


# ------------------------[ API to manage Curriculums ]--------------------------
@apiRestful.route('/resource/curriculums/list')
class AllCurriculumns(Resource):
    def get(self):
        def to_json(x= CurriculumsModel):
            return {
                'curriculumNo': x.curriculumNo,
                'curriculumCategory': x.curriculumCategory,
                'ordinalNo': x.ordinalNo,
                'curriculumName': x.curriculumName,
                'curriculumType': x.curriculumType,
                'startDate': str(x.startDate),
                'endDate': str(x.endDate),
                'applicantsInserted': x.applicantsInserted,
                'membersInserted': x.membersInserted,
                'insertedTimestamp': str(x.insertedTimestamp),
                'updatedTimestamp': str(x.updatedTimestamp)
            }
        return {
            'curriculums': list(map(lambda x: to_json(x), CurriculumsModel.query.all()))
        }
# -------------------------------------------------------------------------------