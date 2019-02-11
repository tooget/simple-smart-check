import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType, utils
from app.ormmodels import UsersModel, RevokedTokenModel
from app.ormmodels import ApplicantsModel, AttendanceLogsModel, CurriculumsModel, MembersModel

class Users(SQLAlchemyObjectType):
    class Meta:
        model = UsersModel
        interfaces = (relay.Node, )

class UsersCon(relay.Connection):
    class Meta:
        node = Users

class RevokedToken(SQLAlchemyObjectType):
    class Meta:
        model = RevokedTokenModel
        interfaces = (relay.Node, )

class RevokedTokenCon(relay.Connection):
    class Meta:
        node = RevokedToken

class Applicants(SQLAlchemyObjectType):
    class Meta:
        model = ApplicantsModel
        interfaces = (relay.Node, )

class ApplicantsCon(relay.Connection):
    class Meta:
        node = Applicants

# class AttendanceLogs(SQLAlchemyObjectType):
#     class Meta:
#         model = AttendanceLogsModel
#         interfaces = (relay.Node, )

# class AttendanceLogsCon(relay.Connection):
#     class Meta:
#         node = AttendanceLogs

class Curriculums(SQLAlchemyObjectType):
    class Meta:
        model = CurriculumsModel
        interfaces = (relay.Node, )

class CurriculumsCon(relay.Connection):
    class Meta:
        node = Curriculums

class Members(SQLAlchemyObjectType):
    class Meta:
        model = MembersModel
        interfaces = (relay.Node, )

class MembersCon(relay.Connection):
    class Meta:
        node = Members


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    allUsers = SQLAlchemyConnectionField(UsersCon)
    # Allows sorting over multiple columns, by default over the primary key
    allRevokedToken = SQLAlchemyConnectionField(RevokedTokenCon)
    # Allows sorting over multiple columns, by default over the primary key
    allApplicants = SQLAlchemyConnectionField(ApplicantsCon)
    # Allows sorting over multiple columns, by default over the primary key
    # all_AttendanceLogs = SQLAlchemyConnectionField(AttendanceLogsCon)
    # Allows sorting over multiple columns, by default over the primary key
    allCurriculums = SQLAlchemyConnectionField(CurriculumsCon)
    # Allows sorting over multiple columns, by default over the primary key
    allMembers = SQLAlchemyConnectionField(MembersCon)

schema = graphene.Schema(query=Query)