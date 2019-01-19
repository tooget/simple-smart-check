import app.ormmodels
import inspect
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
    request_args_filters_columns = set(request_args_filters.keys())     # make list to delete dict's items
    queryFiltersByEachOrmModel = dict()
    totalOrmModelTableColumns = set()
    
    for ormClassName, ormModel in inspect.getmembers(app.ormmodels, inspect.isclass):
        if type(ormModel).__module__ == 'flask_sqlalchemy.model' and ormModel.__bind_key__ == 'mysql':
            ormModelTableColumns = set(ormModel.__table__.columns.keys())
            totalOrmModelTableColumns = totalOrmModelTableColumns | ormModelTableColumns
            columnIntersections = request_args_filters_columns & ormModelTableColumns       # when a column from client exists
            queryFiltersByEachOrmModel[ormClassName] = {column: request_args_filters[column] for column in columnIntersections}       # return empty dictionary if there no column inspected in a certain orm model 

    columnDifference = request_args_filters_columns - totalOrmModelTableColumns     # checking when columns are not used
    if bool(columnDifference) == True:      # If unknown columns remain
        raise KeyError(f'app.ormmodels.py does not have columns : {columnDifference}')

    return queryFiltersByEachOrmModel       # return dict


def createOrmModelQuerySortDict(request_args_sort):
    # Making filter dictionary
    # {'ORM Schema Table1': {'column1': value, 'column2': value}, 'ORM Scheam Table2': {'column1': value, 'column2': value}}
    sortQueryDirection = {'desc': '-', 'asc': '+'}
    querySortByOrmModel = [''.join([sortQueryDirection[value], target]) for target, value in request_args_sort.items()]

    return querySortByOrmModel       # return dict
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