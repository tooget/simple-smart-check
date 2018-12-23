from flask import Flask
from .api import api_bp
from .config import Config
from .models import RevokedTokenModel
from .extensions import db, jwt, cors


# -------------------[ Flask App Settings ]----------------------------------
# Initailize db connection/cors session/jwt session from app.extensions
def register_extensions(app):
    db.init_app(app)
    cors.init_app(app, origins=Config.CORS_ORIGIN)
    jwt.init_app(app)

# Create Flask app + CORS + app.config
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    return app
# ---------------------------------------------------------------------------


# -------------------[ Flask App Instance Start ]----------------------------
app = create_app()
# Register modules to URL with Blueprint : Working as an API Router.
app.register_blueprint(api_bp)
# ---------------------------------------------------------------------------



# -----[ Execute with specific condition after Flask App starts. ]-----------
# Create db tables when DB has no scheam/DB call is called at the first time.
@app.before_first_request
def create_tables():
    db.create_all()

# Block api request with blacklisted access token
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)
# ---------------------------------------------------------------------------