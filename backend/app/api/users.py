from app.config import Config
from app.extensions import db
from app.ormmodels import UsersModel, RevokedTokenModel
from app.schema import UsersObject, RevokedTokenObject
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
import graphene
from graphql import GraphQLError
from passlib.hash import django_pbkdf2_sha256


# --------------------[ API to System Users/Admin and Auth ]-----------------------
# ---------------------------[ Register a New User ]-------------------------------
class CreateNewUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required= True)
        password = graphene.String(required= True)

    message = graphene.String()
    accessToken = graphene.String()
    post = graphene.Field(lambda: UsersObject)

    def mutate(self, info, username, password):

        if UsersModel.query.filter_by(username= username).first():
            raise Exception(f'User {username} already exists')

        pbkdf2_sha256 = django_pbkdf2_sha256.using(salt= Config.SALT_KEYWORD, salt_size= Config.SALT_SIZE, rounds= Config.SALT_ROUNDS)
        newUserInfoFromClient = UsersModel(
            username= username,
            password= pbkdf2_sha256.hash(password)    # Crypt the password with pbkdf2
        )
        
        try:
            db.session.add(newUserInfoFromClient)
            # [!] New Token Issue when DB insert fails
            accessToken = create_access_token(identity= password)
            db.session.commit()
            return CreateNewUser(
                message= f'User {username} was created',
                accessToken= accessToken,
                post= newUserInfoFromClient,
            )
        except:
            db.session.rollback()
            raise Exception('Something went wrong')
# ---------------------------------------------------------------------------------


# ----------------------------------[ Login ]--------------------------------------
class UsersLogin(graphene.Mutation):
    class Arguments:
        username = graphene.String(required= True)
        password = graphene.String(required= True)

    message = graphene.String()
    result = graphene.types.json.JSONString()

    def mutate(self, info, username, password):

        UserInfoFromDB = UsersModel.query.filter_by(username= username).first()

        if not UserInfoFromDB:                                          # if User is not registered, return 500
            raise Exception(f'User {username} doesn\'t exist')
        elif password == UserInfoFromDB.password.split('$')[-1]:        # Successfully Login, return 201
            accessToken = create_access_token(identity= password)
            return UsersLogin(
                message= f'Logged in as {UserInfoFromDB.username}',
                result= {
                    "accessToken": accessToken,
                    "username": UserInfoFromDB.username,
                }
            )
        else:                                                           # Something wrong, return 500
            raise Exception('Wrong credentials')
# ---------------------------------------------------------------------------------


# ----------------------------------[ Logout ]-------------------------------------
class UsersLogout(graphene.Mutation):

    message = graphene.String()

    @jwt_required
    def mutate(self, info):
        jti = get_raw_jwt()['jti']
        try:
            db.session.add(RevokedTokenModel(jti= jti))
            db.session.commit()
            return UsersLogout(
                message= 'Successfully Logout, Access token has been revoked',
            )
        except:
            db.session.rollback()
            raise Exception('Something went wrong')
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
