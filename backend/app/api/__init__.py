from app.api.resources.graphql import *
from app.api.users import *
from app.config import Config
from app.schema import UsersConnection, RevokedTokenConnection
from app.schema import ApplicantsConnection, CurriculumnsConnection, MembersConnection
from app.schema import CurriculumsConnectionField
from flask import Blueprint
from flask_restplus import Api
from flask_graphql import GraphQLView
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField


# -------------------[ Manange Query & Mutation in GraphQL ]-----------------------
class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    allUsers = SQLAlchemyConnectionField(UsersConnection)
    # Allows sorting over multiple columns, by default over the primary key
    allRevokedToken = SQLAlchemyConnectionField(RevokedTokenConnection)
    # Allows sorting over multiple columns, by default over the primary key
    allApplicants = SQLAlchemyConnectionField(ApplicantsConnection)
    # Allows sorting over multiple columns, by default over the primary key
    # all_AttendanceLogs = SQLAlchemyConnectionField(AttendanceLogsConnection)
    # Allows sorting over multiple columns, by default over the primary key
    allCurriculums = CurriculumsConnectionField(
        CurriculumnsConnection,
        order= graphene.String(),
        curriculumName= graphene.String(),
        curriculumCategory= graphene.String(),
    )
    # Allows sorting over multiple columns, by default over the primary key
    allMembers = SQLAlchemyConnectionField(MembersConnection)


class Mutation(graphene.ObjectType):
    createNewUser = CreateNewUser.Field()
    usersLogin = UsersLogin.Field()
    usersLogout = UsersLogout.Field()

    createCurriculumsData = CreateCurriculumsData.Field()
    updateCurriculumsData = UpdateCurriculumsData.Field()

schema = graphene.Schema(query= Query, mutation= Mutation)
# ---------------------------------------------------------------------------------


# -----------------------[ API Blueprint Application ]----------------------------
apiBlueprint = Blueprint('apiBlueprint', 
                            __name__,
                            url_prefix= Config.API_URI_PREFIX
                        )

# Decorator instance in each APIs
apiRestful = Api(apiBlueprint,
                    version= '1.0',
                    title= 'simple-smart-check API',
                    description= 'Backend API for simple-smart-check Project',
                    default= 'app.api.__init__.py',
                    default_label= 'simple-smart-check API LIST',
                    # ui= False,  # False: Make Swagger UI disable
                    # doc= False, # False: Do not use Swagger UI
                )

# API Routing with @apiRestful.route in app.api.resources.RESTful
from app.api.resources.RESTful import *

# API Routing with @apiRestful.route in app.api.resources.graphql
# ADD batch query support (used in Apollo-Client)
apiBlueprint.add_url_rule('/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema= schema,
        batch= True,
        graphiql= True, # DEFAULT: False, Do not use GraphiQL UI
    )
)
# -------------------------------------------------------------------------------