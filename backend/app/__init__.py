from flask import Flask
from .config import Config
from .extensions import db, jwt, cors
from .api import api_bp

def register_extensions(app):
    db.init_app(app)
    cors.init_app(app, origins=Config.CORS_ORIGIN)
    jwt.init_app(app)

def create_app():
    # Create Flask app + CORS + app.config
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    return app

# Flask App Instance Start.
app = create_app()
# Register modules to URL with Blueprint
app.register_blueprint(api_bp)


# Execute when this condition meets.
@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    from .models import RevokedTokenModel
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)