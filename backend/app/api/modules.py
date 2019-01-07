from flask import request
from flask_restplus import abort
from functools import wraps
from json import loads

# Secure method decorator
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

def convertDataframeToListedJson(dataframe):
    # to_json() Issue 1 : date_format, TypeError: Object of type DataFrame is not JSON serializable
    # to_json() Issue 2 : force_ascii issue(unicode problem when True)
    # to_json() Issue 3 : return type is always string representation of list, json.loads(), https://stackoverflow.com/questions/1894269/convert-string-representation-of-list-to-list
    df_recordslist = dataframe.to_json(orient= 'records', date_format= 'iso', force_ascii= False)
    json_recordslist = loads(df_recordslist)
    return json_recordslist