from app.api import apiRestful
from app.api.modules import requireAuth, convertDataframeToDictsList, createOrmModelQueryFiltersDict, createOrmModelQuerySortDict
from app.config import Config
from app.extensions import db
from app.ormmodels import AttendanceLogsModel, ApplicantsModel, CurriculumsModel, MembersModel
from app.ormmodels import AttendanceLogsModelSchema, ApplicantsModelSchema, CurriculumsModelSchema, MembersModelSchema
from base64 import b64encode, b64decode
from copy import deepcopy
from datetime import datetime, timedelta
from flask import request, send_file
from flask_restplus import Resource     # Reference : http://flask-restplus.readthedocs.io
from io import BytesIO
from json import dumps, loads
from operator import attrgetter
from sqlalchemy import and_, func, null
from sqlalchemy_utils import sort_query
from PIL import Image
from zlib import compress, decompress
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
            query = CurriculumsModel.query.filter(and_(*filters))
            total = query.count()
            
            paginationLimitConverter = lambda x: x if bool(x) == True else total
            paginationFromClient = queryParams['pagination']
            pagenum = paginationFromClient['pagenum']
            limit = paginationLimitConverter(paginationFromClient['limit'])
            start, stop = (pagenum-1)*limit, pagenum*limit

            ormQuerySort = createOrmModelQuerySortDict(queryParams['sort'])
            query = sort_query(query, *ormQuerySort).slice(start, stop)
            curriculums = query.all()

            curriculumsSchema = CurriculumsModelSchema(many= True)
            output = curriculumsSchema.dump(curriculums)

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
                return {'message': { 'title': 'Succeeded', 'content': 'New Curriculum Created', },
                        'return': { 
                            'argument': f'{argumentToJson}'
                        }}, 201
            except:
                db.session.rollback()
                return {'message': { 'title': 'Failed', 'content': 'New Curriculum creation failed', }}, 500
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
                return {'message': { 'title': 'Succeeded', 'content': 'Curriculum info updated', },
                        'return': {
                            'argument': f'{argumentToJson}'
                        }}, 201
            except:
                db.session.rollback()
                return {'message': { 'title': 'Failed', 'content': 'Updating Curriculum info failed', }}, 500
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
            targetCurriculumRecord = CurriculumsModel.query.filter_by(**requestedBody).one()
            targetApplicants = ApplicantsModel.query.filter_by(curriculumNo= curriculumNoFromClient).all()
            targetMembers = MembersModel.query.filter_by(curriculumNo= curriculumNoFromClient).all()
            targetAttendanceLogs = AttendanceLogsModel.query.filter_by(curriculumNo= curriculumNoFromClient).all()

            try:
                db.session.delete(targetCurriculumRecord)           # session.delete() : A kind of DELETE, http://flask-sqlalchemy.pocoo.org/latest/queries/#deleting-records
                for record in targetApplicants:
                    db.session.delete(record)
                for record in targetMembers:
                    db.session.delete(record)
                for record in targetAttendanceLogs:
                    db.session.delete(record)
                db.session.commit()
                return {'message': {'title': 'Succeeded', 'content': 'Curriculum/all the relavant data deleted'}}, 201
            except:
                db.session.rollback()
                return {'message': 'Something went wrong'}, 500
    # ---------------------------------------------------------------------------  


    # ----------------[ Get Curriculums, joined to Members counts ]--------------
    @apiRestful.route('/resource/curriculums/withmembercount')
    class get_Curriculums_WithMemberCount(Resource):

        def get(self):
            queryParams = {key: loads(request.args[key]) for key in request.args}

            ormQueryFilters = createOrmModelQueryFiltersDict(queryParams['filters'])
            # ormQuerySort = createOrmModelQuerySortDict(queryParams['sort'])

            pagenum, limit = int(queryParams['pagination']['pagenum']), int(queryParams['pagination']['limit'])
            start, stop = (pagenum-1)*limit, pagenum*limit

            curriculumLikeFilters = (getattr(CurriculumsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['CurriculumsModel'].items())
            applicantLikeFilters = (getattr(ApplicantsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['ApplicantsModel'].items())
            memberFilters = (getattr(MembersModel, target) == value for target, value in ormQueryFilters['MembersModel'].items())

            curriculumList = CurriculumsModel.query.with_entities(CurriculumsModel.curriculumNo, CurriculumsModel.curriculumCategory, CurriculumsModel.ordinalNo, CurriculumsModel.curriculumName, func.concat(CurriculumsModel.startDate, '~', CurriculumsModel.endDate).label('curriculumPeriod'), CurriculumsModel.curriculumType).filter(and_(*curriculumLikeFilters)).subquery()
            applicantCount = ApplicantsModel.query.with_entities(ApplicantsModel.curriculumNo, func.count(ApplicantsModel.phoneNo).label('ApplicantCount')).filter(and_(*applicantLikeFilters)).group_by(ApplicantsModel.curriculumNo).subquery()
            memberCount = MembersModel.query.with_entities(MembersModel.curriculumNo, func.count(MembersModel.phoneNo).label('MemberCount')).filter(and_(MembersModel.attendanceCheck == 'Y', *memberFilters)).group_by(MembersModel.curriculumNo).subquery()
            memberCompleteCount = MembersModel.query.with_entities(MembersModel.curriculumNo, func.count(MembersModel.phoneNo).label('MemberCompleteCount')).filter(and_(MembersModel.curriculumComplete == 'Y', *memberFilters)).group_by(MembersModel.curriculumNo).subquery()
            memberEmploymentCount = MembersModel.query.with_entities(MembersModel.curriculumNo, func.count(MembersModel.phoneNo).label('MemberEmploymentCount')).filter(and_(MembersModel.employment == 'Y', *memberFilters)).group_by(MembersModel.curriculumNo).subquery()
            query = db.session.query(curriculumList).with_entities(
                                                        curriculumList,
                                                        func.ifnull(applicantCount.c.ApplicantCount, 0).label('ApplicantCount'),
                                                        func.ifnull(memberCount.c.MemberCount, 0).label('MemberCount'),
                                                        func.ifnull(memberCompleteCount.c.MemberCompleteCount, 0).label('MemberCompleteCount'),
                                                        func.ifnull(memberEmploymentCount.c.MemberEmploymentCount, 0).label('MemberEmploymentCount'))   \
                                                    .outerjoin(applicantCount, curriculumList.c.curriculumNo == applicantCount.c.curriculumNo)  \
                                                    .outerjoin(memberCount, curriculumList.c.curriculumNo == memberCount.c.curriculumNo)  \
                                                    .outerjoin(memberCompleteCount, curriculumList.c.curriculumNo == memberCompleteCount.c.curriculumNo)  \
                                                    .outerjoin(memberEmploymentCount, curriculumList.c.curriculumNo == memberEmploymentCount.c.curriculumNo)
            total = query.count()
            query = query.slice(start, stop)
            # query = sort_query(query, *ormQuerySort).slice(start, stop)
            
            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql'))
            output = convertDataframeToDictsList(df)

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
            queryFilter = createOrmModelQueryFiltersDict(request.args)
            attendanceLogsFilter = queryFilter['AttendanceLogsModel']
            applicantsFilter = queryFilter['ApplicantsModel']
            curriculumsFilter = queryFilter['CurriculumsModel']

            attendanceLogs = AttendanceLogsModel.query.with_entities(
                                                        AttendanceLogsModel.phoneNo,
                                                        AttendanceLogsModel.curriculumNo,
                                                        AttendanceLogsModel.checkInOut,
                                                        AttendanceLogsModel.attendanceDate,
                                                        AttendanceLogsModel.insertedTimestamp,
                                                    ).filter_by(**attendanceLogsFilter)    \
                                                    .subquery()
            applicnats = ApplicantsModel.query.with_entities(
                                                        ApplicantsModel.curriculumNo,
                                                        ApplicantsModel.phoneNo,
                                                        ApplicantsModel.applicantName,
                                                    ).filter_by(**applicantsFilter)    \
                                                    .subquery()
            curriculums = CurriculumsModel.query.with_entities(
                                                        CurriculumsModel.curriculumNo,
                                                        CurriculumsModel.curriculumName,
                                                    ).filter_by(**curriculumsFilter)   \
                                                    .subquery()

            query = db.session.query(attendanceLogs).with_entities(
                                                        attendanceLogs,
                                                        applicnats.c.applicantName,
                                                        curriculums.c.curriculumName,
                                                    ).outerjoin(applicnats, and_(applicnats.c.curriculumNo == attendanceLogs.c.curriculumNo, applicnats.c.phoneNo == attendanceLogs.c.phoneNo))  \
                                                    .outerjoin(curriculums, curriculums.c.curriculumNo == attendanceLogs.c.curriculumNo)

            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql'))
            output = convertDataframeToDictsList(df)

            total = query.count()

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
            # Get only attendancePassed members and phoneNo list of a curriculum.
            membersAttendancePassOnlyQuery = MembersModel.query.with_entities(MembersModel.phoneNo).filter_by(**queryFilter, attendancePass= 'Y').subquery()
            applicantNameQuery = ApplicantsModel.query.with_entities(ApplicantsModel.phoneNo, ApplicantsModel.applicantName).filter_by(**queryFilter).subquery()
            applicantsNameAndphoneNoQuery = db.session.query(membersAttendancePassOnlyQuery).with_entities(
                                                        membersAttendancePassOnlyQuery,
                                                        applicantNameQuery.c.applicantName
                                                    ).outerjoin(applicantNameQuery, membersAttendancePassOnlyQuery.c.phoneNo == applicantNameQuery.c.phoneNo)
            applicantsNameAndphoneNoList = pd.read_sql(applicantsNameAndphoneNoQuery.statement, db.get_engine(bind= 'mysql'), index_col= 'phoneNo')
            membersPhoneNoList = list(applicantsNameAndphoneNoList.index)
            membersNameList = list(applicantsNameAndphoneNoList['applicantName'])
            if len(membersPhoneNoList) != len(set(membersPhoneNoList)):
                raise KeyError(f'Duplicate PhoneNo exists in curriculum ID {curriculumNo}.')

            # Pivot Attendance Check-Table for now.
            attendanceLogsDf = pd.read_sql(attendanceLogs.statement, db.get_engine(bind= 'mysql'))
            attendanceLogsDf['attendanceDate'] = attendanceLogsDf['attendanceDate'].astype(str)
            attendanceLogsDf['signature'] = attendanceLogsDf['signature'].apply( lambda x: 'signed' )
            pivot = attendanceLogsDf.set_index(['phoneNo', 'checkInOut', 'attendanceDate'])[['signature', 'insertedTimestamp']]
            pivot['signatureTimestamp'] = pivot['signature'] + '\n' + pivot['insertedTimestamp'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').astype(str)
            pivot = pivot.join(applicantsNameAndphoneNoList, on= 'phoneNo')     ##
            pivot = pivot.set_index('applicantName', append= True)              ##
            pivot = pivot.drop(columns= ['signature', 'insertedTimestamp']).unstack(level= [2, 1]).sort_index(axis= 'columns', level= 1)

            # Create Full Attendance Check-Table with Nan values.
            iterables = [
                list(set(pivot.columns.get_level_values(0))),
                curriculumDuration,
                list(set(pivot.columns.get_level_values(2))),
            ]
            phoneNoAndNameIndex = pd.MultiIndex.from_arrays(
                                        [membersPhoneNoList, membersNameList],
                                        names= ('phoneNo', 'applicantName'),
                                  )
            emptyAttendanceTableDF = pd.DataFrame(
                index= phoneNoAndNameIndex,
                columns= pd.MultiIndex.from_product(iterables, names= pivot.columns.names),
            )
            emptyAttendanceTableDF.index.name = pivot.index.name
            # Check attendancePassed members and actually attended applicants who were not attendancePassed.
            attendanceLogsOfapplicantsWithoutAttendnacePass = pivot.index.difference(emptyAttendanceTableDF.index)
            pivot = pivot.drop(attendanceLogsOfapplicantsWithoutAttendnacePass)
            # Overlay and Update the pivot table.
            pivot = pivot.combine_first(emptyAttendanceTableDF)
            # Convert NaN to None.
            pivot = pivot.where((pd.notnull(pivot)), None)

            # Make ListedJson for Vue Element-Ui to visualize a multicolumn Table.
            pivotLebels = list(map(lambda x: x.tolist(), pivot.columns.levels))
            signatureTimestampLevel, insertedTimestampLevel, checkInOutLevel = pivotLebels
            vueElementUiListedJson = list()
            signatureTimestampListItem = dict()
            vueElementUiListedJsonItem = dict()
            signatureTimestampList = list()
            for phoneNoAndNameIdx, row in pivot.iterrows():
                # tuple 'phoneNoAndNameIdx' has phoneNo 'phoneNoAndNameIdx[0]' and applicantName 'phoneNoAndNameIdx[1]'
                for signatureTimestampLabel, insertedTimestampLabel, checkInOutLabel in zip(*pivot.columns.labels):
                    level1 = signatureTimestampLevel[signatureTimestampLabel]
                    level2 = insertedTimestampLevel[insertedTimestampLabel]
                    level3 = checkInOutLevel[checkInOutLabel]            
                    value = row[level1][level2][level3]
                    signatureTimestampListItem.update({'attendanceDate': level2})
                    signatureTimestampListItem.update({level3: value})
                    if checkInOutLabel == 1:
                        signatureTimestampList.append(deepcopy(signatureTimestampListItem))

                vueElementUiListedJsonItem.update({'phoneNo': phoneNoAndNameIdx[0]})
                vueElementUiListedJsonItem.update({'applicantName': phoneNoAndNameIdx[1]})
                vueElementUiListedJsonItem.update({'signatureTimestamp': deepcopy(signatureTimestampList)})
                vueElementUiListedJson.append(deepcopy(vueElementUiListedJsonItem))

            output = vueElementUiListedJson
            total = attendanceLogs.count()

            return {'return': {'items': output, 'total': total}}, 200
    # ---------------------------------------------------------------------------


    # ----------------[ Get attendance list of a specific curriculum ]-----------
    @apiRestful.route('/resource/attendancelogs/listfile')
    @apiRestful.doc(params= {
            'curriculumNo': {'in': 'query', 'description': 'URL parameter, reqired'},
    })
    # Almost same with @apiRestful.route('/resource/attendancelogs/list')
    class get_AttendanceLogs_Listfile(Resource):

        def get(self):
            queryFilter = request.args
            curriculumNo = queryFilter['curriculumNo']

            attendanceLogs = AttendanceLogsModel.query.filter_by(**queryFilter)
            # Get full duration of a curriculum.
            curriculumDuration = CurriculumsModel.query.with_entities(CurriculumsModel.startDate, CurriculumsModel.endDate).filter_by(**queryFilter).first()
            startDate, endDate = curriculumDuration.startDate.strftime('%Y-%m-%dT%H:%M:%SZ'), curriculumDuration.endDate.strftime('%Y-%m-%dT%H:%M:%SZ')
            curriculumDuration = set([date.strftime('%Y-%m-%d') for date in pd.date_range(start= startDate, end= endDate, freq= 'B')])
            # Get only attendancePassed members and phoneNo list of a curriculum.
            membersAttendancePassOnlyQuery = MembersModel.query.with_entities(MembersModel.phoneNo).filter_by(**queryFilter, attendancePass= 'Y').subquery()
            applicantNameQuery = ApplicantsModel.query.with_entities(ApplicantsModel.phoneNo, ApplicantsModel.applicantName).filter_by(**queryFilter).subquery()
            applicantsNameAndphoneNoQuery = db.session.query(membersAttendancePassOnlyQuery).with_entities(
                                                        membersAttendancePassOnlyQuery,
                                                        applicantNameQuery.c.applicantName
                                                    ).outerjoin(applicantNameQuery, membersAttendancePassOnlyQuery.c.phoneNo == applicantNameQuery.c.phoneNo)
            applicantsNameAndphoneNoList = pd.read_sql(applicantsNameAndphoneNoQuery.statement, db.get_engine(bind= 'mysql'), index_col= 'phoneNo')
            membersPhoneNoList = list(applicantsNameAndphoneNoList.index)
            membersNameList = list(applicantsNameAndphoneNoList['applicantName'])
            if len(membersPhoneNoList) != len(set(membersPhoneNoList)):
                raise KeyError(f'Duplicate PhoneNo exists in curriculum ID {curriculumNo}.')

            # Pivot Attendance Check-Table for now.
            attendanceLogsDf = pd.read_sql(attendanceLogs.statement, db.get_engine(bind= 'mysql'))
            attendanceLogsDf['attendanceDate'] = attendanceLogsDf['attendanceDate'].astype(str)
            # attendanceLogsDf['signature'] = attendanceLogsDf['signature'].apply( lambda x: 'signed' )
            attendanceLogsDf['signature'] = attendanceLogsDf['signature'].apply( lambda x: decompress(b64decode(x)).decode() )      # Different from @apiRestful.route('/resource/attendancelogs/list')
            pivot = attendanceLogsDf.set_index(['phoneNo', 'checkInOut', 'attendanceDate'])[['signature', 'insertedTimestamp']]
            # pivot['signatureTimestamp'] = pivot['signature'] + '\n' + pivot['insertedTimestamp'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').astype(str)
            pivot['signatureTimestamp'] = pivot['signature']
            pivot = pivot.join(applicantsNameAndphoneNoList, on= 'phoneNo')
            pivot = pivot.set_index('applicantName', append= True)
            pivot = pivot.drop(columns= ['signature', 'insertedTimestamp']).unstack(level= [2, 1]).sort_index(axis= 'columns', level= 1)

            # Create Full Attendance Check-Table with Nan values.
            iterables = [
                list(set(pivot.columns.get_level_values(0))),
                curriculumDuration,
                list(set(pivot.columns.get_level_values(2))),
            ]
            phoneNoAndNameIndex = pd.MultiIndex.from_arrays(
                                        [membersPhoneNoList, membersNameList],
                                        names= ('phoneNo', 'applicantName'),
                                  )
            emptyAttendanceTableDF = pd.DataFrame(
                index= phoneNoAndNameIndex,
                columns= pd.MultiIndex.from_product(iterables, names= pivot.columns.names),
            )
            emptyAttendanceTableDF.index.name = pivot.index.name
            # Check attendancePassed members and actually attended applicants who were not attendancePassed.
            attendanceLogsOfapplicantsWithoutAttendnacePass = pivot.index.difference(emptyAttendanceTableDF.index)
            pivot = pivot.drop(attendanceLogsOfapplicantsWithoutAttendnacePass)
            # Overlay and Update the pivot table.
            pivot = pivot.combine_first(emptyAttendanceTableDF)

            # -------------------------------------------------------------------
            # Different from 'GET @apiRestful.route('/resource/attendancelogs/list')'
            # -------------------------------------------------------------------
            # create an output stream
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            pivot.to_excel(writer, sheet_name= 'Sheet1')        # taken from the original question

            worksheet = writer.sheets['Sheet1']

            baseCellx, baseCelly = 4, 2     # Data starts from C5 on Spreadsheet

            # Make width of columns and height of rows fit to signature images.
            for rownum in range(pivot.index.size + baseCellx):
                if rownum > 3:
                    worksheet.set_row(rownum, 110)                          # Make Height of rows larger
            
            worksheet.set_column(baseCelly, pivot.columns.size + 1, 25)     # Make Width of Columns after C much larger
            worksheet.set_column(0, baseCelly - 1, 15)                      # Make Width of A:B column larger

            # Insert images to each cell and delete each cell value.
            cells = [(x,y) for x in range(pivot.index.size) for y in range(pivot.columns.size)]
            for rownum, colnum in cells:
                # print( rownum, colnum, str(pivot.iat[rownum, colnum])[:10], type(pivot.iat[rownum,colnum]), bool(pivot.iat[rownum,colnum]) )
                try:
                    signatureImg = BytesIO(b64decode( pivot.iat[rownum,colnum].encode() ))      # Make Image from Base64 String.
                    worksheet.write_string(baseCellx + rownum, baseCelly + colnum, '')
                    worksheet.insert_image(baseCellx + rownum, baseCelly + colnum, f'signature_{baseCellx + rownum}_{baseCelly + colnum}.png', {'image_data': signatureImg, 'x_scale': 0.15, 'y_scale': 0.15})
                except AttributeError:
                    continue

            writer.close()              #the writer has done its job
            output.seek(0)              #go back to the beginning of the stream

            #finally return the file
            return send_file(output, attachment_filename= f'attendance_ID_{curriculumNo}.xlsx', as_attachment=True)
            # -------------------------------------------------------------------
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
            
            rawSignatureStrFromClient = infoFromClient['signature'].split(',')[-1].strip()
            signatureFromClient = compress(                   # use 'compress' to reduce about 30% of binary size : https://stackoverflow.com/questions/28641731/decode-gzip-compressed-and-base64-encoded-data-to-a-readable-format
                                          rawSignatureStrFromClient.encode(),
                                          level= 9,         # -1 ~ 9, maximum compression
                                  )

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


    # ----------------[ Get summary of members count ]-----------------------------
    @apiRestful.route('/resource/members/summarycount')
    @apiRestful.doc(params= {
            'curriculumNo': {'in': 'query', 'description': 'URL parameter, optional'},
            # You can add query filter columns if needed.
    })
    class get_Members_Summarycount(Resource):

        def get(self):
            queryFilter = request.args

            curriculumsQuery = CurriculumsModel.query.with_entities(
                                                CurriculumsModel.curriculumNo,
                                                CurriculumsModel.curriculumName,
                                                CurriculumsModel.curriculumCategory,
                                                CurriculumsModel.ordinalNo,
                                                CurriculumsModel.startDate,
                                                CurriculumsModel.endDate,
                                            ).filter_by(**queryFilter)
            curriculumsSchema = CurriculumsModelSchema(many= True)
            curriculumsInfo = curriculumsSchema.dump(curriculumsQuery.all())
            targetCurriculumsCount = curriculumsQuery.count()

            output = {
                'curriculumInfo': curriculumsInfo,
                'applicants_count': MembersModel.query.filter_by(**queryFilter).count(),
                'members_count': MembersModel.query.filter_by(**queryFilter, attendancePass= 'Y').count(),
                'membersComplete_count': MembersModel.query.filter_by(**queryFilter, curriculumComplete= 'Y').count(),
            }

            total = targetCurriculumsCount

            return {'return': {'items': output, 'total': total}}, 200
    # -----------------------------------------------------------------------------


    # -----------------------[ Get Members ]---------------------------------------
    @apiRestful.route('/resource/members/list')
    @apiRestful.doc(params= {
            'filters': {'in': 'query', 'description': 'URL parameter, required'},
            'sort': {'in': 'query', 'description': 'URL parameter, required'},
            'pagination': {'in': 'query', 'description': 'URL parameter, required'},
            # You can add query filter columns if needed.
    })
    class get_Members_List(Resource):

        def get(self):
            queryParams = {key: loads(request.args[key]) for key in request.args}

            ormQueryFilters = createOrmModelQueryFiltersDict(queryParams['filters'])
            ormQuerySort = createOrmModelQuerySortDict(queryParams['sort'])

            pagenum, limit = int(queryParams['pagination']['pagenum']), int(queryParams['pagination']['limit'])
            start, stop = (pagenum-1)*limit, pagenum*limit

            memberFilters = (getattr(MembersModel, target) == value for target, value in ormQueryFilters['MembersModel'].items())
            curriculumLikeFilters = (getattr(CurriculumsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['CurriculumsModel'].items())
            applicantLikeFilters = (getattr(ApplicantsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['ApplicantsModel'].items())

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
                                        ).join(curriculumsQuery, curriculumsQuery.c.curriculumNo == membersQuery.c.curriculumNo)  \
                                        .join(applicantsQuery, and_(applicantsQuery.c.curriculumNo == membersQuery.c.curriculumNo, applicantsQuery.c.phoneNo == membersQuery.c.phoneNo))
            total = query.count()
            query = sort_query(query, *ormQuerySort).slice(start, stop)
            
            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql'))
            output = convertDataframeToDictsList(df)

            return {'return': {'items': output, 'total': total}}, 200
    # -----------------------------------------------------------------------------


    # -----------------------[ Get Members xlsx file ]-----------------------------
    @apiRestful.route('/resource/members/listfile')
    @apiRestful.doc(params= {
            'filters': {'in': 'query', 'description': 'URL parameter, required'},
            'sort': {'in': 'query', 'description': 'URL parameter, required'},
            # 'pagination': {'in': 'query', 'description': 'URL parameter, optional'},
            # You can add query filter columns if needed.
    })
    # Almost same with @apiRestful.route('/resource/members/list')
    class get_Members_Listfile(Resource):

        def get(self):
            queryParams = {key: loads(request.args[key]) for key in request.args}

            ormQueryFilters = createOrmModelQueryFiltersDict(queryParams['filters'])
            ormQuerySort = createOrmModelQuerySortDict(queryParams['sort'])

            # pagenum, limit = int(queryParams['pagination']['pagenum']), int(queryParams['pagination']['limit'])       # Different from @apiRestful.route('/resource/members/list')
            # start, stop = (pagenum-1)*limit, pagenum*limit                                                            # Different from @apiRestful.route('/resource/members/list')

            memberFilters = (getattr(MembersModel, target) == value for target, value in ormQueryFilters['MembersModel'].items())
            curriculumLikeFilters = (getattr(CurriculumsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['CurriculumsModel'].items())
            applicantLikeFilters = (getattr(ApplicantsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['ApplicantsModel'].items())

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
                                        ).join(curriculumsQuery, curriculumsQuery.c.curriculumNo == membersQuery.c.curriculumNo)  \
                                        .join(applicantsQuery, and_(applicantsQuery.c.curriculumNo == membersQuery.c.curriculumNo, applicantsQuery.c.phoneNo == membersQuery.c.phoneNo))
            # total = query.count()
            # query = sort_query(query, *ormQuerySort).slice(start, stop)       # Different from @apiRestful.route('/resource/members/list')
            query = sort_query(query, *ormQuerySort)
            
            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql'))

            # ---------------------------------------------------------------------
            # Different from @apiRestful.route('/resource/members/list')
            # ---------------------------------------------------------------------
            # create an output stream
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name= 'Sheet1')        # taken from the original question

            writer.close()              # the writer has done its job
            output.seek(0)              # go back to the beginning of the stream

            #finally return the file
            return send_file(output, attachment_filename="members.xlsx", as_attachment=True)
            # ---------------------------------------------------------------------
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
            # Convert empty string to None
            emptyStringToNone = lambda x: x if bool(x) == True else None
            # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
            # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask         
            infoFromClient = {key: emptyStringToNone(request.form[key]) for key in request.form}
            phoneNoFromClient = infoFromClient['phoneNo']
            curriculumNoFromClient = int(infoFromClient['curriculumNo'])
            attendancePassFromClient = infoFromClient['attendancePass']
            attendanceCheckFromClient = infoFromClient['attendanceCheck']
            curriculumCompleteFromClient = infoFromClient['curriculumComplete']
            employmentFromClient = infoFromClient['employment']
            
            requestedBody = {
                'phoneNo': phoneNoFromClient,
                'curriculumNo': curriculumNoFromClient,
                'attendancePass': attendancePassFromClient,
                'attendanceCheck': attendanceCheckFromClient,
                'curriculumComplete': curriculumCompleteFromClient,
                'employment': employmentFromClient,
            }

            membersData = MembersModel(**requestedBody)

            try:
                db.session.merge(membersData)      # session.merge() : A kind of UPSERT, https://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#merging
                db.session.commit()
                members = MembersModel.query.filter_by(**requestedBody).one()
                membersSchema = MembersModelSchema(many= False)
                argument = membersSchema.dump(members)
                argumentToJson = dumps(argument)
                return {'message': { 'title': 'Succeeded', 'content': 'Personal info updated', },
                        'return': {
                            'argument': f'{argumentToJson}'
                        }}, 201
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
            queryParams = {'curriculumNo': int(request.form['curriculumNo'])}               # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            applicantsBulkFromClient = request.files['applicantsBulkXlsxFile']

            applicantsDf = pd.read_excel(applicantsBulkFromClient)
            applicantsDf.columns = applicantsDf.columns.map(lambda x: Config.XLSX_COLUMNS_TO_SCHEMA_MAP[ x[:4]+'_'+str(len(x)//19) ])       # Convert column names, Using "x[:4]+'_'+str(len(x)//19)" as a unique key
            applicantsDf['curriculumNo'] = queryParams['curriculumNo']
            membersDf = applicantsDf[['phoneNo', 'curriculumNo']]

            applicantsDictsList = convertDataframeToDictsList(applicantsDf)
            membersDictsList = convertDataframeToDictsList(membersDf)

            oldBulkApplicants = ApplicantsModel.query.filter_by(curriculumNo= queryParams['curriculumNo']).all()
            oldBulkMembers = MembersModel.query.filter_by(curriculumNo= queryParams['curriculumNo']).all()
            oldBulkAttendanceLogs = AttendanceLogsModel.query.filter_by(curriculumNo= queryParams['curriculumNo']).all()

            newBulkApplicants = [ApplicantsModel(**applicant) for applicant in applicantsDictsList]
            newBulkMembers = [MembersModel(**member) for member in membersDictsList]

            try:
                # Delete old applicants/members of a curriculumn.
                for record in oldBulkApplicants:
                    db.session.delete(record)
                for record in oldBulkMembers:
                    db.session.delete(record)
                for record in oldBulkAttendanceLogs:
                    db.session.delete(record)
                # # Add new applicants/members of a curriculumn.
                db.session.add_all(newBulkApplicants)
                db.session.add_all(newBulkMembers)
                db.session.commit()
                return {'message': { 'title': 'Succeeded', 'content': 'Created/Replaced all the relavant data', }}, 201
            except:
                db.session.rollback()
                return {'message': { 'title': 'Failed', 'content': 'Creating/Replacing all the relavant data failed', }}, 500
    # -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------