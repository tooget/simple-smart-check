from flask_restplus import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from app.models import UserModel, RevokedTokenModel
from . import apiRestful
from .security import require_auth


# ---------------------------[ SecureResource ]----------------------------------
# Calls require_auth decorator on all requests
class SecureResource(Resource):
    method_decorators = [require_auth]
# -------------------------------------------------------------------------------


# ----------------[ parser : Requested HTTP Body data ]--------------------------
parser = reqparse.RequestParser()
parser.add_argument('username', help= 'username cannot be blank', required= True)
parser.add_argument('password', help= 'password cannot be blank', required= True)
# -------------------------------------------------------------------------------


# ------------------------[ API to Register a New User ]--------------------------
@apiRestful.route('/auth/registration')
@apiRestful.expect(parser)
class UserRegistration(Resource):       # Before applying SecureResource
    def post(self):
        data = parser.parse_args()
        username = data['username']
        
        if UserModel.find_by_username(username):
            return {'message': f'User {username} already exists'}
        
        new_user = UserModel(
            username = username,
            password = UserModel.generate_hash(data['password'])
        )
        
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity= username)
            return {
                'message': f'User {username} was created',
                'access_token': access_token,
            }
        except:
            return {'message': 'Something went wrong'}, 500
# -------------------------------------------------------------------------------


# --------------------[ API to login with access token ]-------------------------
@apiRestful.route('/auth/login')
@apiRestful.expect(parser)
class UserLogin(Resource):      # Before applying SecureResource
    def post(self):
        data = parser.parse_args()
        username = data['username']
        current_user = UserModel.find_by_username(username)

        if not current_user:
            return {'message': f'User {username} doesn\'t exist'}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity= username)
            return {
                'message': f'Logged in as {current_user.username}',
                'access_token': access_token,
            }
        else:
            return {'message': 'Wrong credentials'}
# -------------------------------------------------------------------------------


# -----------------------------[ API to logout ]---------------------------------
@apiRestful.route('/auth/logout/access')
class UserLogoutAccess(Resource):       # Before applying SecureResource
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti= jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
# -------------------------------------------------------------------------------


# --------------------------[ API to Query users ]-------------------------------
@apiRestful.route('/auth/users')
class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()
# -------------------------------------------------------------------------------


# ----------------[ API SAMPLE with Applying SecureResources ]-------------------
@apiRestful.route('/auth/secret')
class SecretResource(SecureResource):
    @jwt_required
    def get(self):
        return {'answer': 42}
# -------------------------------------------------------------------------------