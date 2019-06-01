import os


class Config(object):

    # -----------------[ app.config.from_object Parameters in app.__init__.py ]-----------------
    # Pure flask app.config for Flask(__name__)
    # Parameters : http://flask.pocoo.org/docs/1.0/config/
    # If not set fall back to production for safety
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')
    # Set Flaks Return type as a Unicode, not ASCII
    JSON_AS_ASCII = False

    # flask_sqlalchemy app.config for db.init_app()
    # Set SQLALCHEMY env on your production Environment
    SQLALCHEMY_COMMIT_ON_TEARDOWN = os.getenv('SQLALCHEMY_COMMIT_ON_TEARDOWN', False)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    SQLALCHEMY_BINDS = os.getenv('SQLALCHEMY_BINDS', {
        'mysql-simplesmartcheckusers': 'mysql+pymysql://{RDS_USERNAME}:{RDS_USERPASSWORD}@{RDS_ENDPOINT_URL}:3306/simplesmartcheckusers?charset=utf8mb4'.format(
            RDS_ENDPOINT_URL= os.getenv('RDS_ENDPOINT_URL', '127.0.0.1'),
            RDS_USERNAME= os.getenv('RDS_USERNAME', 'root'),
            RDS_USERPASSWORD= os.getenv('RDS_USERPASSWORD', '1qaz'),
        ),
        'mysql-simplesmartcheck': 'mysql+pymysql://{RDS_USERNAME}:{RDS_USERPASSWORD}@{RDS_ENDPOINT_URL}:3306/simplesmartcheck?charset=utf8mb4&binary_prefix=true'.format(
            RDS_ENDPOINT_URL= os.getenv('RDS_ENDPOINT_URL', '127.0.0.1'),
            RDS_USERNAME= os.getenv('RDS_USERNAME', 'root'),
            RDS_USERPASSWORD= os.getenv('RDS_USERPASSWORD', '1qaz'),
        ),
    })
    # flask_jwt_extended app.config for jwt.init_app()
    # Set JWT_SECRET env on your production Environment
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    JWT_BLACKLIST_ENABLED = os.getenv('JWT_BLACKLIST_ENABLED', True)
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS', ['access'])
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.__init__.py ]--------------------------
    # app.Config for cors.init_app()
    CORS_ORIGIN = [
        'http://127.0.0.1:7000', 'http://localhost:7000', 'https://www.smartcheck.ml/*',
        'http://127.0.0.1:9528/*', 'http://localhost:9528', 'https://admin.smartcheck.ml/*'
    ]
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.api.__init__.py ]----------------------
    # app.Config for API Blueprint
    API_URI_PREFIX = '/api'
    # ------------------------------------------------------------------------------------------


    # ------------------------[ Custom Parameters in app.api.__init__.py ]----------------------
    # Hash Parameters for app.api.users.py
    SALT_KEYWORD = 'AnyKey'
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

    COLUMNNAMES_TO_KORNAMES_MAP = {
        'phoneNo': '전화번호',
        'curriculumNo': '과정ID',
        'attendancePass': '선발여부',
        'attendanceCheck': '참석여부',
        'curriculumComplete': '수료여부',
        'employment': '취업여부',
        'ordinalNo': '기수',
        'curriculumName': '과정명',
        'curriculumCategory': '과정분류',
        'startDate': '시작일',
        'endDate': '종료일',
        'applicantName': '지원자명',
        'birthDate': '생년월일',
        'email': '이메일',
        'affiliation': '소속(회사/학교)',
        'department': '부서(전공)',
        'position': '직급(학년)',
        'job': '지원자 상태',
        'purposeSelection': '수강목적',
        'careerDuration': '개발경력(기간)',
        'agreeWithPersonalinfo': '개인정보 제공동의',
        'agreeWithMktMailSubscription': '핀테크 기술지원센터 소식 수신여부',
        'operationMemo': '비고'
    }
    # ------------------------------------------------------------------------------------------