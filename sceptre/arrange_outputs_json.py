import json
from functools import reduce
import os
import yaml

class SceptreJsonOutput(object):

    def __init__(self, JSON_FILE_PATH, CONFIG_FILE_PATH):
        self.json_load = json.loads(open(JSON_FILE_PATH).read())
        self.config_load = yaml.load(open(CONFIG_FILE_PATH).read())
        self.parsedOutput = {}
        self._parsingListedJson(self.json_load)
        self.parsedOutput = dict(self.config_load, **self.parsedOutput)

    def _parsingListedJson(self, TARGET_JSON_LOADED):
        temp = {}
        for element in TARGET_JSON_LOADED:
            temp.update(element)        
        array = reduce(lambda x, y: x + y, filter(lambda x: x is not [], (value for value in temp.values())))
        self.parsedOutput = {value['OutputKey']:value['OutputValue'] for value in array}

JSON_FILE_PATH = os.getcwd() + '/sceptreprj-dev_outputs.json'
CONFIG_FILE_PATH = os.getcwd() + '/config/config.yaml'
sceptreJsonOutput = SceptreJsonOutput(JSON_FILE_PATH, CONFIG_FILE_PATH)

with open('sceptreprj-dev_outputs.json', 'w') as f:
    json.dump(sceptreJsonOutput.parsedOutput, f)
