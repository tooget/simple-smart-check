from app.api import apiRestful
from app.api.security import require_auth
from app.extensions import db
from app.ormmodels import AttendanceLogsModel, ApplicantsModel, CurriculumsModel, MembersModel
from app.ormmodels import AttendanceLogsModelSchema, ApplicantsModelSchema, CurriculumsModelSchema, MembersModelSchema
from datetime import datetime, timedelta
from json import loads
from flask import request
from flask_restplus import Resource     # Reference : http://flask-restplus.readthedocs.io
import pandas as pd


# # ---------------------------[ SecureResource ]----------------------------------
# # Calls require_auth decorator on all requests
# class SecureResource(Resource):
#     method_decorators = [require_auth]
# # -------------------------------------------------------------------------------


# # --------------------[ API SAMPLE without SecureResources ]---------------------
# @apiRestful.route('/resource/<string:resource_id>')
# @apiRestful.param('resource_id', 'Class-wide description')
# class ResourceOne(Resource):    # Unsecure Resource Class: Inherit from Resource
    
#     @apiRestful.doc(params= {
#                         'smaple_get_params1': 'get param1 samples',
#                         'smaple_get_params2': 'get param2 samples',})
#     def get(self, resource_id):
#         checkParamsFromHttpReq(['smaple_get_params1'])
#         timestamp = datetime.utcnow().isoformat()
#         return {'timestamp': timestamp}

#     @apiRestful.doc(params= {
#                         'smaple_post_params1': 'post param1 samples',
#                         'smaple_post_params2': 'post param2 samples',})
#     @apiRestful.expect()
#     def post(self, resource_id):
#         requestBody = request.form.to_dict()
#         return {'smaple_params': data}, 201
# # -------------------------------------------------------------------------------


# # ----------------[ API SAMPLE with Applying SecureResources ]-------------------
# @apiRestful.route('/secure-resource/<string:resource_id>')
# @apiRestful.param('resource_id', 'Class-wide description')
# class SecureResourceOne(SecureResource):    # Secure Resource Class: Inherit from Resource

#     @apiRestful.doc(params= {'resource_id': 'An ID'})
#     def get(self, resource_id):
#         timestamp = datetime.utcnow().isoformat()
#         return {'timestamp': timestamp}
# # -------------------------------------------------------------------------------


# ------------------------[ API to manage Curriculums ]-------------------------
class Curriculums:

    # ----------------[ Get Curriculums ]---------------------------------------
    @apiRestful.route('/resource/curriculums/filter')
    @apiRestful.doc(params= {
                    'curriculumCategory': {'in': 'query', 'description': 'URL parameter, optional'},
                    'curriculumType': {'in': 'query', 'description': 'URL parameter, optional'},
                    # You can add query filter columns if needed.
    })
    class get_Curriculums_Filter(Resource):

        def get(self):
            queryFilter = request.args
            curriculums = CurriculumsModel.query.filter_by(**queryFilter).all()
            curriculumsSchema = CurriculumsModelSchema(many= True)
            output = curriculumsSchema.dump(curriculums)
            return {'return': output}
    # ---------------------------------------------------------------------------


    # ----------------[ Get Curriculums, joined to Members counts ]--------------
    @apiRestful.route('/resource/curriculums/join/members')
    class get_Curriculums_Join(Resource):

        def get(self):
            query = CurriculumsModel.query  # [!] join query

            engine = db.get_binds()[ list(db.get_binds().keys())[4] ]   # [!] CurriculumsModel Engine, defined in get_binds()
            df = pd.read_sql(query.statement, engine)
            df_recordslist = df.to_json(orient= 'records', date_format= 'iso', force_ascii= False)      # df_recordslist : date_format issue(TypeError: Object of type DataFrame is not JSON serializable), return type issue(always string representation of list), force_ascii issue(unicode problem when True)
            output = loads(df_recordslist)                              # str representation list to list : https://stackoverflow.com/questions/1894269/convert-string-representation-of-list-to-list

            return {'return': output}
    # ---------------------------------------------------------------------------
# -------------------------------------------------------------------------------


# ------------------------[ API to manage AttendanceLogs ]-----------------------
class AttendanceLogs:
    
    # ----------------[ Get new Attendance logs ]--------------------------------
    @apiRestful.route('/resource/attendancelogs/filter')
    @apiRestful.doc(params= {
                    'phoneNo': {'in': 'query', 'description': 'URL parameter, optional'},
                    'curriculumNo': {'in': 'query', 'description': 'URL parameter, optional'},
                    'checkInOut': {'in': 'query', 'description': 'URL parameter, optional'},
                    'attendanceDate': {'in': 'query', 'description': 'URL parameter, optional'},
                    # You can add query filter columns if needed.
    })
    class get_AttendanceLogs_Filter(Resource):

        def get(self):
            queryFilter = request.args
            attendanceLogs = AttendanceLogsModel.query.filter_by(**queryFilter).all()
            attendanceLogsSchema = AttendanceLogsModelSchema(many= True)
            output = attendanceLogsSchema.dump(attendanceLogs)
            return {'return': output}
    # ---------------------------------------------------------------------------


    # ----------------[ Create a new Attendance log ]----------------------------
    @apiRestful.route('/resource/attendancelogs/new')
    @apiRestful.doc(params= {
                    'phoneNo': {'in': 'formData', 'description': 'application/json, body required'},
                    'curriculumNo': {'in': 'formData', 'description': 'application/json, body required'},
                    'checkInOut': {'in': 'formData', 'description': 'application/json, body required'},
                    'signature': {'in': 'formData', 'description': 'application/json, body required'},
                    # You can add formData columns if needed.
    })
    class post_AttendanceLogs_New(Resource):

        def post(self):
            # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
            # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            infoFromClient = request.form
            phoneNoFromClient = infoFromClient['phoneNo']
            curriculumNoFromClient = infoFromClient['curriculumNo']
            checkInOutFromClient = infoFromClient['checkInOut']
            signatureFromClient = infoFromClient['signature']
            attendanceDate = datetime.utcnow()

            requestedBody = {
                "phoneNo": phoneNoFromClient,
                "curriculumNo": curriculumNoFromClient,
                "checkInOut": checkInOutFromClient,
                "signature": signatureFromClient.split(',')[-1].strip(),
                "attendanceDate": attendanceDate.strftime('%Y-%m-%d')
            }
            
            newAttendanceLog = AttendanceLogsModel(**requestedBody)

            try:
                db.session.add(newAttendanceLog)
                db.session.commit()
                return {'return': {'message': f'New AttendanceLog created : {requestedBody}'}}, 201
            except:
                db.session.rollback()
                return {'return': {'message': 'Something went wrong'}}, 500
    # ---------------------------------------------------------------------------
# -------------------------------------------------------------------------------


# ------------------------[ API to manage Members ]------------------------------
class Members:

    # ----------------[ Get members ]--------------------------------------------
    @apiRestful.route('/resource/members/filter')
    @apiRestful.doc(params= {
                    'phoneNo': {'in': 'query', 'description': 'URL parameter, optional'},
                    'curriculumNo': {'in': 'query', 'description': 'URL parameter, optional'},
                    'attendancePass': {'in': 'query', 'description': 'URL parameter, optional'},
                    'attendanceCheck': {'in': 'query', 'description': 'URL parameter, optional'},
                    'curriculumComplete': {'in': 'query', 'description': 'URL parameter, optional'},
                    'employment': {'in': 'query', 'description': 'URL parameter, optional'},
                    # You can add query filter columns if needed.
    })
    class get_Members_Filter(Resource):

        def get(self):
            queryFilter = request.args
            members = MembersModel.query.filter_by(**queryFilter).all()
            membersSchema = MembersModelSchema(many= True)
            output = membersSchema.dump(members)
            return {'return': output}
    # -----------------------------------------------------------------------------


    # ----------------[ Update members' Info ]-------------------------------------
    @apiRestful.route('/resource/members')
    @apiRestful.doc(params= {
                    'phoneNo': {'in': 'formData', 'description': 'application/json, body required'},
                    'curriculumNo': {'in': 'formData', 'description': 'application/json, body required'},
                    'attendancePass': {'in': 'formData', 'description': 'application/json, body required'},
                    'attendanceCheck': {'in': 'formData', 'description': 'application/json, body required'},
                    'curriculumComplete': {'in': 'formData', 'description': 'application/json, body required'},
                    'employment': {'in': 'formData', 'description': 'application/json, body required'},
                    # You can add formData columns if needed.
    })
    class put_Members_Info(Resource):

        def put(self):
            # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
            # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            infoFromClient = request.form
            requestedBody = {
                'phoneNo': infoFromClient['phoneNo'],
                'curriculumNo': infoFromClient['curriculumNo'],
                'attendancePass': infoFromClient['attendancePass'],
                'attendanceCheck': infoFromClient['attendanceCheck'],
                'curriculumComplete': infoFromClient['curriculumComplete'],
                'employment': infoFromClient['employment'],
            }

            memberInfo = MembersModel(**requestedBody)

            try:
                db.session.merge(memberInfo)    # session.merge() : A kind of UPSERT, https://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#merging
                db.session.commit()
                return {'return': {'message': f'MemberInfo updated : {requestedBody}'}}, 201
            except:
                db.session.rollback()
                return {'return': {'message': 'Something went wrong'}}, 500
    # -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


# ------------------------[ API to manage Applicants ]-----------------------------
class Applicants:

    # ----------------[ Get Applicants ]-------------------------------------------
    @apiRestful.route('/resource/applicants/filter')
    @apiRestful.doc(params= {
                    'phoneNo': {'in': 'query', 'description': 'URL parameter, optional'},
                    'curriculumNo': {'in': 'query', 'description': 'URL parameter, optional'},
                    'applicantName': {'in': 'query', 'description': 'URL parameter, optional'},
                    'email': {'in': 'query', 'description': 'URL parameter, optional'},
                    # You can add query filter columns if needed.
    })
    class get_Applicants_Filter(Resource):

        def get(self):
            queryFilter = request.args
            applicants = ApplicantsModel.query.filter_by(**queryFilter).all()
            applicantsSchema = ApplicantsModelSchema(many= True)
            output = applicantsSchema.dump(applicants)
            return {'return': output}
    # -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------