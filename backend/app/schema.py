from app.config import Config
from app.ormmodels import UsersModel, RevokedTokenModel
from app.ormmodels import ApplicantsModel, AttendanceLogsModel, CurriculumsModel, MembersModel
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy_utils import sort_query


# ---------------[ ObjectType & Connection Management for Schema in Graph ]--------------------
# ---------------------------------------------------------------------------------
class UsersObject(SQLAlchemyObjectType):
    class Meta:
        model = UsersModel
        interfaces = (relay.Node, )

class UsersConnection(relay.Connection):
    class Meta:
        node = UsersObject
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
class RevokedTokenObject(SQLAlchemyObjectType):
    class Meta:
        model = RevokedTokenModel
        interfaces = (relay.Node, )

class RevokedTokenConnection(relay.Connection):
    class Meta:
        node = RevokedTokenObject
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
class ApplicantsObject(SQLAlchemyObjectType):
    class Meta:
        model = ApplicantsModel
        interfaces = (relay.Node, )

class ApplicantsConnection(relay.Connection):
    class Meta:
        node = ApplicantsObject
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# class AttendanceLogsObject(SQLAlchemyObjectType):
#     class Meta:
#         model = AttendanceLogsModel
#         interfaces = (relay.Node, )

# class AttendanceLogsCon(relay.Connection):
#     class Meta:
#         node = AttendanceLogsObject
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
class CurriculumsObject(SQLAlchemyObjectType):
    class Meta:
        model = CurriculumsModel
        interfaces = (relay.Node, )

class CurriculumnsConnection(relay.Connection):
    class Meta:
        node = CurriculumsObject

    message = graphene.types.json.JSONString()
    totalCount = graphene.Int()

    @staticmethod
    def resolve_message(self, info):
        return {'title': '교육과정 목록조회 성공', 'content': f'{self.length}건의 교육과정을 성공적으로 조회하였습니다.'}

    @staticmethod
    def resolve_totalCount(self, info):
        return self.length

class CurriculumsConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ['first', 'last', 'before', 'after', 'sort', 'order']

    @classmethod
    def get_query(cls, model, info, sort, **args):
        query = super(CurriculumsConnectionField, cls).get_query(model, info, **args)
        for field, value in args.items():
            if field not in cls.RELAY_ARGS:
                query = query.filter(getattr(model, field).like(f'%{value}%'))
        
        # Applies an sql ORDER BY for given query.
        field, sort = args.get('order').split('_')
        query = query.order_by(getattr(getattr(model, field), sort)())
        return query
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
class MembersObject(SQLAlchemyObjectType):
    class Meta:
        model = MembersModel
        interfaces = (relay.Node, )

class MembersConnection(relay.Connection):
    class Meta:
        node = MembersObject
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
