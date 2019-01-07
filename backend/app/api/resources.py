from app.api import apiRestful
from app.api.modules import requireAuth, convertDataframeToListedJson
from app.config import Config
from app.extensions import db
from app.ormmodels import AttendanceLogsModel, ApplicantsModel, CurriculumsModel, MembersModel
from app.ormmodels import AttendanceLogsModelSchema, ApplicantsModelSchema, CurriculumsModelSchema, MembersModelSchema
from datetime import datetime, timedelta
from flask import request
from flask_restplus import Resource     # Reference : http://flask-restplus.readthedocs.io
from sqlalchemy import func
import pandas as pd


# # ---------------------------[ SecureResource ]----------------------------------
# # Calls requireAuth decorator on all requests
# class SecureResource(Resource):
#     method_decorators = [requireAuth]
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
            return {'return': output}, 200
    # ---------------------------------------------------------------------------


    # ----------------[ Get Curriculums, joined to Members counts ]--------------
    @apiRestful.route('/resource/curriculums/withmembercount')
    class get_Curriculums_WithMemberCount(Resource):

        def get(self):
            curriculumList = CurriculumsModel.query.with_entities(CurriculumsModel.curriculumNo, CurriculumsModel.curriculumCategory, CurriculumsModel.ordinalNo, CurriculumsModel.curriculumName, func.concat(CurriculumsModel.startDate, '~', CurriculumsModel.endDate).label('curriculumPeriod'), CurriculumsModel.curriculumType).subquery()
            applicantCount = ApplicantsModel.query.with_entities(ApplicantsModel.curriculumNo, func.count(ApplicantsModel.phoneNo).label('ApplicantCount')).group_by(ApplicantsModel.curriculumNo).subquery()
            memberCount = MembersModel.query.with_entities(MembersModel.curriculumNo, func.count(MembersModel.phoneNo).label('MemberCount')).filter(MembersModel.attendanceCheck == 'Y').group_by(MembersModel.curriculumNo).subquery()
            memberCompleteCount = MembersModel.query.with_entities(MembersModel.curriculumNo, func.count(MembersModel.phoneNo).label('MemberCompleteCount')).filter(MembersModel.curriculumComplete == 'Y').group_by(MembersModel.curriculumNo).subquery()
            memberEmploymentCount = MembersModel.query.with_entities(MembersModel.curriculumNo, func.count(MembersModel.phoneNo).label('MemberEmploymentCount')).filter(MembersModel.employment == 'Y').group_by(MembersModel.curriculumNo).subquery()
            query = db.session.query(curriculumList).with_entities(curriculumList, func.ifnull(applicantCount.c.ApplicantCount, 0).label('ApplicantCount'), func.ifnull(memberCount.c.MemberCount, 0).label('MemberCount'), func.ifnull(memberCompleteCount.c.MemberCompleteCount, 0).label('MemberCompleteCount'), func.ifnull(memberEmploymentCount.c.MemberEmploymentCount, 0).label('MemberEmploymentCount')).outerjoin(applicantCount, curriculumList.c.curriculumNo == applicantCount.c.curriculumNo).outerjoin(memberCount, curriculumList.c.curriculumNo == memberCount.c.curriculumNo).outerjoin(memberCompleteCount, curriculumList.c.curriculumNo == memberCompleteCount.c.curriculumNo).outerjoin(memberEmploymentCount, curriculumList.c.curriculumNo == memberEmploymentCount.c.curriculumNo)

            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql'))
            output = convertDataframeToListedJson(df)

            return {'return': output}, 200
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
            return {'return': output}, 200
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
            attendanceDate = datetime.utcnow() + timedelta(hours= 9) # Calculate Korea Standard Time(KST)

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
            return {'return': output}, 200
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
            return {'return': output}, 200
    # -----------------------------------------------------------------------------


    #--------[ POST Raw Excel File(Google Survey) to Applicants and Members ]------
    @apiRestful.route('/resource/applicants/bulk')
    @apiRestful.doc(params= {
                    'curriculumNo': {'in': 'formData', 'description': 'application/json, body required'},
                    'applicantsBulkXlsxFile': {'in': 'formData', 'type': 'file', 'description': 'application/json, body/xlsx file required'},
                    # You can add formData columns if needed.
    })
    class post_Applicants_Bulk(Resource):

        def post(self):
            # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
            # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            curriculumNoFromClient = request.form['curriculumNo']
            applicantsbulkFromClient = request.files['applicantsBulkXlsxFile']

            applicantsDf = pd.read_excel(applicantsbulkFromClient)
            applicantsDf.columns = applicantsDf.columns.map(lambda x: Config.XLSX_COLUMNS_TO_SCHEMA_MAP[ x[:4]+'_'+str(len(x)//19) ])       # Using "x[:4]+'_'+str(len(x)//19)" as a unique key.
            applicantsDf['curriculumNo'] = curriculumNoFromClient               # Add a new 'curriculumNo' column
            membersDf = applicantsDf[[
                            'phoneNo',
                            'curriculumNo'
                        ]]      # Extract Members Table bulk records' Primary key

            applicantsListedJson = convertDataframeToListedJson(applicantsDf)
            membersListedJson = convertDataframeToListedJson(membersDf)

            newBulkApplicants = [ApplicantsModel(**applicant) for applicant in applicantsListedJson]
            newBulkMembers = [MembersModel(**member) for member in membersListedJson]

            try:
                db.session.add_all(newBulkApplicants)
                db.session.add_all(newBulkMembers)
                db.session.commit()
                return {'return': {'message': f'Applicants/Members Bulk inserted. curriculumNo={curriculumNoFromClient}, bulk={applicantsListedJson}'}}, 201
            except:
                db.session.rollback()
                return {'return': {'message': 'Something went wrong'}}, 500
    # -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------