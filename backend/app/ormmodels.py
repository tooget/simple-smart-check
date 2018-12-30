# Circular import issues in flask, Reference 1 : http://flask.pocoo.org/docs/1.0/patterns/packages
# Circular import issues in flask, Reference 2 : https://stackoverflow.com/questions/22929839/circular-import-of-db-reference-using-flask-sqlalchemy-and-blueprints/23400668#23400668
from app.extensions import db
from sqlalchemy import text


# ----------------[ User Schema for SignUp/Login/Logout/Token ]--------------------------------
class UserModel(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'sqlite'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)

    def add(self):
        db.session.add(self)
        db.session.commit()


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    __bind_key__ = 'sqlite'

    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
# ---------------------------------------------------------------------------------------------


# ----------------[ Curriculums Schema for Managing Attendance Check ]-------------------------
class CurriculumsModel(db.Model):
    __tablename__ = 'curriculums'
    __bind_key__ = 'mysql'

    curriculumNo = db.Column(db.Integer, primary_key= True)
    curriculumCategory = db.Column(db.Text, nullable= False)
    ordinalNo = db.Column(db.Text, nullable= False)
    curriculumName = db.Column(db.Text, nullable= False)
    curriculumType = db.Column(db.Text,  nullable= False)
    startDate = db.Column(db.DateTime, nullable= False)
    endDate = db.Column(db.DateTime, nullable= False)
    applicantsInserted = db.Column(db.Text, nullable= True)
    membersInserted = db.Column(db.Text, nullable= True)
    insertedTimestamp = db.Column(db.TIMESTAMP, nullable= False, server_default= text('CURRENT_TIMESTAMP'))
    updatedTimestamp = db.Column(db.TIMESTAMP, nullable= True, server_default= text('NULL ON UPDATE CURRENT_TIMESTAMP'))

    def add(self):
        db.session.add(self)
        db.session.commit()
# ---------------------------------------------------------------------------------------------