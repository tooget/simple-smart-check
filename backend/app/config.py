import os


class Config(object):

    # -----------------[ app.config.from_object Parameters in app.__init__.py ]-----------------
    # Pure flask app.config for Flask(__name__)
    # Parameters : http://flask.pocoo.org/docs/1.0/config/
    # If not set fall back to production for safety
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    # flask_sqlalchemy app.config for db.init_app()
    # Set SQLALCHEMY env on your production Environment
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    SQLALCHEMY_BINDS = os.getenv('SQLALCHEMY_BINDS', {  
        'sqlite': 'sqlite:///app.db',
        'mysql': 'mysql+pymysql://kisa:kisakisakisakisa!@rds-simplesmartcheck-mysql8.c4bcyomq603x.ap-northeast-2.rds.amazonaws.com:3306/simplesmartcheck?charset=utf8'
    })
    # flask_jwt_extended app.config for jwt.init_app()
    # Set JWT_SECRET env on your production Environment
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    JWT_BLACKLIST_ENABLED = os.getenv('JWT_BLACKLIST_ENABLED', True)
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS', ['access'])
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.__init__.py ]--------------------------
    # app.Config for cors.init_app()
    CORS_ORIGIN = ['http://0.0.0.0:7000', 'http://localhost:9528']
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.api.__init__.py ]----------------------
    # app.Config for API Blueprint
    API_URI_PREFIX = '/api'
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.api.__init__.py ]----------------------
    # Hash Parameters for app.api.users.py
    SALT_KEYWORD = 'kisa'
    SALT_SIZE = 256/32
    SALT_ROUNDS = 1
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.api.resources.py ]---------------------
    # Mapper of Google Survey Xlsx files to Applicants Table Schema
    # Used in @apiRestful.route('/resource/applicants/bulk')
    # Used in class post_Applicants_Bulk(Resource):
    XLSX_COLUMNS_TO_SCHEMA_MAP = {
        # Using "x[:4]+'_'+str(len(x)//19)" as a unique key. a few len(x) is various within its context.
        # 'unique key': 'table schema'
        '타임스탬_0': 'surveyTimestamp',
        '1. 성_0': 'applicantName',
        '2. 소_0': 'affiliation',                   # len(x)%19 = 0.7
        '3. 부_0': 'department',
        '4. 직_0': 'position',
        '5. 생_1': 'birthDate',
        '6. E_0': 'email',
        '7. 휴_1': 'phoneNo',
        '8. 기_0': 'otherContact',                  # len(x)%19 = 0.8
        '9. 현_1': 'job',
        '10. _1': 'purposeSelection',
        '11. _1': 'competencyForJava',
        '11-1_4': 'competencyForWeb',
        '11-2_4': 'projectExperience',
        '12. _1': 'careerDuration',
        '13. _3': 'purposeDescription',             # len(x)%19 = 0.7
        '14. _2': 'agreeWithFullAttendance',        # len(x)%19 = 0.8
        'Unna_0': 'agreeWithPersonalinfo',          # 'Unnamed' : 15th column name is empty in xlsx
        '16. _2': 'agreeWithMktMailSubscription',
        '17. _4': 'applicationConfirm',
        '18. _2': 'recommender',
        '18. _1': 'howToFindOut',
        '운영메모_0': 'operationMemo'
    }
    # ------------------------------------------------------------------------------------------