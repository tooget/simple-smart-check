from app.api import apiRestful
from app.api.security import require_auth
from app.config import Config
from app.ormmodels import UserModel, RevokedTokenModel
from datetime import timedelta
from flask import request
from flask_restplus import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from passlib.hash import django_pbkdf2_sha256


# # ---------------------------[ SecureResource ]----------------------------------
# # Calls require_auth decorator on all requests
# class SecureResource(Resource):
#     method_decorators = [require_auth]
# # -------------------------------------------------------------------------------


# --------------------------[ Register a New User ]------------------------------
@apiRestful.route('/auth/registration')
@apiRestful.doc(params= {
                    'username': 'required',
                    'password': 'reuqried',
                })
class UserRegistration(Resource):       # Before applying SecureResource

    def post(self):
        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
        # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
        usernameFromClient = request.form['username']
        passwordFromClient = request.form['password']
        
        if UserModel.query.filter_by(username= usernameFromClient).first():
            return {
                'message': f'User {usernameFromClient} already exists'
            }
        
        pbkdf2_sha256 = django_pbkdf2_sha256.using(salt= Config.SALT_KEYWORD, salt_size= Config.SALT_SIZE, rounds= Config.SALT_ROUNDS)
        newUserInfoFromClient = UserModel(
            username= usernameFromClient,
            password= pbkdf2_sha256.hash(passwordFromClient)    #Crypt the password with pbkdf2
        )

        # [!] Transaction Issue when DB insert fails
        try:
            UserModel.add(newUserInfoFromClient)
            accessToken = create_access_token(identity= usernameFromClient)
            return {
                'message': f'User {usernameFromClient} was created',
                'access_token': accessToken,
            }
        except:
            return {
                'message': 'Something went wrong'
            }, 500
# -------------------------------------------------------------------------------


# ---------------------------------[ LOGIN ]-------------------------------------
@apiRestful.route('/auth/login')
@apiRestful.doc(params= {
                    'username': 'required',
                    'password': 'reuqried',
                })
class UserLogin(Resource):      # Before applying SecureResource
    def post(self):
        # if key doesn't exist, returns a 400, bad request error("message": "The browser (or proxy) sent a request that this server could not understand.")
        # Reference : https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
        usernameFromClient = request.form['username']
        passwordFromClient = request.form['password']
        UserInfoFromDB = UserModel.query.filter_by(username= usernameFromClient).first()

        # if UserInfoFromDB doesn't exist, return 500
        if not UserInfoFromDB:
            return {
                'message': f'User {usernameFromClient} doesn\'t exist'
            }, 500
        # Successfully Login, return 201
        elif passwordFromClient == UserInfoFromDB.password.split('$')[-1]:
            accessToken = create_access_token(identity= usernameFromClient)
            return {
                'message': f'Logged in as {UserInfoFromDB.username}',
                'access_token': accessToken,
            }, 201
        # Something wrong, return 500
        else:
            return {
                'message': 'Wrong credentials'
            }, 500
# -------------------------------------------------------------------------------


# ---------------------------------[ LOGOUT ]------------------------------------
@apiRestful.route('/auth/logout')
class UserLogout(Resource):       # Before applying SecureResource
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revokedToken = RevokedTokenModel(jti= jti)
            revokedToken.add()
            return {
                'message': 'Access token has been revoked'
            }
        except:
            return {
                'message': 'Something went wrong'
            }, 500
# -------------------------------------------------------------------------------


# ------------------------------[ Get All Users ]--------------------------------
@apiRestful.route('/auth/users/all')
class AllUsers(Resource):       # Before applying SecureResource
    def get(self):
        def to_json(x= UserModel):
            return {
                'id': x.id,
                'username': x.username,
                'password': x.password
            }
        return {
            'users': list(map(lambda x: to_json(x), UserModel.query.all()))
        }
# -------------------------------------------------------------------------------


# # ----------------[ API SAMPLE with Applying SecureResources ]-------------------
# @apiRestful.route('/auth/secret')
# class SecretResource(SecureResource):
#     @jwt_required
#     def get(self):
#         return {
#             'answer': 42
#         }
# # -------------------------------------------------------------------------------