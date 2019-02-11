from app.extensions import db  # Circular import issues in flask, Reference : http://flask.pocoo.org/docs/1.0/patterns/packages, https://stackoverflow.com/questions/22929839/circular-import-of-db-reference-using-flask-sqlalchemy-and-blueprints/23400668#23400668
from sqlalchemy import text


# -------------------[ sqlite: User Schema for SignUp/Login/Logout/Token ]----------------------
class UsersModel(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'mysql-simplesmartcheckusers'

    id = db.Column(db.Integer, nullable= False, primary_key= True)
    username = db.Column(db.String(120), nullable= False, unique= True)
    password = db.Column(db.String(120), nullable= False)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    __bind_key__ = 'mysql-simplesmartcheckusers'

    id = db.Column(db.Integer, nullable= False, primary_key= True)
    jti = db.Column(db.String(120))
# ---------------------------------------------------------------------------------------------


# ------------------------[ mysql: Attendance Management Schema ]------------------------------
# applicants Schema for Inserting/Querying applicants info, especially imported from google survey form.
class ApplicantsModel(db.Model):
    __tablename__ = 'applicants'
    __bind_key__ = 'mysql-simplesmartcheck'

    phoneNo = db.Column(db.String(16), nullable= False, primary_key= True)
    curriculumNo = db.Column(db.Integer, nullable= False, primary_key= True)
    applicantName = db.Column(db.Text, nullable= False)
    affiliation = db.Column(db.Text, nullable= False)
    department = db.Column(db.Text, nullable= False)
    position = db.Column(db.Text, nullable= False)
    birthDate = db.Column(db.Text, nullable= False)
    email = db.Column(db.Text, nullable= False)
    otherContact = db.Column(db.Text, nullable= False)
    job = db.Column(db.Text, nullable= False)
    purposeSelection = db.Column(db.Text, nullable= False)
    competencyForJava = db.Column(db.Text, nullable= False)
    competencyForWeb = db.Column(db.Text, nullable= False)
    projectExperience = db.Column(db.Text, nullable= False)
    careerDuration = db.Column(db.Text, nullable= False)
    purposeDescription = db.Column(db.Text, nullable= False)
    agreeWithFullAttendance = db.Column(db.Text, nullable= False)
    agreeWithPersonalinfo = db.Column(db.Text, nullable= False)
    agreeWithMktMailSubscription = db.Column(db.Text, nullable= False)
    applicationConfirm = db.Column(db.Text, nullable= False)
    recommender = db.Column(db.Text, nullable= True)
    howToFindOut = db.Column(db.Text, nullable= True)
    operationMemo = db.Column(db.Text, nullable= True)
    surveyTimestamp = db.Column(db.Text, nullable= False)
    insertedTimestamp = db.Column(db.TIMESTAMP, nullable= False, server_default= text('CURRENT_TIMESTAMP'))
    updatedTimestamp = db.Column(db.TIMESTAMP, nullable= True, server_default= text('NULL ON UPDATE CURRENT_TIMESTAMP'))


# AttendanceLogs Schema for Inserting/Querying Attendance Logs
class AttendanceLogsModel(db.Model):
    __tablename__ = 'attendanceLogs'
    __bind_key__ = 'mysql-simplesmartcheck'

    phoneNo = db.Column(db.String(16), nullable= False, primary_key= True)
    curriculumNo = db.Column(db.Integer, nullable= False, primary_key= True)
    checkInOut = db.Column(db.String(5), nullable= False, primary_key= True)
    attendanceDate = db.Column(db.Date, nullable= False, primary_key= True)
    signature = db.Column(db.LargeBinary, nullable= False)
    insertedTimestamp = db.Column(db.TIMESTAMP, nullable= False, server_default= text('CURRENT_TIMESTAMP'))
    updatedTimestamp = db.Column(db.TIMESTAMP, nullable= True, server_default= text('NULL ON UPDATE CURRENT_TIMESTAMP'))


# Curriculums Schema for Managing Attendance Check
class CurriculumsModel(db.Model):
    __tablename__ = 'curriculums'
    __bind_key__ = 'mysql-simplesmartcheck'

    curriculumNo = db.Column(db.Integer, nullable= False, primary_key= True)
    curriculumCategory = db.Column(db.Text, nullable= False)
    ordinalNo = db.Column(db.Text, nullable= False)
    curriculumName = db.Column(db.Text, nullable= False)
    curriculumType = db.Column(db.Text,  nullable= False)
    startDate = db.Column(db.Date, nullable= False)
    endDate = db.Column(db.Date, nullable= False)
    applicantsBulkInserted = db.Column(db.TIMESTAMP, nullable= True)
    insertedTimestamp = db.Column(db.TIMESTAMP, nullable= False, server_default= text('CURRENT_TIMESTAMP'))
    updatedTimestamp = db.Column(db.TIMESTAMP, nullable= True, server_default= text('NULL ON UPDATE CURRENT_TIMESTAMP'))


# members Schema for Updating/Querying members(students) info
class MembersModel(db.Model):
    __tablename__ = 'members'
    __bind_key__ = 'mysql-simplesmartcheck'

    phoneNo = db.Column(db.String(16), nullable= False, primary_key= True)
    curriculumNo = db.Column(db.Integer, nullable= False, primary_key= True)
    attendancePass = db.Column(db.Text, nullable= False)
    attendanceCheck = db.Column(db.Text, nullable= False)
    curriculumComplete = db.Column(db.Text, nullable= False)
    employment = db.Column(db.Text, nullable= False)
    insertedTimestamp = db.Column(db.TIMESTAMP, nullable= False, server_default= text('CURRENT_TIMESTAMP'))
    updatedTimestamp = db.Column(db.TIMESTAMP, nullable= True, server_default= text('NULL ON UPDATE CURRENT_TIMESTAMP'))
# ---------------------------------------------------------------------------------------------