from app.api import apiRestful
from app.api.security import require_auth
from app.extensions import db
from app.ormmodels import AttendanceLogsModel, ApplicantsModel, CurriculumsModel, MembersModel
from app.ormmodels import AttendanceLogsModelSchema, ApplicantsModelSchema, CurriculumsModelSchema, MembersModelSchema
from datetime import datetime, timedelta
from flask import request
from flask_restplus import Resource     # Reference : http://flask-restplus.readthedocs.io


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
class Curriculums(Resource):

    # ----------------[ Get Curriculums ]---------------------------------------
    @apiRestful.route('/resource/curriculums/filter')
    @apiRestful.doc(params= {
                'curriculumCategory': 'URL parameter, optional',
                'curriculumType': 'URL parameter, optional',
                # You can add query filter columns if needed.
    })
    class get_Filter(Resource):
        def get(self):
            queryFilter = request.args
            curriculums = CurriculumsModel.query.filter_by(**queryFilter).all()
            curriculumsSchema = CurriculumsModelSchema(many= True)
            output = curriculumsSchema.dump(curriculums)
            return {'curriculums': output}
    # ---------------------------------------------------------------------------
# -------------------------------------------------------------------------------


# ------------------------[ API to manage AttendanceLogs ]-----------------------
class AttendanceLogs(Resource):
    
    # ----------------[ Get new Attendance logs ]--------------------------------
    @apiRestful.route('/resource/attendancelogs/filter')
    @apiRestful.doc(params= {
                    'phoneNo': 'URL parameter, optional',
                    'curriculumNo': 'URL parameter, optional',
                    'checkInOut': 'URL parameter, optional',
                    'attendanceDate': 'URL parameter, optional',
                    # You can add query filter columns if needed.
    })
    class get_Filter(Resource):
        def get(self):
            queryFilter = request.args
            attendanceLogs = AttendanceLogsModel.query.filter_by(**queryFilter).all()
            attendanceLogsSchema = AttendanceLogsModelSchema(many= True)
            output = attendanceLogsSchema.dump(attendanceLogs)
            return {'attendanceLogs': output}
    # ---------------------------------------------------------------------------


    # ----------------[ Create a new Attendance log ]----------------------------
    @apiRestful.route('/resource/attendancelogs/new')
    @apiRestful.doc(params= {
                        'phoneNo': 'application/json, body required',
                        'curriculumNo': 'application/json, body required',
                        'checkInOut': 'application/json, body required',
                        'signature': 'application/json, body required',
                        # You can add query filter columns if needed.
    })
    class post_New(Resource):
        def post(self):
            # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
            # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            infoFromClient = request.form
            phoneNoFromClient = infoFromClient['phoneNo']
            curriculumNoFromClient = infoFromClient['curriculumNo']
            checkInOutFromClient = infoFromClient['checkInOut']
            signatureFromClient = infoFromClient['signature']

            requestedBody = {
                "phoneNo": phoneNoFromClient,
                "curriculumNo": curriculumNoFromClient,
                "checkInOut": checkInOutFromClient,
                "signature": signatureFromClient.split(',')[-1].strip(),
                "attendanceDate": datetime.utcnow() + timedelta(hours= 9) # Calculate Korea Standard Time(KST)
            }
            
            newAttendanceLog = AttendanceLogsModel(**requestedBody)

            try:
                db.session.add(newAttendanceLog)
                db.session.commit()
                return {'message': f'New AttendanceLog created : {requestedBody}'}, 201
            except:
                db.session.rollback()
                return {'message': 'Something went wrong'}, 500
    # ---------------------------------------------------------------------------
# -------------------------------------------------------------------------------


# ------------------------[ API to manage Members ]------------------------------
class Members(Resource):

    # ----------------[ Get members ]--------------------------------------------
    @apiRestful.route('/resource/members/filter')
    @apiRestful.doc(params= {
                    'phoneNo': 'URL parameter, optional',
                    'curriculumNo': 'URL parameter, optional',
                    'attendancePass': 'URL parameter, optional',
                    'attendanceCheck': 'URL parameter, optional',
                    'curriculumComplete': 'URL parameter, optional',
                    'employment': 'URL parameter, optional',
                    # You can add query filter columns if needed.
    })
    class get_Filter(Resource):
        def get(self):
            queryFilter = request.args
            members = MembersModel.query.filter_by(**queryFilter).all()
            membersSchema = MembersModelSchema(many= True)
            output = membersSchema.dump(members)
            return {'members': output}
    # -----------------------------------------------------------------------------


    # ----------------[ Update members' Info ]-------------------------------------
    @apiRestful.route('/resource/members')
    @apiRestful.doc(params= {
                        'phoneNo': 'application/json, body required',
                        'curriculumNo': 'application/json, body required',
                        'attendancePass': 'application/json, body required',
                        'attendanceCheck': 'application/json, body required',
                        'curriculumComplete': 'application/json, body required',
                        'employment': 'application/json, body required',
                        # You can add query filter columns if needed.
    })
    class put_Info(Resource):
        def put(self):
            # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
            # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            infoFromClient = request.form
            
            queryFilter = {
                    'phoneNo': infoFromClient['phoneNo'],
                    'curriculumNo': infoFromClient['curriculumNo'],
            }

            attendancePassFromClient = infoFromClient['attendancePass'],                    
            attendanceCheckFromClient = infoFromClient['attendanceCheck'],
            curriculumCompleteFromClient = infoFromClient['curriculumComplete'],
            employmentFromClient = infoFromClient['employment'],

            try:
                targetMember = MembersModel.query.filter_by(**queryFilter).first()  # Querying target member to update information.
                print(targetMember)
                targetMember.attendancePass = attendancePassFromClient              # ORM Update 'attendancePass' column 
                targetMember.attendanceCheck = attendanceCheckFromClient            # ORM Update 'attendanceCheck' column
                targetMember.curriculumComplete = curriculumCompleteFromClient      # ORM Update 'curriculumComplete' column
                targetMember.employment = employmentFromClient                      # ORM Update 'employment' column
                db.session.merge(targetMember)
                db.session.commit()
                return {'message': f'MemberInfo updated : {memberInfoFromClient}'}, 201
            except:
                db.session.rollback()
                return {'message': 'Something went wrong'}, 500
    # -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


# ------------------------[ API to manage Applicants ]-----------------------------
class Applicants(Resource):

    # ----------------[ Get Applicants ]-------------------------------------------
    @apiRestful.route('/resource/applicants/filter')
    @apiRestful.doc(params= {
                    'phoneNo': 'URL parameter, optional',
                    'curriculumNo': 'URL parameter, optional',
                    'applicantName': 'URL parameter, optional',
                    'email': 'URL parameter, optional',
                    # You can add query filter columns if needed.
    })
    class get_Filter(Resource):
        def get(self):
            queryFilter = request.args
            applicants = ApplicantsModel.query.filter_by(**queryFilter).all()
            applicantsSchema = ApplicantsModelSchema(many= True)
            output = applicantsSchema.dump(applicants)
            return {'applicants': output}
    # -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------