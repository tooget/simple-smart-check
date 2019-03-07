from app.api.modules import convertDataframeToDictsList, createOrmModelQueryFiltersDict, createOrmModelQuerySortDict
from app.config import Config
from app.extensions import db
from app.ormmodels import AttendanceLogsModel, ApplicantsModel, CurriculumsModel, MembersModel
from app.schema import ApplicantsObject, CurriculumsObject, MembersObject
from base64 import b64encode, b64decode
from copy import deepcopy
from datetime import datetime, timedelta
from flask import request, send_file
from io import BytesIO
from json import dumps, loads
from PIL import Image, ImageDraw
from sqlalchemy import and_, func
from sqlalchemy_utils import sort_query
from zlib import compress, decompress
import graphene
import pandas as pd


# ------------------------[ API to manage Curriculums ]----------------------------
# ----------------------[ Create a new Curriculums data ]--------------------------
class CreateCurriculumsData(graphene.Mutation):
    class Arguments:
        curriculumName = graphene.String(required= True)
        ordinalNo = graphene.String(required= True)
        curriculumCategory = graphene.String(required= True)
        curriculumType = graphene.String(required= True)
        startDate = graphene.Int(required= True) 
        endDate = graphene.Int(required= True)

    message = graphene.types.json.JSONString()
    result = graphene.Field(lambda: CurriculumsObject)

    def mutate(self, info, curriculumCategory, ordinalNo, curriculumName, curriculumType, startDate, endDate):

        requestedBody = {
            "curriculumName": curriculumName,
            "ordinalNo": ordinalNo,
            "curriculumCategory": curriculumCategory,
            "curriculumType": curriculumType,
            "startDate": datetime.fromtimestamp(startDate).strftime('%Y-%m-%d'),
            "endDate": datetime.fromtimestamp(endDate).strftime('%Y-%m-%d'),
        }
        
        CurriculumsData = CurriculumsModel(**requestedBody)
        
        try:
            db.session.add(CurriculumsData)
            db.session.commit()
            return CreateCurriculumsData(
                message= {'title': '신규 교육과정 입력 성공', 'content': '새로운 교육과정 데이터가 입력되었습니다.'},
                result= CurriculumsData,
            )
        except:
            db.session.rollback()
            raise Exception(dumps({'title': '신규 교육과정 입력 실패', 'content': '새로운 교육과정 데이터 입력에 실패하였습니다.'}))
# ---------------------------------------------------------------------------------


# ------------------------[ Update a Curriculums data ]----------------------------
class UpdateCurriculumsData(graphene.Mutation):
    class Arguments:
        curriculumNo = graphene.Int(required= True) 
        curriculumCategory = graphene.String(required= True)
        ordinalNo = graphene.String(required= True)
        curriculumName = graphene.String(required= True)
        curriculumType = graphene.String(required= True)
        startDate = graphene.Int(required= True) 
        endDate = graphene.Int(required= True)

    message = graphene.types.json.JSONString()
    put = graphene.Field(lambda: CurriculumsObject)

    def mutate(self, info, curriculumNo, curriculumCategory, ordinalNo, curriculumName, curriculumType, startDate, endDate):

        requestedBody = {
            "curriculumNo": curriculumNo,
            "curriculumCategory": curriculumCategory,
            "ordinalNo": ordinalNo,
            "curriculumName": curriculumName,
            "curriculumType": curriculumType,
            "startDate": datetime.fromtimestamp(startDate).strftime('%Y-%m-%d'),
            "endDate": datetime.fromtimestamp(endDate).strftime('%Y-%m-%d'),
        }
        
        CurriculumsData = CurriculumsModel(**requestedBody)
        
        try:
            db.session.merge(CurriculumsData)
            db.session.commit()
            return UpdateCurriculumsData(
                message= {'title': '교육과정 업데이트 성공', 'content': '교육과정 정보가 업데이트 되었습니다.'},
                put= CurriculumsData,
            )
        except:
            db.session.rollback()
            raise Exception(dumps({'title': '교육과정 업데이트 실패', 'content': '교육과정 정보가 업데이트에 실패하였습니다.'}))
# ---------------------------------------------------------------------------------