from app.api import apiBlueprint
from app.config import Config
from app.extensions import db, ma, jwt, cors
from app.ormmodels import RevokedTokenModel
from flask import Flask


# -------------------[ Flask App Settings ]----------------------------------
# Create Flask app
def create_app():
    app = Flask(__name__)
    # Set app.config from app.config.py
    app.config.from_object(Config)
    # Register modules to URL with Blueprint : Working as an API Router.
    app.register_blueprint(apiBlueprint)
    return app

# Register Flask app extensions
def register_extentions(app):
    # Initailize db connection from app.extensions.py
    db.init_app(app)
    # Initailize ma session from app.extensions.py
    ma.init_app(app)
    # Initailize cors session from app.extensions.py
    cors.init_app(app, origins= Config.CORS_ORIGIN)
    # Initailize jwt session from app.extensions.py
    jwt.init_app(app)
# ---------------------------------------------------------------------------


# -------------------[ Flask App Instance Start ]----------------------------
app = create_app()
register_extentions(app)
# ---------------------------------------------------------------------------


# -----[ Execute with specific condition after Flask App starts. ]-----------
# Create DB tables defined in models.py when DB has no scheam/a query is called at the first time.
@app.before_first_request
def create_tables():
    for key in Config.SQLALCHEMY_BINDS.keys():
        db.create_all(bind= key)

@app.teardown_appcontext
def shutdown_session(exception= None):
    db.session.remove()

# Block api request with blacklisted access token
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    blacklisted = RevokedTokenModel.query.filter_by(jti= jti).first()
    return bool(blacklisted)

@apiBlueprint.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origins'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response
# ---------------------------------------------------------------------------