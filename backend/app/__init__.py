from app.config import Config
from app.extensions import db, jwt, cors
from app.ormmodels import RevokedTokenModel
from app.schema import schema
from flask import Flask
from flask_graphql import GraphQLView


# -------------------[ Flask App Settings ]----------------------------------
# Create Flask app
def create_app():
    app = Flask(__name__)
    # Set app.config from app.config.py
    app.config.from_object(Config)
    # Register modules to URL with Blueprint : Working as an API Router.
    # app.register_blueprint(apiBlueprint)
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True # for having the GraphiQL interface
        )
    )
    return app

# Register Flask app extensions
def register_extentions(app):
    # Initailize db connection from app.extensions.py
    db.init_app(app)
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

# Block api request with blacklisted access token
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    blacklisted = RevokedTokenModel.query.filter_by(jti= jti).first()
    return bool(blacklisted)

# @apiBlueprint.after_request
# def add_header(response):
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
#     return response
# ---------------------------------------------------------------------------