from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# ----[ Going to be initialized when app.__init__.register_extensions() is executed. ] ----
# Connect to DB with flask_sqlalchemy
db = SQLAlchemy()
 
# Create authentificated session with JWT
jwt = JWTManager()

# Create CORS session from origin URL
cors = CORS()
# -----------------------------------------------------------------------------------------