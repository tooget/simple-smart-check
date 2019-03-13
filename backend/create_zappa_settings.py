import json
import os


class Zappa(object):

    def __init__(self, JSON_FILE_PATH):
        self.sceptreOutputs = json.loads(open(JSON_FILE_PATH).read())
        self.settings = {
            'dev': {
                'app_function': 'app.__init__.app',
                'aws_region': '',
                'profile_name': 'default',
                'project_name': '',
                'runtime': 'python3.6',
                'keep_warm': False,
                'memory_size': 256,
                'timeout_seconds': 30,
                's3_bucket': '',
                'aws_environment_variables': {
                    'RDS_ENDPOINT_URL': '',
                    'RDS_USERNAME': '',
                    'RDS_USERPASSWORD': ''
                },
                'vpc_config': {
                    'SubnetIds': [],
                    'SecurityGroupIds': []
                }
            }
        }

        self.settings['dev']['aws_region'] = self.sceptreOutputs['region']
        self.settings['dev']['project_name'] = self.sceptreOutputs['project_code']
        self.settings['dev']['s3_bucket'] = self.sceptreOutputs['backends3bucketnameoutput']
        self.settings['dev']['aws_environment_variables']['RDS_ENDPOINT_URL'] = self.sceptreOutputs['dbendpoint']
        self.settings['dev']['aws_environment_variables']['RDS_USERNAME'] = self.sceptreOutputs['dbusername']
        self.settings['dev']['aws_environment_variables']['RDS_USERPASSWORD'] = self.sceptreOutputs['dbuserpassword']
        self.settings['dev']['vpc_config']['SubnetIds'].append(self.sceptreOutputs['privatesubnet1idoutput'])
        self.settings['dev']['vpc_config']['SecurityGroupIds'].append(self.sceptreOutputs['sgidoutput'])

JSON_FILE_PATH = os.path.dirname(os.getcwd()) + \
                    '/sceptre/sceptreprj/sceptreprj-dev_outputs.json'
zappa = Zappa(JSON_FILE_PATH)

with open('zappa_settings.json', 'w') as f:
    json.dump(zappa.settings, f)
