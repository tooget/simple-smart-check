from app.api import apiRestful
from app.api.modules import requireAuth, convertDataframeToDictsList, createOrmModelQueryFiltersDict, createOrmModelQuerySortDict
from app.config import Config
from app.extensions import db
from app.ormmodels import AttendanceLogsModel, ApplicantsModel, CurriculumsModel, MembersModel
from app.ormmodels import ApplicantsModelSchema, CurriculumsModelSchema, MembersModelSchema
from base64 import b64encode, b64decode
from copy import deepcopy
from datetime import datetime, timedelta
from flask import request, send_file
from flask_restplus import Resource     # Reference : http://flask-restplus.readthedocs.io
from io import BytesIO
from json import dumps, loads
from PIL import Image, ImageDraw
from sqlalchemy import and_, func
from sqlalchemy_utils import sort_query
from zlib import compress, decompress
import pandas as pd


# ---------------------------[ SecureResource ]----------------------------------
# Calls requireAuth decorator on all requests
# [!] Production must be '(SecureResource)' instead of '(Resource)'
# class SecureResource(Resource):
#     method_decorators = [requireAuth]
# # -------------------------------------------------------------------------------


# ------------------------[ API to manage Curriculums ]-------------------------
class Curriculums:


    @apiRestful.route('/resource/curriculums')
    class Curriculums(Resource):

        # ----------------[ Create a new Curriculums data ]----------------------------
        @apiRestful.doc(params= {
            'curriculumCategory': {'in': 'formData', 'description': 'application/json, body required'},
            'ordinalNo': {'in': 'formData', 'description': 'application/json, body required'},
            'curriculumName': {'in': 'formData', 'description': 'application/json, body required'},
            'curriculumType': {'in': 'formData', 'description': 'application/json, body required'},
            'startDate': {'in': 'formData', 'description': 'application/json, body required'},
            'endDate': {'in': 'formData', 'description': 'application/json, body required'},
            # You can add formData columns if needed.
        })
        def post(self):
            infoFromClient = request.form
            try:
                curriculumCategoryFromClient = infoFromClient['curriculumCategory']     # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                ordinalNoFromClient = infoFromClient['ordinalNo']
                curriculumNameFromClient = infoFromClient['curriculumName']
                curriculumTypeFromClient = infoFromClient['curriculumType']
                startDateFromClient = datetime.fromtimestamp(int(infoFromClient['startDate']) / 1000.0).strftime('%Y-%m-%d')      # Divide by 1000.0, to preserve the millisecond accuracy 
                endDateFromClient = datetime.fromtimestamp(int(infoFromClient['endDate']) / 1000.0).strftime('%Y-%m-%d')      # Divide by 1000.0, to preserve the millisecond accuracy
            except KeyError:
                return {'message': {'title': '교육과정 입력 데이터 오류', 'content': '생성할 교육과정 데이터를 확인해 주시기 바랍니다.'}}, 400

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
                return {'message': {'title': '신규 교육과정 입력 성공', 'content': '새로운 교육과정 데이터가 입력되었습니다.'},
                        'return': { 
                            'argument': f'{argumentToJson}'
                        }}, 201
            except:
                db.session.rollback()
                return {'message': {'title': '신규 교육과정 입력 실패', 'content': '새로운 교육과정 데이터 입력에 실패하였습니다.'}}, 500
        # ---------------------------------------------------------------------------


        # ----------------[ Update a new Curriculums data ]----------------------------
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
        def put(self):
            infoFromClient = request.form
            try:
                curriculumNoFromClient = int(infoFromClient['curriculumNo'])        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                curriculumCategoryFromClient = infoFromClient['curriculumCategory']
                ordinalNoFromClient = infoFromClient['ordinalNo']
                curriculumNameFromClient = infoFromClient['curriculumName']
                curriculumTypeFromClient = infoFromClient['curriculumType']
                startDateFromClient = datetime.fromtimestamp(int(infoFromClient['startDate']) / 1000.0).strftime('%Y-%m-%d')      # Divide by 1000.0, to preserve the millisecond accuracy 
                endDateFromClient = datetime.fromtimestamp(int(infoFromClient['endDate']) / 1000.0).strftime('%Y-%m-%d')      # Divide by 1000.0, to preserve the millisecond accuracy
            except KeyError:
                return {'message': {'title': '교육과정 입력 데이터 오류', 'content': '업데이트할 교육과정 데이터를 확인해 주시기 바랍니다.'}}, 400

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
                return {'message': {'title': '교육과정 업데이트 성공', 'content': '교육과정 정보가 업데이트 되었습니다.'},
                        'return': {
                            'argument': f'{argumentToJson}'
                        }}, 201
            except:
                db.session.rollback()
                return {'message': {'title': '교육과정 업데이트 실패', 'content': '교육과정 정보가 업데이트에 실패하였습니다.'}}, 500
        # ---------------------------------------------------------------------------


        # ----------------[ Delete a Curriculums data ]----------------------------
        @apiRestful.doc(params= {
                'curriculumNo': {'in': 'formData', 'description': 'application/json, body required'},
                # You can add formData columns if needed.
        })
        def delete(self):
            infoFromClient = request.form
            try:
                curriculumNoFromClient = int(infoFromClient['curriculumNo'])        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            except KeyError:
                return {'message': {'title': '삭제대상 교육과정 오류', 'content': '삭제할 교육과정을 확인해 주시기 바랍니다.'}}, 400

            targetCurriculumRecord = CurriculumsModel.query.filter_by(curriculumNo= curriculumNoFromClient).one()
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
                return {'message': {'title': '교육과정 삭제 성공', 'content': '해당 교육과정 정보, 관련 신청자 정보, 출결 및 서명데이터가 모두 삭제되었습니다.'}}, 201
            except:
                db.session.rollback()
                return {'message': {'title': '교육과정 삭제 실패', 'content': '해당 교육과정 및 관련 정보 삭제에 실패하였습니다.'}}, 500
        # ---------------------------------------------------------------------------  


        # ----------------[ Get Curriculums ]---------------------------------------
        @apiRestful.doc(params= {
                'filters': {'in': 'query', 'description': 'URL parameter, required'},
                'sort': {'in': 'query', 'description': 'URL parameter, required'},
                'pagination': {'in': 'query', 'description': 'URL parameter, optional'},
                # You can add query filter columns if needed.
        })
        def get(self):
            infoFromClient = {key: loads(request.args[key]) for key in request.args}
            try:
                filterFromClient = infoFromClient['filters']        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                sortParamFromClient = infoFromClient['sort']
            except KeyError:
                return {'message': {'title': '교육과정 목록조회 오류', 'content': '조회할 교육과정의 기준정보를 확인해 주시기 바랍니다.'}}, 400

            ormQueryFilters = createOrmModelQueryFiltersDict(filterFromClient)
            ormQuerySort = createOrmModelQuerySortDict(sortParamFromClient)

            filters = (getattr(CurriculumsModel, target).like(f'%{value}%') for target, value in ormQueryFilters['CurriculumsModel'].items())
            query = CurriculumsModel.query.filter(and_(*filters))
            query = sort_query(query, *ormQuerySort)
            total = query.count()

            try:
                pagenum, limit = int(infoFromClient['pagination']['pagenum']), int(infoFromClient['pagination']['limit'])
                start, stop = (pagenum - 1) * limit, pagenum * limit
                query = query.slice(start, stop).all()
            except:
                query = query.all()

            curriculumsSchema = CurriculumsModelSchema(many= True)
            output = curriculumsSchema.dump(query)

            return {'message':
                        {'title': '교육과정 목록조회 성공', 'content': f'{total}건의 교육과정을 성공적으로 조회하였습니다.'},
                    'return':
                        {'items': output, 'total': total}
                    }, 200
        # ---------------------------------------------------------------------------


    # ----------------[ Get Curriculums, joined to Members counts ]--------------
    @apiRestful.route('/resource/curriculums/withmembercount')
    @apiRestful.doc(params= {
            'filters': {'in': 'query', 'description': 'URL parameter, required'},
            'sort': {'in': 'query', 'description': 'URL parameter, required'},
            'pagination': {'in': 'query', 'description': 'URL parameter, required'},
            # You can add query filter columns if needed.
    })
    class get_Curriculums_WithMemberCount(Resource):

        def get(self):
            infoFromClient = {key: loads(request.args[key]) for key in request.args}
            try:
                filterFromClient = infoFromClient['filters']        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                sortParamFromClient = infoFromClient['sort']
                pagenum, limit = int(infoFromClient['pagination']['pagenum']), int(infoFromClient['pagination']['limit'])
            except KeyError:
                return {'message': {'title': '교육과정 요약통계 조회 오류', 'content': '요약통계를 조회할 교육과정의 기준정보를 확인해 주시기 바랍니다.'}}, 400

            ormQueryFilters = createOrmModelQueryFiltersDict(filterFromClient)
            ormQuerySort = createOrmModelQuerySortDict(sortParamFromClient)
            start, stop = (pagenum - 1) * limit, pagenum * limit

            curriculumLikeFilters = (getattr(CurriculumsModel, target) == value for target, value in ormQueryFilters.get('CurriculumsModel', dict()).items())
            applicantLikeFilters = (getattr(ApplicantsModel, target) == value for target, value in ormQueryFilters.get('ApplicantsModel', dict()).items())
            memberFilters = (getattr(MembersModel, target) == value for target, value in ormQueryFilters.get('MembersModel', dict()).items())

            curriculumList = CurriculumsModel.query.with_entities(CurriculumsModel.curriculumNo, CurriculumsModel.curriculumCategory, CurriculumsModel.ordinalNo, CurriculumsModel.curriculumName, CurriculumsModel.startDate, CurriculumsModel.endDate, CurriculumsModel.curriculumType).filter(and_(*curriculumLikeFilters)).subquery()
            applicantCount = ApplicantsModel.query.with_entities(ApplicantsModel.curriculumNo, func.count(ApplicantsModel.phoneNo).label('ApplicantCount')).filter(and_(*applicantLikeFilters)).group_by(ApplicantsModel.curriculumNo).subquery()
            memberCount = MembersModel.query.with_entities(MembersModel.curriculumNo, func.count(MembersModel.phoneNo).label('MemberCount')).filter(and_(MembersModel.attendanceCheck == 'Y', *memberFilters)).group_by(MembersModel.curriculumNo).subquery()
            memberCompleteCount = MembersModel.query.with_entities(MembersModel.curriculumNo, func.count(MembersModel.phoneNo).label('MemberCompleteCount')).filter(and_(MembersModel.curriculumComplete == 'Y', *memberFilters)).group_by(MembersModel.curriculumNo).subquery()
            memberEmploymentCount = MembersModel.query.with_entities(MembersModel.curriculumNo, func.count(MembersModel.phoneNo).label('MemberEmploymentCount')).filter(and_(MembersModel.employment == 'Y', *memberFilters)).group_by(MembersModel.curriculumNo).subquery()
            query = db.session.query(curriculumList).with_entities(
                                                        curriculumList.c.curriculumNo.label('curriculumNo'),
                                                        curriculumList.c.curriculumCategory,
                                                        curriculumList.c.ordinalNo,
                                                        curriculumList.c.curriculumName,
                                                        curriculumList.c.startDate,
                                                        curriculumList.c.endDate,
                                                        curriculumList.c.curriculumType,
                                                        func.ifnull(applicantCount.c.ApplicantCount, 0).label('ApplicantCount'),
                                                        func.ifnull(memberCount.c.MemberCount, 0).label('MemberCount'),
                                                        func.ifnull(memberCompleteCount.c.MemberCompleteCount, 0).label('MemberCompleteCount'),
                                                        func.ifnull(memberEmploymentCount.c.MemberEmploymentCount, 0).label('MemberEmploymentCount'))   \
                                                    .outerjoin(applicantCount, curriculumList.c.curriculumNo == applicantCount.c.curriculumNo)  \
                                                    .outerjoin(memberCount, curriculumList.c.curriculumNo == memberCount.c.curriculumNo)  \
                                                    .outerjoin(memberCompleteCount, curriculumList.c.curriculumNo == memberCompleteCount.c.curriculumNo)  \
                                                    .outerjoin(memberEmploymentCount, curriculumList.c.curriculumNo == memberEmploymentCount.c.curriculumNo)
            total = query.count()
            query = sort_query(query, *ormQuerySort).slice(start, stop)
            
            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql-simplesmartcheck'))
            output = convertDataframeToDictsList(df)

            return {'message':
                        {'title': '교육과정 요약통계 조회 성공', 'content': f'{total}건의 교육과정 요약통계를 성공적으로 조회하였습니다.'},
                    'return':
                        {'items': output, 'total': total}
                    }, 200
    # ---------------------------------------------------------------------------
# -------------------------------------------------------------------------------


# ------------------------[ API to manage AttendanceLogs ]-----------------------
class AttendanceLogs:
    
    
    @apiRestful.route('/resource/attendancelogs')
    class AttendanceLogs(Resource):

        # ----------------[ Get new Attendance logs ]--------------------------------
        @apiRestful.doc(params= {
                'phoneNo': {'in': 'query', 'description': 'URL parameter, optional'},
                'curriculumNo': {'in': 'query', 'description': 'URL parameter, optional'},
                'checkInOut': {'in': 'query', 'description': 'URL parameter, optional'},
                'attendanceDate': {'in': 'query', 'description': 'URL parameter, optional'},
                # You can add query filter columns if needed.
        })
        def get(self):
            infoFromClient = request.args
            queryFilter = createOrmModelQueryFiltersDict(infoFromClient)
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

            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql-simplesmartcheck'))
            output = convertDataframeToDictsList(df)

            total = query.count()

            return {'message':
                        {'title': '출결기록 조회 성공', 'content': f'{total}건의 출결기록을 성공적으로 조회하였습니다.'},
                    'return':
                        {'items': output, 'total': total}
                    }, 200
        # ---------------------------------------------------------------------------


        # ----------------[ Create a new AttendanceLog ]----------------------------
        @apiRestful.doc(params= {
                'phoneNo': {'in': 'formData', 'description': 'application/json, body required'},
                'curriculumNo': {'in': 'formData', 'description': 'application/json, body required'},
                'checkInOut': {'in': 'formData', 'description': 'application/json, body required'},
                'signature': {'in': 'formData', 'description': 'application/json, body required'},
                # You can add formData columns if needed.
        })
        def post(self):
            infoFromClient = request.form
            try:
                phoneNoFromClient = infoFromClient['phoneNo']               # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                curriculumNoFromClient = infoFromClient['curriculumNo']
                checkInOutFromClient = infoFromClient['checkInOut']
                signatureB64FromClient = infoFromClient['signature'].split(',')[-1].strip()
            except KeyError:
                return {'message': {'title': '출석데이터 입력오류', 'content': '전화번호, 입실/퇴실, 서명데이터 입력상태를 확인해 주시기 바랍니다.'}}, 400
            
            attendancePassedMemberCheck = MembersModel.query.filter_by(
                                                            curriculumNo= curriculumNoFromClient,
                                                            phoneNo= phoneNoFromClient,
                                                            attendancePass= 'Y',
                                                       ).count()
            if attendancePassedMemberCheck == 1:
                pass
            else:
                return {'message': {'title': '대상자 전화번호 미확인', 'content': '입력한 전화번호 또는 교육과정 선정 여부를 확인해 주시기 바랍니다.'}}, 400

            # Calculate Korea Standard Time(KST), AttendanceDate/Time must be shown as a KST for filtering etc.
            attendanceTimestamp = datetime.utcnow() + timedelta(hours= 9)
            attendanceDate = attendanceTimestamp.strftime('%Y-%m-%d')
            imgTimestamp = attendanceTimestamp.strftime('%Y-%m-%d %H:%M:%S') + ' KST'

            # Get full duration of a curriculum.
            curriculumDuration = CurriculumsModel.query.with_entities(CurriculumsModel.startDate, CurriculumsModel.endDate).filter_by(curriculumNo= curriculumNoFromClient).first()
            startDate, endDate = (curriculumDuration.startDate + timedelta(hours= 9)).strftime('%Y-%m-%dT%H:%M:%SZ'), (curriculumDuration.endDate + timedelta(hours= 9)).strftime('%Y-%m-%dT%H:%M:%SZ')
            curriculumDuration = [date.strftime('%Y-%m-%d') for date in pd.date_range(start= startDate, end= endDate, freq= 'B')]
            if attendanceDate in curriculumDuration:
                pass
            else:
                return {'message': {'title': '출석데이터 일자 오류', 'content': '해당 교육과정의 교육기간 중에 출석데이터를 입력하여 주시기 바랍니다.'}}, 400

            # Resizing Signature Image(width: 500) and Putting timestamp on it.
            signatureImg = Image.open(BytesIO(b64decode( signatureB64FromClient.encode() )))
            imgRatio = signatureImg.height / signatureImg.width
            baseWidthToResize = 400

            resizedSignature = signatureImg.resize((baseWidthToResize, int(baseWidthToResize * imgRatio))).convert('RGBA')
            del signatureImg, signatureB64FromClient
            txt = Image.new('RGBA', resizedSignature.size, (255,255,255,0))
            d = ImageDraw.Draw(txt)
            d.text((resizedSignature.width * 0.1, resizedSignature.height * 0.9), imgTimestamp, fill= (0,0,0,255))
            resizedSignature = Image.alpha_composite(resizedSignature, txt)
            # resizedSignature.show()

            resizedImgBytes = BytesIO()
            resizedSignature.save(resizedImgBytes, format='PNG')
            resizedImgBytesCompressed = compress(resizedImgBytes.getvalue(), level= 9)      # use 'compress' to reduce about 30% of binary size : https://stackoverflow.com/questions/28641731/decode-gzip-compressed-and-base64-encoded-data-to-a-readable-format
            del resizedImgBytes

            # Create a new attendanceLogs record. 
            newAttendanceLogData = {
                "phoneNo": phoneNoFromClient,
                "curriculumNo": curriculumNoFromClient,
                "checkInOut": checkInOutFromClient,
                "signature": resizedImgBytesCompressed,
                "attendanceDate": attendanceDate,
            }
            newAttendanceLog = AttendanceLogsModel(**newAttendanceLogData)
            
            try:
                db.session.add(newAttendanceLog)
                db.session.commit()
                return {'message': {'title': '출석데이터 입력 성공', 'content': '출석 및 서명데이터가 성공적으로 입력되었습니다.'}}, 201
            except:
                db.session.rollback()
                return {'message': {'title': '출석데이터 입력 실패', 'content': '출석 및 서명데이터 입력에 실패하였습니다.'}}, 500
        # ---------------------------------------------------------------------------
    

    # ----------------[ Get attendance list of a specific curriculum ]-----------
    @apiRestful.route('/resource/attendancelogs/list')
    @apiRestful.doc(params= {
            'curriculumNo': {'in': 'query', 'description': 'URL parameter, reqired'},
    })
    class get_AttendanceLogs_List(Resource):

        def get(self):
            infoFromClient = request.args
            try:
                curriculumNoFromClient = int(infoFromClient['curriculumNo'])         # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            except KeyError:
                return {'message': {'title': '조회대상 교육과정 오류', 'content': '조회대상 교육과정을 확인하여 주시기 바랍니다.'}}, 400
            
            attendanceLogs = AttendanceLogsModel.query.filter_by(curriculumNo= curriculumNoFromClient)
            # Get full duration of a curriculum.
            curriculumDuration = CurriculumsModel.query.with_entities(CurriculumsModel.startDate, CurriculumsModel.endDate).filter_by(curriculumNo= curriculumNoFromClient).first()
            startDate, endDate = (curriculumDuration.startDate + timedelta(hours= 9)).strftime('%Y-%m-%dT%H:%M:%SZ'), (curriculumDuration.endDate + timedelta(hours= 9)).strftime('%Y-%m-%dT%H:%M:%SZ')
            curriculumDuration = [date.strftime('%Y-%m-%d') for date in pd.date_range(start= startDate, end= endDate, freq= 'B')]
            # Get only attendancePassed members and phoneNo list of a curriculum.
            membersAttendancePassOnlyQuery = MembersModel.query.with_entities(MembersModel.phoneNo).filter_by(curriculumNo= curriculumNoFromClient, attendancePass= 'Y').subquery()
            applicantNameQuery = ApplicantsModel.query.with_entities(ApplicantsModel.phoneNo, ApplicantsModel.applicantName).filter_by(curriculumNo= curriculumNoFromClient).subquery()
            applicantsNameAndphoneNoQuery = db.session.query(membersAttendancePassOnlyQuery).with_entities(
                                                        membersAttendancePassOnlyQuery,
                                                        applicantNameQuery.c.applicantName
                                                    ).outerjoin(applicantNameQuery, membersAttendancePassOnlyQuery.c.phoneNo == applicantNameQuery.c.phoneNo)
            applicantsNameAndphoneNoList = pd.read_sql(applicantsNameAndphoneNoQuery.statement, db.get_engine(bind= 'mysql-simplesmartcheck'), index_col= 'phoneNo')
            membersPhoneNoList = list(applicantsNameAndphoneNoList.index)
            membersNameList = list(applicantsNameAndphoneNoList['applicantName'])
            if len(membersPhoneNoList) != len(set(membersPhoneNoList)):
                return {'message': {'title': '조회대상 교육과정 교육생 중복오류', 'content': f'조회대상 교육과정의 교육생의 중복된 전화번호가 있습니다.'}}, 400

            # Pivot Attendance Check-Table for now.
            attendanceLogsDf = pd.read_sql(attendanceLogs.statement, db.get_engine(bind= 'mysql-simplesmartcheck'))
            attendanceLogsDf['attendanceDate'] = attendanceLogsDf['attendanceDate'].astype(str)
            pivot = attendanceLogsDf.set_index(['phoneNo', 'checkInOut', 'attendanceDate'])[['signature', 'insertedTimestamp']]
            pivot['signatureTimestamp'] = pivot['insertedTimestamp'].apply( lambda x: x.strftime('%Y-%m-%dT%H:%M:%SZ') ).astype(str)
            pivot = pivot.join(applicantsNameAndphoneNoList, on= 'phoneNo')
            pivot = pivot.set_index('applicantName', append= True)
            pivot = pivot.drop(columns= ['signature', 'insertedTimestamp']).unstack(level= [2, 1]).sort_index(axis= 'columns', level= 1)

            # Create Full Attendance Check-Table with Nan values.
            phoneNoAndNameIndex = pd.MultiIndex.from_arrays(
                                        [membersPhoneNoList, membersNameList],
                                        names= ('phoneNo', 'applicantName'),
                                  )
            pivotedColumnsIndex = pd.MultiIndex.from_product(
                                        [['signatureTimestamp'], curriculumDuration, ['In', 'Out']],
                                        names= (None, 'attendanceDate', 'checkInOut')
                                  )
            emptyAttendanceTableDF = pd.DataFrame(
                                        index= phoneNoAndNameIndex,
                                        columns= pivotedColumnsIndex,
                                  )
            # Check attendancePassed members and actually attended applicants who were not attendancePassed.
            attendanceLogsOfapplicantsWithoutAttendnacePass = pivot.index.difference(emptyAttendanceTableDF.index)
            pivot = pivot.drop(attendanceLogsOfapplicantsWithoutAttendnacePass)

            # Overlay and Update the pivot table.
            pivot = pivot.combine_first(emptyAttendanceTableDF)
            # Convert NaN to None.
            pivot = pivot.where((pd.notnull(pivot)), None)

            # Make ListedJson for Vue Element-Ui to visualize a multicolumn Table.
            signatureTimestampLevel, insertedTimestampLevel, checkInOutLevel = pivot.columns.levels

            vueElementUiListedJson = list()
            vueElementUiListedJsonItem = dict()
            signatureTimestampList = list()
            signatureTimestampListItem = dict()
            
            for (phoneNo, applicantName), row in pivot.iterrows():
                # DataFrame 'pivot' has multiple indexes, and it return them as type of 'tuple' like (phoneNo, applicantName) when pivot.iterrows() working.'
                for signatureTimestampLabel, insertedTimestampLabel, checkInOutLabel in zip(*pivot.columns.labels):
                    level1 = signatureTimestampLevel[signatureTimestampLabel]
                    level2 = insertedTimestampLevel[insertedTimestampLabel]
                    level3 = checkInOutLevel[checkInOutLabel]            
                    value = row[level1][level2][level3]
                    signatureTimestampListItem.update({'attendanceDate': level2})
                    signatureTimestampListItem.update({level3: value})
                    if checkInOutLabel % 2 == 1:
                        signatureTimestampList.append(deepcopy(signatureTimestampListItem))

                vueElementUiListedJsonItem.update({'phoneNo': phoneNo})
                vueElementUiListedJsonItem.update({'applicantName': applicantName})
                vueElementUiListedJsonItem.update({'signatureTimestamp': signatureTimestampList})
                vueElementUiListedJson.append(deepcopy(vueElementUiListedJsonItem))
                signatureTimestampList = list()

            output = vueElementUiListedJson
            total = len(pivot)

            return {'message':
                        {'title': '출석부 조회 성공', 'content': f'교육생 {total}명의 출석부를 성공적으로 조회하였습니다.'},
                    'return':
                        {'items': output, 'total': total}
                    }, 200
    # ---------------------------------------------------------------------------


    # ----------------[ Get attendance list of a specific curriculum ]-----------
    @apiRestful.route('/resource/attendancelogs/listfile')
    @apiRestful.doc(params= {
            'curriculumNo': {'in': 'query', 'description': 'URL parameter, reqired'},
    })
    # Almost same with @apiRestful.route('/resource/attendancelogs/list')
    class get_AttendanceLogs_Listfile(Resource):

        def get(self):
            infoFromClient = request.args
            try:
                curriculumNoFromClient = int(infoFromClient['curriculumNo'])        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
            except KeyError:
                return {'message': {'title': '조회대상 교육과정 오류', 'content': '조회대상 교육과정을 확인하여 주시기 바랍니다.'}}, 400
            
            attendanceLogs = AttendanceLogsModel.query.filter_by(curriculumNo= curriculumNoFromClient)
            # Get full duration of a curriculum.
            curriculumDuration = CurriculumsModel.query.with_entities(CurriculumsModel.startDate, CurriculumsModel.endDate).filter_by(curriculumNo= curriculumNoFromClient).first()
            startDate, endDate = (curriculumDuration.startDate + timedelta(hours= 9)).strftime('%Y-%m-%dT%H:%M:%SZ'), (curriculumDuration.endDate + timedelta(hours= 9)).strftime('%Y-%m-%dT%H:%M:%SZ')
            curriculumDuration = [date.strftime('%Y-%m-%d') for date in pd.date_range(start= startDate, end= endDate, freq= 'B')]
            # Get only attendancePassed members and phoneNo list of a curriculum.
            membersAttendancePassOnlyQuery = MembersModel.query.with_entities(MembersModel.phoneNo).filter_by(curriculumNo= curriculumNoFromClient, attendancePass= 'Y').subquery()
            applicantNameQuery = ApplicantsModel.query.with_entities(ApplicantsModel.phoneNo, ApplicantsModel.applicantName).filter_by(curriculumNo= curriculumNoFromClient).subquery()
            applicantsNameAndphoneNoQuery = db.session.query(membersAttendancePassOnlyQuery).with_entities(
                                                        membersAttendancePassOnlyQuery,
                                                        applicantNameQuery.c.applicantName
                                                    ).outerjoin(applicantNameQuery, membersAttendancePassOnlyQuery.c.phoneNo == applicantNameQuery.c.phoneNo)
            applicantsNameAndphoneNoList = pd.read_sql(applicantsNameAndphoneNoQuery.statement, db.get_engine(bind= 'mysql-simplesmartcheck'), index_col= 'phoneNo')
            membersPhoneNoList = list(applicantsNameAndphoneNoList.index)
            membersNameList = list(applicantsNameAndphoneNoList['applicantName'])
            if len(membersPhoneNoList) != len(set(membersPhoneNoList)):
                return {'message': {'title': '조회대상 교육과정 교육생 중복오류', 'content': f'조회대상 교육과정의 교육생의 중복된 전화번호가 있습니다.'}}, 400

            # Pivot Attendance Check-Table for now.
            attendanceLogsDf = pd.read_sql(attendanceLogs.statement, db.get_engine(bind= 'mysql-simplesmartcheck'))
            attendanceLogsDf['attendanceDate'] = attendanceLogsDf['attendanceDate'].astype(str)
            pivot = attendanceLogsDf.set_index(['phoneNo', 'checkInOut', 'attendanceDate'])[['signature', 'insertedTimestamp']]
            pivot['signatureTimestamp'] = pivot['signature'].apply( lambda x: b64encode(decompress(x)).decode() )
            pivot = pivot.join(applicantsNameAndphoneNoList, on= 'phoneNo')
            pivot = pivot.set_index('applicantName', append= True)
            pivot = pivot.drop(columns= ['signature', 'insertedTimestamp']).unstack(level= [2, 1]).sort_index(axis= 'columns', level= 1)

            # Create Full Attendance Check-Table with Nan values.
            phoneNoAndNameIndex = pd.MultiIndex.from_arrays(
                                        [membersPhoneNoList, membersNameList],
                                        names= ('phoneNo', 'applicantName'),
                                  )
            pivotedColumnsIndex = pd.MultiIndex.from_product(
                                        [['signatureTimestamp'], curriculumDuration, ['In', 'Out']],
                                        names= (None, 'attendanceDate', 'checkInOut')
                                  )
            emptyAttendanceTableDF = pd.DataFrame(
                                        index= phoneNoAndNameIndex,
                                        columns= pivotedColumnsIndex,
                                  )
            # Check attendancePassed members and actually attended applicants who were not attendancePassed.
            attendanceLogsOfapplicantsWithoutAttendnacePass = pivot.index.difference(emptyAttendanceTableDF.index)
            pivot = pivot.drop(attendanceLogsOfapplicantsWithoutAttendnacePass)

            # Overlay and Update the pivot table.
            pivot = pivot.combine_first(emptyAttendanceTableDF)

            # Update Columns to Korean
            pivot.index.names = ('전화번호', '성명')
            pivot.columns.names = (f'과정ID_{curriculumNoFromClient}', '출석일', '입퇴실구분')
            pivot.columns.set_levels(['출석부'], level= 0, inplace= True)
            pivot.columns.set_levels(['입실','퇴실'], level= 2, inplace= True)

            # Convert NaN to None.
            pivot = pivot.where((pd.notnull(pivot)), None)

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
                    worksheet.set_row(rownum, 85)                          # Make Height of rows larger
            
            worksheet.set_column(baseCelly, pivot.columns.size + 1, 25)     # Make Width of Columns after C much larger
            worksheet.set_column(0, baseCelly - 1, 15)                      # Make Width of A:B column larger

            # Insert images to each cell and delete each cell value.
            cells = [(x,y) for x in range(pivot.index.size) for y in range(pivot.columns.size)]

            for rownum, colnum in cells:
                try:
                    signatureImg = BytesIO(b64decode( pivot.iat[rownum, colnum] ))      # Make Image from Base64 String.
                    worksheet.write_string(baseCellx + rownum, baseCelly + colnum, '')
                    worksheet.insert_image(baseCellx + rownum, baseCelly + colnum, 'signatureImg', {'image_data': signatureImg, 'x_scale': 0.48, 'y_scale': 0.48})
                except TypeError:
                    continue

            writer.close()              # the writer has done its job
            output.seek(0)              # go back to the beginning of the stream

            #finally return the file
            return send_file(output, cache_timeout= 0, attachment_filename= f'attendance_ID_{curriculumNoFromClient}.xlsx', as_attachment= True)
    # ---------------------------------------------------------------------------
# -------------------------------------------------------------------------------


# ------------------------[ API to manage Members ]------------------------------
class Members:


    @apiRestful.route('/resource/members')
    class Members(Resource):

        # ----------------[ Update members' Info ]-------------------------------------
        @apiRestful.doc(params= {
                'phoneNo': {'in': 'formData', 'description': 'application/json, body required'},
                'curriculumNo': {'in': 'formData', 'description': 'application/json, body required'},
                'attendancePass': {'in': 'formData', 'description': 'application/json, body required'},
                'attendanceCheck': {'in': 'formData', 'description': 'application/json, body required'},
                'curriculumComplete': {'in': 'formData', 'description': 'application/json, body required'},
                'employment': {'in': 'formData', 'description': 'application/json, body required'},
                # You can add formData columns if needed.
        })
        def put(self):
            # Convert empty string to None
            emptyStringToNone = lambda x: None if x == 'null' else x            
            infoFromClient = {key: emptyStringToNone(request.form[key]) for key in request.form}
            try:
                phoneNoFromClient = infoFromClient['phoneNo']       # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                curriculumNoFromClient = int(infoFromClient['curriculumNo'])
                attendancePassFromClient = infoFromClient['attendancePass']
                attendanceCheckFromClient = infoFromClient['attendanceCheck']
                curriculumCompleteFromClient = infoFromClient['curriculumComplete']
                employmentFromClient = infoFromClient['employment']
            except KeyError:
                return {'message': {'title': '교육생 입력정보 오류', 'content': '업데이트할 교육생 입력정보를 확인하여 주시기 바랍니다.'}}, 400
            
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
                return {'message': {'title': '교육생 정보 업데이트 성공', 'content': '해당 교육생의 정보를 성공적으로 업데이트 하였습니다.'},
                        'return': {
                            'argument': f'{argumentToJson}'
                        }}, 201
            except:
                db.session.rollback()
                return {'message': {'title': '교육생 정보 업데이트 실패', 'content': '해당 교육생의 정보 업데이트에 실패하였습니다.'}}, 500
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
            infoFromClient = {key: loads(request.args[key]) for key in request.args}
            try:
                filterFromClient = infoFromClient['filters']        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                sortParamFromClient = infoFromClient['sort']
                pagenum, limit = int(infoFromClient['pagination']['pagenum']), int(infoFromClient['pagination']['limit'])
            except KeyError:
                return {'message': {'title': '신청자/교육생 조회 기준정보 오류', 'content': '신청자/교육생 조회를 위한 기준정보를 확인하여 주시기 바랍니다.'}}, 400

            ormQueryFilters = createOrmModelQueryFiltersDict(filterFromClient)
            ormQuerySort = createOrmModelQuerySortDict(sortParamFromClient)
            start, stop = (pagenum - 1) * limit, pagenum * limit

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
            
            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql-simplesmartcheck'))
            output = convertDataframeToDictsList(df)

            return {'message':
                        {'title': '출석부 조회 성공', 'content': f'교육생 {total}명의 출석부를 성공적으로 조회하였습니다.'},
                    'return':
                        {'items': output, 'total': total}
                    }, 200
    # -----------------------------------------------------------------------------


    # -----------------------[ Get Members xlsx file ]-----------------------------
    @apiRestful.route('/resource/members/listfile')
    @apiRestful.doc(params= {
            'filters': {'in': 'query', 'description': 'URL parameter, required'},
            'sort': {'in': 'query', 'description': 'URL parameter, required'},
            # You can add query filter columns if needed.
    })
    # Almost same with @apiRestful.route('/resource/members/list')
    class get_Members_Listfile(Resource):

        def get(self):
            infoFromClient = {key: loads(request.args[key]) for key in request.args}
            try:
                filterFromClient = infoFromClient['filters']        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                sortParamFromClient = infoFromClient['sort']
            except KeyError:
                return {'message': {'title': '신청자/교육생 조회 기준정보 오류', 'content': '신청자/교육생 조회를 위한 기준정보를 확인하여 주시기 바랍니다.'}}, 400

            ormQueryFilters = createOrmModelQueryFiltersDict(filterFromClient)
            ormQuerySort = createOrmModelQuerySortDict(sortParamFromClient)

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
            query = sort_query(query, *ormQuerySort)
            
            df = pd.read_sql(query.statement, db.get_engine(bind= 'mysql-simplesmartcheck'))

            # Update Columns to Korean
            df.columns = pd.Index( [Config.COLUMNNAMES_TO_KORNAMES_MAP[x] for x in df.columns] )

            # ---------------------------------------------------------------------
            # Different from @apiRestful.route('/resource/members/list')
            # ---------------------------------------------------------------------
            # create an output stream
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name= 'Sheet1')        # taken from the original question

            writer.close()              # the writer has done its job
            output.seek(0)              # go back to the beginning of the stream`

            #finally return the file
            return send_file(output, cache_timeout= 0, attachment_filename= "members.xlsx", as_attachment= True)
            # ---------------------------------------------------------------------
    # -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


# ------------------------[ API to manage Applicants ]-----------------------------
class Applicants:


    @apiRestful.route('/resource/applicants')
    class Applicants(Resource):

        #-----------------------[ Update Applicant memo ]------------------------------
        @apiRestful.doc(params= {
                'curriculumNo': {'in': 'formData', 'description': 'application/json, body required'},
                'phoneNo': {'in': 'formData', 'description': 'application/json, body/xlsx file required'},
                'operationMemo': {'in': 'formData', 'description': 'application/json, body/xlsx file required'},
                # You can add formData columns if needed.
        })
        def put(self):
            infoFromClient = request.form
            try:
                curriculumNoFromClient = int(infoFromClient['curriculumNo'])        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                phoneNoFromClient = infoFromClient['phoneNo']
                operationMemoFromClient = infoFromClient['operationMemo']
            except KeyError:
                return {'message': {'title': '신청자/교육생 추가정보 입력 오류', 'content': '입력할 신청자/교육생의 전화번호 및 추가정보를 확인하여 주시기 바랍니다.'}}, 400

            requestedBody = {
                "curriculumNo": curriculumNoFromClient,
                "phoneNo": phoneNoFromClient,
                "operationMemo": operationMemoFromClient,
            }
            
            updatedApplicantInfo = ApplicantsModel(**requestedBody)

            try:
                db.session.merge(updatedApplicantInfo)      # session.merge() : A kind of UPSERT, https://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#merging
                db.session.commit()
                applicants = ApplicantsModel.query.filter_by(**requestedBody).one()
                applicantsSchema = ApplicantsModelSchema(many= False)
                argument = applicantsSchema.dump(applicants)
                argumentToJson = dumps(argument)
                return {'message': {'title': '신청자/교육생 추가정보 입력 성공', 'content': '신청자/교육생 추가정보를 성공적으로 입력하였습니다.'},
                        'return': {
                            'argument': f'{argumentToJson}'
                        }}, 201
            except:
                db.session.rollback()
                return {'message': {'title': '신청자/교육생 추가정보 입력 실패', 'content': '신청자/교육생 추가정보 입력에 실패하였습니다.'}}, 500
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
            infoFromClient = request.form
            try:
                curriculumNoFromClient = int(infoFromClient['curriculumNo'])          # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand."), https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
                applicantsBulkFromClient = request.files['applicantsBulkXlsxFile']
            except KeyError:
                return {'message': {'title': '교육과정 신청자 엑셀파일 업로드 오류', 'content': '해당 교육과정 및 엑셀파일 업로드 상태를 확인하여 주시기 바랍니다.'}}, 400

            applicantsDf = pd.read_excel(applicantsBulkFromClient)
            applicantsDf.columns = applicantsDf.columns.map(lambda x: Config.XLSX_COLUMNS_TO_SCHEMA_MAP[ x[:4]+'_'+str(len(x)//19) ])       # Convert column names, Using "x[:4]+'_'+str(len(x)//19)" as a unique key
            applicantsDf['curriculumNo'] = curriculumNoFromClient
            membersDf = applicantsDf[['phoneNo', 'curriculumNo']]

            applicantsDictsList = convertDataframeToDictsList(applicantsDf)
            membersDictsList = convertDataframeToDictsList(membersDf)

            oldBulkApplicants = ApplicantsModel.query.filter_by(curriculumNo= curriculumNoFromClient).all()
            oldBulkMembers = MembersModel.query.filter_by(curriculumNo= curriculumNoFromClient).all()
            oldBulkAttendanceLogs = AttendanceLogsModel.query.filter_by(curriculumNo= curriculumNoFromClient).all()

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
                return {'message': {'title': '교육과정 신청자 엑셀파일 입력/갱신 성공', 'content': '교육과정 신청자 엑셀파일의 내용을 성공적으로 입력/갱신하였습니다.'}}, 201
            except:
                db.session.rollback()
                return {'message': {'title': '교육과정 신청자 엑셀파일 입력/갱신 실패', 'content': '교육과정 신청자 엑셀파일의 내용 입력/갱신에 실패하였습니다.'}}, 500
    # -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------