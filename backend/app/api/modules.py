import app.ormmodels
import inspect
import importlib
from json import loads
from flask import request
from flask_restplus import abort
from functools import wraps


# --------------------------[ Data Control in API ]------------------------------
def convertDataframeToDictsList(dataframe):
    # to_json() Issue 1 : date_format, TypeError: Object of type DataFrame is not JSON serializable
    # to_json() Issue 2 : force_ascii issue(unicode problem when True)
    # to_json() Issue 3 : return type is always string representation of list, json.loads(), https://stackoverflow.com/questions/1894269/convert-string-representation-of-list-to-list
    listedDictsStr = dataframe.to_json(orient= 'records', date_format= 'iso', force_ascii= False)
    listedDicts = loads(listedDictsStr)
    return listedDicts        # return list


def createOrmModelQueryFiltersDict(request_args_filters):
    # Making filter dictionary
    # {'ORM Schema Table1': {'column1': value, 'column2': value}, 'ORM Scheam Table2': {'column1': value, 'column2': value}}
    ormClassNames = [m[0] for m in inspect.getmembers(app.ormmodels, inspect.isclass) if m[1].__module__ == 'app.ormmodels']
    queryFiltersByEachOrmModel = {ormClassName: {} for ormClassName in ormClassNames}

    for column, value in list(request_args_filters.items()):    # make list to delete dict's items

        columnIsInOrmModel = False
        for ormClassName in ormClassNames:
            ormModelClasses = importlib.import_module('app.ormmodels')
            ormModel = getattr(ormModelClasses, ormClassName)
            if hasattr(ormModel, column):
                queryFiltersByEachOrmModel[ormClassName][column] = value    # hasattr : https://wikidocs.net/13945, operator.methodcaller : https://docs.python.org/3/library/operator.html#operator.methodcaller
                columnIsInOrmModel = True                                   # checking when columns are used
        
        if columnIsInOrmModel:
            del request_args_filters[column]

    if bool(request_args_filters) == True:     # If unknown columns remain
        raise KeyError(f'app.ormmodels.py does not have columns : {request_args_filters}')

    return queryFiltersByEachOrmModel       # return dict
# -------------------------------------------------------------------------------


# ------------------------------[ Secure ]---------------------------------------
# 'class SecureResource(Resource):' in 'app.api.resources.py', 'app.api.users.py'
def requireAuth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify if User is Authenticated
        # Authentication logic goes here
        if request.headers.get('authorization'):
            return func(*args, **kwargs)
        else:
            return abort(401)
    return wrapper
# -------------------------------------------------------------------------------