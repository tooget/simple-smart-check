from app.config import Config
from flask import Blueprint
from flask_restplus import Api


# -----------------------[ API Blueprint Application ]----------------------------
apiBlueprint = Blueprint('apiBlueprint', 
                            __name__,
                            url_prefix= Config.API_URI_PREFIX
                        )

#Decorator instance in each APIs
apiRestful = Api(apiBlueprint,
                    version= '1.0',
                    title= 'simple-smart-check API',
                    description= 'Backend API for simple-smart-check Project',
                    default= 'app.api.__init__.py',
                    default_label= 'simple-smart-check API LIST',
                    ui= False,  # Make Swagger UI disable
                    doc= False, # Do not use Swagger UI
                )

# API Routing with @apiRestful.route
from app.api.resources import *
from app.api.users import *
# -------------------------------------------------------------------------------