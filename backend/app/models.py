# Circular import issues in flask, Reference 1 : http://flask.pocoo.org/docs/1.0/patterns/packages
# Circular import issues in flask, Reference 2 : https://stackoverflow.com/questions/22929839/circular-import-of-db-reference-using-flask-sqlalchemy-and-blueprints/23400668#23400668
from .extensions import db
from sqlalchemy import text
from passlib.hash import django_pbkdf2_sha256


class UserModel(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'sqlite'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        pbkdf2_sha256 = django_pbkdf2_sha256.using(salt='kisa', salt_size=256/32, rounds=1)
        return pbkdf2_sha256.hash(password)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    __bind_key__ = 'sqlite'

    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


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

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'curriculumNo': x.curriculumNo,
                'curriculumCategory': x.curriculumCategory,
                'ordinalNo': x.ordinalNo,
                'curriculumName': x.curriculumName,
                'curriculumType': x.curriculumType,
                'startDate': str(x.startDate),
                'endDate': str(x.endDate),
                'applicantsInserted': x.applicantsInserted,
                'membersInserted': x.membersInserted,
                'insertedTimestamp': str(x.insertedTimestamp),
                'updatedTimestamp': str(x.updatedTimestamp)
            }
        return {'curriculums': list(map(lambda x: to_json(x), CurriculumsModel.query.all()))}