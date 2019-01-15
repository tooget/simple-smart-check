from app.api import apiRestful
from app.api.modules import requireAuth, convertDataframeToDictsList, createOrmModelQueryFiltersDict
from app.config import Config
from app.extensions import db
from app.ormmodels import AttendanceLogsModel, ApplicantsModel, CurriculumsModel, MembersModel
from app.ormmodels import AttendanceLogsModelSchema, ApplicantsModelSchema, CurriculumsModelSchema, MembersModelSchema
from datetime import datetime, timedelta
from flask import request
from flask_restplus import Resource     # Reference : http://flask-restplus.readthedocs.io
from json import dumps, loads
from operator import attrgetter
from sqlalchemy import and_, func
from copy import deepcopy
import pandas as pd


# # ---------------------------[ SecureResource ]----------------------------------
# # Calls requireAuth decorator on all requests
# class SecureResource(Resource):
#     method_decorators = [requireAuth]
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
            'filters': {'in': 'query', 'description': 'URL parameter, optional'},
            'sort': {'in': 'query', 'description': 'URL parameter, optional'},
            'pagination': {'in': 'query', 'description': 'URL parameter, optional'},
            # You can add query filter columns if needed.
    })
    class get_Curriculums_Filter(Resource):

        def get(self):
            queryParams = {key: loads(request.args[key]) for key in request.args}

            ormQueryFilters = createOrmModelQueryFiltersDict(queryParams['filters'])
            filters = (getattr(CurriculumsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['CurriculumsModel'].items())

            sortFromClient = queryParams['sort']
            sortTarget, sortOption = sortFromClient['target'], sortFromClient['value']
            sort = getattr(getattr(CurriculumsModel, sortTarget), sortOption)()

            paginationFromClient = queryParams['pagination']
            pagenum, limit = paginationFromClient['pagenum'], paginationFromClient['limit']
            start, stop = (pagenum-1)*limit, pagenum*limit

            query = CurriculumsModel.query.filter(and_(*filters))
            curriculums = query.order_by(sort).slice(start, stop).all()

            curriculumsSchema = CurriculumsModelSchema(many= True)
            output = curriculumsSchema.dump(curriculums)

            total = query.count()

            return {'return': {'items': output, 'total': total}}, 200
    # ---------------------------------------------------------------------------


    # ----------------[ Create a new Curriculums data ]----------------------------
    @apiRestful.route('/resource/curriculums')
    @apiRestful.doc(params= {
            'curriculumCategory': {'in': 'formData', 'description': 'application/json, body required'},
            'ordinalNo': {'in': 'formData', 'description': 'application/json, body required'},
            'curriculumName': {'in': 'formData', 'description': 'application/json, body required'},
            'curriculumType': {'in': 'formData', 'description': 'application/json, body required'},
            'startDate': {'in': 'formData', 'description': 'application/json, body required'},
            'endDate': {'in': 'formData', 'description': 'application/json, body required'},
            # You can add formData columns if needed.
    })
    class post_Curriculums(Resource):

        def post(self):
            # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
            # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            infoFromClient = request.form
            curriculumCategoryFromClient = infoFromClient['curriculumCategory']
            ordinalNoFromClient = infoFromClient['ordinalNo']
            curriculumNameFromClient = infoFromClient['curriculumName']
            curriculumTypeFromClient = infoFromClient['curriculumType']
            startDateFromClient = datetime.fromtimestamp(int(infoFromClient['startDate']) / 1000.0).strftime('%Y-%m-%d')      # Divide by 1000.0, to preserve the millisecond accuracy 
            endDateFromClient = datetime.fromtimestamp(int(infoFromClient['endDate']) / 1000.0).strftime('%Y-%m-%d')      # Divide by 1000.0, to preserve the millisecond accuracy

            requestedBody = {
                "curriculumCategory": curriculumCategoryFromClient,
                "ordinalNo": ordinalNoFromClient,
                "curriculumName": curriculumNameFromClient,
                "curriculumType": curriculumTypeFromClient,
                "startDate": startDateFromClient,
                "endDate": endDateFromClient,
            }
            
            CurriculumsData = CurriculumsModel(**requestedBody)

            try:
                db.session.add(CurriculumsData)
                db.session.commit()
                requestedBody['curriculumNo'] = CurriculumsData.curriculumNo
                curriculums = CurriculumsModel.query.filter_by(**requestedBody).one()
                curriculumsSchema = CurriculumsModelSchema(many= False)
                argument = curriculumsSchema.dump(curriculums)
                argumentToJson = dumps(argument)
                return {'message': { 'title': '成功', 'content': '创建成功', },
                        'return': { 
                            'argument': f'{argumentToJson}'
                        }}, 201
            except:
                db.session.rollback()
                return {'message': { 'title': '失敗', 'content': '创建失敗', }}, 500
    # ---------------------------------------------------------------------------


    # ----------------[ Update a new Curriculums data ]----------------------------
    @apiRestful.route('/resource/curriculums')
    @apiRestful.doc(params= {
            'curriculumNo': {'in': 'formData', 'description': 'application/json, body required'},
            'curriculumCategory': {'in': 'formData', 'description': 'application/json, body required'},
            'ordinalNo': {'in': 'formData', 'description': 'application/json, body required'},
            'curriculumName': {'in': 'formData', 'description': 'application/json, body required'},
            'curriculumType': {'in': 'formData', 'description': 'application/json, body required'},
            'startDate': {'in': 'formData', 'description': 'application/json, body required'},
            'endDate': {'in': 'formData', 'description': 'application/json, body required'},
            # You can add formData columns if needed.
    })
    class put_Curriculums(Resource):

        def put(self):
            # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
            # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            infoFromClient = request.form
            curriculumNoFromClient = int(infoFromClient['curriculumNo'])
            curriculumCategoryFromClient = infoFromClient['curriculumCategory']
            ordinalNoFromClient = infoFromClient['ordinalNo']
            curriculumNameFromClient = infoFromClient['curriculumName']
            curriculumTypeFromClient = infoFromClient['curriculumType']
            startDateFromClient = datetime.fromtimestamp(int(infoFromClient['startDate']) / 1000.0).strftime('%Y-%m-%d')      # Divide by 1000.0, to preserve the millisecond accuracy 
            endDateFromClient = datetime.fromtimestamp(int(infoFromClient['endDate']) / 1000.0).strftime('%Y-%m-%d')      # Divide by 1000.0, to preserve the millisecond accuracy

            requestedBody = {
                "curriculumNo": curriculumNoFromClient,
                "curriculumCategory": curriculumCategoryFromClient,
                "ordinalNo": ordinalNoFromClient,
                "curriculumName": curriculumNameFromClient,
                "curriculumType": curriculumTypeFromClient,
                "startDate": startDateFromClient,
                "endDate": endDateFromClient,
            }
            
            CurriculumsData = CurriculumsModel(**requestedBody)

            try:
                db.session.merge(CurriculumsData)      # session.merge() : A kind of UPSERT, https://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#merging
                db.session.commit()
                curriculums = CurriculumsModel.query.filter_by(**requestedBody).one()
                curriculumsSchema = CurriculumsModelSchema(many= False)
                argument = curriculumsSchema.dump(curriculums)
                argumentToJson = dumps(argument)
                return {'message': { 'title': '成功', 'content': '更新成功', },
                        'return': {
                            'argument': f'{argumentToJson}'
                        }}, 201
            except:
                db.session.rollback()
                return {'message': { 'title': '失敗', 'content': '更新失敗', }}, 500
    # ---------------------------------------------------------------------------


    # ----------------[ Delete a Curriculums data ]----------------------------
    @apiRestful.route('/resource/curriculums')
    @apiRestful.doc(params= {
            'curriculumNo': {'in': 'formData', 'description': 'application/json, body required'},
            # You can add formData columns if needed.
    })
    class delete_Curriculums(Resource):

        def delete(self):
            # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
            # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            infoFromClient = request.form
            curriculumNoFromClient = int(infoFromClient['curriculumNo'])
            requestedBody = { "curriculumNo": curriculumNoFromClient }
            curriculums = CurriculumsModel.query.filter_by(**requestedBody).one()

            try:
                db.session.delete(curriculums)      # session.delete() : A kind of DELETE, http://flask-sqlalchemy.pocoo.org/latest/queries/#deleting-records
                db.session.commit()
                return {'message': {'title': '成功', 'content': '删除成功'}}, 201
            except:
                db.session.rollback()
                return {'message': 'Something went wrong'}, 500
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
            query = db.session.query(curriculumList).with_entities( \
                                                        curriculumList, \
                                                        func.ifnull(applicantCount.c.ApplicantCount, 0).label('ApplicantCount'), \
                                                        func.ifnull(memberCount.c.MemberCount, 0).label('MemberCount'), \
                                                        func.ifnull(memberCompleteCount.c.MemberCompleteCount, 0).label('MemberCompleteCount'), \
                                                        func.ifnull(memberEmploymentCount.c.MemberEmploymentCount, 0).label('MemberEmploymentCount'))   \
                                                    .outerjoin(applicantCount, curriculumList.c.curriculumNo == applicantCount.c.curriculumNo)  \
                                                    .outerjoin(memberCount, curriculumList.c.curriculumNo == memberCount.c.curriculumNo)    \
                                                    .outerjoin(memberCompleteCount, curriculumList.c.curriculumNo == memberCompleteCount.c.curriculumNo)    \
                                                    .outerjoin(memberEmploymentCount, curriculumList.c.curriculumNo == memberEmploymentCount.c.curriculumNo)    \

            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql'))
            output = convertDataframeToDictsList(df)
            total = query.count()

            return {'return': {'items': output, 'total': total}}, 200
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
            attendanceLogs = AttendanceLogsModel.query.filter_by(**queryFilter)
            attendanceLogsSchema = AttendanceLogsModelSchema(many= True)
            output = attendanceLogsSchema.dump(attendanceLogs.all())
            total = attendanceLogs.count()

            return {'return': {'items': output, 'total': total}}, 200
    # ---------------------------------------------------------------------------


    # ----------------[ Get attendance list of a specific curriculum ]-----------
    @apiRestful.route('/resource/attendancelogs/list')
    @apiRestful.doc(params= {
            'curriculumNo': {'in': 'query', 'description': 'URL parameter, reqired'},
    })
    class get_AttendanceLogs_List(Resource):

        def get(self):
            queryFilter = request.args
            
            attendanceLogs = AttendanceLogsModel.query.filter_by(**queryFilter)
            # Get full duration of a curriculum.
            curriculumDuration = CurriculumsModel.query.with_entities(CurriculumsModel.startDate, CurriculumsModel.endDate).filter_by(**queryFilter).first()
            startDate, endDate = curriculumDuration.startDate.strftime('%Y-%m-%dT%H:%M:%SZ'), curriculumDuration.endDate.strftime('%Y-%m-%dT%H:%M:%SZ')
            curriculumDuration = set([date.strftime('%Y-%m-%d') for date in pd.date_range(start= startDate, end= endDate, freq= 'B')])
            # Get entire members list of a curriculum.
            membersPhoneNoList = MembersModelSchema(many= True).dump( MembersModel.query.with_entities(MembersModel.phoneNo).filter_by(**queryFilter, attendanceCheck= 'Y').all() )
            membersPhoneNoList = set([phoneNoDict['phoneNo'] for phoneNoDict in membersPhoneNoList])

            # Pivot Attendance Check-Table for now.
            attendanceLogsDf = pd.read_sql(attendanceLogs.statement, db.get_engine(bind= 'mysql'))
            attendanceLogsDf['attendanceDate'] = attendanceLogsDf['attendanceDate'].astype(str)
            pivot = attendanceLogsDf.set_index(['phoneNo', 'checkInOut', 'attendanceDate'])[['signature', 'insertedTimestamp']]
            pivot['signatureTimestamp'] = pivot['signature'] + '\n' + pivot['insertedTimestamp'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').astype(str)
            pivot = pivot.drop(columns= ['signature', 'insertedTimestamp']).unstack(level= [2, 1]).sort_index(axis= 'columns', level= 1)

            # Create Full Attendance Check-Table with Nan values.
            iterables = [
                list(set(pivot.columns.get_level_values(0))),
                curriculumDuration,
                list(set(pivot.columns.get_level_values(2))),
            ]
            emptyAttendanceTableDF = pd.DataFrame(
                index= membersPhoneNoList,
                columns= pd.MultiIndex.from_product(iterables, names= pivot.columns.names),
            )
            emptyAttendanceTableDF.index.name = pivot.index.name
            # Overlay and Update the pivot table.
            pivot = pivot.combine_first(emptyAttendanceTableDF)

            # Make ListedJson for Vue Element-Ui to visualize a multicolumn Table.
            pivotLebels = list(map(lambda x: x.tolist(), pivot.columns.levels))
            signatureTimestampLevel, insertedTimestampLevel, checkInOutLevel = pivotLebels
            vueElementUiListedJson = list()
            signatureTimestampListItem = dict()
            vueElementUiListedJsonItem = dict()
            signatureTimestampList = list()
            for phoneNo, row in pivot.iterrows():
                for signatureTimestampLabel, insertedTimestampLabel, checkInOutLabel in zip(*pivot.columns.labels):
                    level1 = signatureTimestampLevel[signatureTimestampLabel]
                    level2 = insertedTimestampLevel[insertedTimestampLabel]
                    level3 = checkInOutLevel[checkInOutLabel]            
                    value = row[level1][level2][level3]
                    signatureTimestampListItem.update({'attendanceDate': level2})
                    signatureTimestampListItem.update({level3: value})
                    if checkInOutLabel == 1:
                        signatureTimestampList.append(deepcopy(signatureTimestampListItem))

                vueElementUiListedJsonItem.update({'phoneNo': phoneNo})
                vueElementUiListedJsonItem.update({'signatureTimestamp': deepcopy(signatureTimestampList)})
                vueElementUiListedJson.append(deepcopy(vueElementUiListedJsonItem))

            output = vueElementUiListedJson
            total = attendanceLogs.count()

            return {'return': {'items': output, 'total': total}}, 200
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
            infoFromClient = request.form
            phoneNoFromClient = infoFromClient['phoneNo']               # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            curriculumNoFromClient = infoFromClient['curriculumNo']
            checkInOutFromClient = infoFromClient['checkInOut']
            signatureFromClient = infoFromClient['signature'].split(',')[-1].strip()
            attendanceDate = (datetime.utcnow() + timedelta(hours= 9)).strftime('%Y-%m-%d')     # Calculate Korea Standard Time(KST), date only

            requestedBody = {
                "phoneNo": phoneNoFromClient,
                "curriculumNo": curriculumNoFromClient,
                "checkInOut": checkInOutFromClient,
                "signature": signatureFromClient,
                "attendanceDate": attendanceDate,
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
            members = MembersModel.query.filter_by(**queryFilter)
            membersSchema = MembersModelSchema(many= True)
            output = membersSchema.dump(members.all())
            total = members.count()

            return {'return': {'items': output, 'total': total}}, 200
    # -----------------------------------------------------------------------------


    # ----------------[ Get Curriculums ]---------------------------------------
    @apiRestful.route('/resource/members/list')
    @apiRestful.doc(params= {
            'filters': {'in': 'query', 'description': 'URL parameter, optional'},
            'sort': {'in': 'query', 'description': 'URL parameter, optional'},
            'pagination': {'in': 'query', 'description': 'URL parameter, optional'},
            # You can add query filter columns if needed.
    })
    class get_Members_List(Resource):

        def get(self):
            queryParams = {key: loads(request.args[key]) for key in request.args}

            ormQueryFilters = createOrmModelQueryFiltersDict(queryParams['filters'])
            # ormQuerySort = createOrmModelQueryFiltersDict(queryParams['sort'])

            memberFilters = (getattr(MembersModel, target) == value for target, value in ormQueryFilters['MembersModel'].items())
            # memberSort = (getattr(MembersModel, target) == value for target, value in ormQuerySort['MembersModel'].items())
            curriculumLikeFilters = (getattr(CurriculumsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['CurriculumsModel'].items())
            # curriculumSort = (getattr(MembersModel, target) == value for target, value in ormQuerySort['CurriculumsModel'].items())
            applicantLikeFilters = (getattr(ApplicantsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['ApplicantsModel'].items())
            # applicantSort = (getattr(MembersModel, target) == value for target, value in ormQuerySort['ApplicantsModel'].items())

            membersQuery = MembersModel.query.with_entities(
                                            MembersModel.phoneNo,
                                            MembersModel.curriculumNo,
                                            MembersModel.attendancePass,
                                            MembersModel.attendanceCheck,
                                            MembersModel.curriculumComplete,
                                            MembersModel.employment,
                                        ).filter(and_(*memberFilters))  \
                                        .subquery()
            curriculumsQuery = CurriculumsModel.query.filter(and_(*curriculumLikeFilters))  \
                                        .subquery()
            applicantsQuery = ApplicantsModel.query.filter(and_(*applicantLikeFilters)) \
                                        .subquery()

            paginationFromClient = queryParams['pagination']
            pagenum, limit = paginationFromClient['pagenum'], paginationFromClient['limit']
            start, stop = (pagenum-1)*limit, pagenum*limit

            query = db.session.query(membersQuery).with_entities(
                                            membersQuery,
                                            curriculumsQuery.c.ordinalNo,
                                            curriculumsQuery.c.curriculumName,
                                            curriculumsQuery.c.curriculumCategory,
                                            curriculumsQuery.c.startDate,
                                            curriculumsQuery.c.endDate,
                                            applicantsQuery.c.applicantName,
                                            applicantsQuery.c.birthDate,
                                            applicantsQuery.c.email,
                                            applicantsQuery.c.affiliation,
                                            applicantsQuery.c.department,
                                            applicantsQuery.c.position,
                                            applicantsQuery.c.job,
                                            applicantsQuery.c.purposeSelection,
                                            applicantsQuery.c.careerDuration,
                                            applicantsQuery.c.agreeWithPersonalinfo,
                                            applicantsQuery.c.agreeWithMktMailSubscription,
                                            applicantsQuery.c.operationMemo,
                                        ).outerjoin(curriculumsQuery, curriculumsQuery.c.curriculumNo == membersQuery.c.curriculumNo)  \
                                        .outerjoin(applicantsQuery, and_(applicantsQuery.c.curriculumNo == membersQuery.c.curriculumNo, applicantsQuery.c.phoneNo == membersQuery.c.phoneNo))
            query = query.slice(start, stop)

            # sortFromClient = queryParams['sort']
            # sortTarget, sortOption = sortFromClient['target'], sortFromClient['value']
            # sort = getattr(getattr(query, sortTarget), sortOption)()      # AttributeError: 'BaseQuery' object has no attribute 'phoneNo'
            # query = query.order_by(sort).slice(start, stop)

            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql'))
            output = convertDataframeToDictsList(df)

            total = query.count()

            return {'return': {'items': output, 'total': total}}, 200
    # ---------------------------------------------------------------------------


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
            infoFromClient = request.form
            requestedBody = {
                'phoneNo': infoFromClient['phoneNo'],                   # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                'curriculumNo': infoFromClient['curriculumNo'],
                'attendancePass': infoFromClient['attendancePass'],
                'attendanceCheck': infoFromClient['attendanceCheck'],
                'curriculumComplete': infoFromClient['curriculumComplete'],
                'employment': infoFromClient['employment'],
            }

            memberInfo = MembersModel(**requestedBody)

            try:
                db.session.merge(memberInfo)      # session.merge() : A kind of UPSERT, https://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#merging
                db.session.commit()
                return {'message': f'MemberInfo updated : {requestedBody}'}, 201
            except:
                db.session.rollback()
                return {'message': 'Something went wrong'}, 500
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
            applicants = ApplicantsModel.query.filter_by(**queryFilter)
            applicantsSchema = ApplicantsModelSchema(many= True)
            output = applicantsSchema.dump(applicants.all())
            total = applicants.count()

            return {'return': {'items': output, 'total': total}}, 200
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
            curriculumNoFromClient = request.form['curriculumNo']               # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            applicantsbulkFromClient = request.files['applicantsBulkXlsxFile']

            applicantsDf = pd.read_excel(applicantsbulkFromClient)
            applicantsDf.columns = applicantsDf.columns.map(lambda x: Config.XLSX_COLUMNS_TO_SCHEMA_MAP[ x[:4]+'_'+str(len(x)//19) ])       # Convert column names, Using "x[:4]+'_'+str(len(x)//19)" as a unique key
            applicantsDf['curriculumNo'] = curriculumNoFromClient
            membersDf = applicantsDf[['phoneNo', 'curriculumNo']]

            applicantsDictsList = convertDataframeToDictsList(applicantsDf)
            membersDictsList = convertDataframeToDictsList(membersDf)

            oldBulkApplicants = ApplicantsModel.query.filter(curriculumNo= curriculumNoFromClient)
            oldBulkMembers = MembersModel.query.filter(curriculumNo= curriculumNoFromClient)
            oldBulkAttendanceLogs = AttendanceLogsModel.filter(curriculumNo= curriculumNoFromClient)
            newBulkApplicants = [ApplicantsModel(**applicant) for applicant in applicantsDictsList]
            newBulkMembers = [MembersModel(**member) for member in membersDictsList]

            try:
                # Delete old applicants/members of a curriculumn.
                db.session.delete(oldBulkApplicants.all())
                db.session.delete(oldBulkMembers.all())
                db.session.delete(oldBulkAttendanceLogs.all())
                # Add new applicants/members of a curriculumn.
                db.session.add_all(newBulkApplicants)
                db.session.add_all(newBulkMembers)
                db.session.commit()
                return {'message': f'Applicants/Members Bulk : curriculumNo {curriculumNoFromClient}, {len(newBulkApplicants)} records are inserted.'}, 201
            except:
                db.session.rollback()
                return {'message': 'Something went wrong'}, 500
    # -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------