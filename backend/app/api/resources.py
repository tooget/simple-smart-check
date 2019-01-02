from datetime import datetime, timedelta
from flask import request
from flask_restplus import Resource, reqparse     # Reference : http://flask-restplus.readthedocs.io
from app.models import AttendanceLogsModel, CurriculumsModel
from . import apiRestful
from .security import require_auth


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


# ------------------------[ API to GET a All Curriculumns ]--------------------------
@apiRestful.route('/resource/curriculums/list')
class AllCurriculumns(Resource):
    def get(self):
        return CurriculumsModel.return_all()
# -------------------------------------------------------------------------------


# ------------------------[ API to Create Attendance Logs ]--------------------------
@apiRestful.route('/resource/attendance/log')
class CreateAttendanceLog(Resource):
    def post(self):
        requestBody = request.get_json()
        requestBody['signature'] = requestBody['signature'].split(',')[-1].strip()

        utcnow = datetime.utcnow()
        time_gap = timedelta(hours=9)
        kst = utcnow + time_gap
        requestBody['attendanceDate'] = kst.strftime('%Y-%m-%d')
        
        attendanceLog = AttendanceLogsModel(**requestBody)
        
        try:
            attendanceLog.save_to_db()
            return {'message': f"User {requestBody['phoneNo']}\'s attendanceLog is created"}, 201
        except:
            return {'message': 'Something went wrong'}, 500
# -------------------------------------------------------------------------------