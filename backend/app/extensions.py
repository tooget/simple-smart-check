# Connect to DB with flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Create authentificated session with JWT 
from flask_jwt_extended import JWTManager
jwt = JWTManager()

# Set CORS URL origin
from flask_cors import CORS
cors = CORS()