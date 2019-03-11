import time
import json
from functools import reduce
import os
JSON_FILE_PATH = os.getcwd() + '/export.json'
print(JSON_FILE_PATH)

# class SceptreJsonOutput0(object):

#     def __init__(self, JSON_FILE_PATH):
#         self.json_load = json.loads(open(JSON_FILE_PATH).read())
#         self.parsedOutput = {}
#         self._parsingListedJson(self.json_load)
    
#     def _parsingListedJson(self, TARGET_JSON_LOADED):
#         typeOfJsonLoaded = type(TARGET_JSON_LOADED)
#         if typeOfJsonLoaded != dict:
#             for item in TARGET_JSON_LOADED:
#                 self._parsingListedJson(item)
#         elif typeOfJsonLoaded == dict:
#             if set(TARGET_JSON_LOADED.keys()) == {'OutputKey', 'OutputValue'}:
#                 self.parsedOutput[TARGET_JSON_LOADED['OutputKey']] = TARGET_JSON_LOADED['OutputValue']
#             else:
#                 self._parsingListedJson(TARGET_JSON_LOADED.values())


# class SceptreJsonOutput1(object):

#     def __init__(self, JSON_FILE_PATH):
#         self.json_load = json.loads(open(JSON_FILE_PATH).read())
#         self.parsedOutput = {}
#         self._parsingListedJson(self.json_load)

#     def _parsingListedJson(self, TARGET_JSON_LOADED):
#         for element in TARGET_JSON_LOADED:
#             for value in element.values():
#                 if value:
#                     reform = {item['OutputKey']:item['OutputValue'] for item in value}
#                     self.parsedOutput.update(reform)


class SceptreJsonOutput2(object):

    def __init__(self, JSON_FILE_PATH):
        self.json_load = json.loads(open(JSON_FILE_PATH).read())
        self.parsedOutput = {}
        self._parsingListedJson(self.json_load)

    def _parsingListedJson(self, TARGET_JSON_LOADED):
        temp = {}
        for element in TARGET_JSON_LOADED:
            temp.update(element)
        
        # array = reduce(lambda x, y: x + y, (value for value in temp.values() if value))
        array = reduce(lambda x, y: x + y, filter(lambda x: x is not [], (value for value in temp.values())))
        self.parsedOutput = {value['OutputKey']:value['OutputValue'] for value in array}


re2 = SceptreJsonOutput2(JSON_FILE_PATH)

from pprint import pprint
print(pprint(re2.parsedOutput))

with open('export_keyvalue.json', 'w') as f:
    json.dump(re2.parsedOutput, f)

# start2 = time.time()
# for i in range(0, 10):
#     re2 = SceptreJsonOutput2(JSON_FILE_PATH)
# end2 = time.time()
# print('re2', end2 - start2)

# start1 = time.time()
# for i in range(0, 10):
#     re1 = SceptreJsonOutput1(JSON_FILE_PATH)
# end1 = time.time()
# print('re1', end1 - start1)

# start0 = time.time()
# for i in range(0, 10):
#     re0 = SceptreJsonOutput0(JSON_FILE_PATH)
# end0 = time.time()
# print('re0', end0 - start0)

# print(re1.parsedOutput == re2.parsedOutput)