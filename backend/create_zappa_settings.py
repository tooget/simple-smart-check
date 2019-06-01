import json
import os


class Zappa(object):

    def __init__(self, JSON_FILE_PATH):
        self.sceptreOutputs = json.loads(open(JSON_FILE_PATH).read())
        self.settings = {
            'dev': {
                'app_function': 'app.__init__.app',
                'aws_region': '',
                # 'profile_name': 'default',        # if 'profile_name' doesn't exits, skip '~/.aws/credential' file and read credentials from environmental variables, https://velog.io/@city7310/%EB%B0%B1%EC%97%94%EB%93%9C%EA%B0%80-%EC%9D%B4%EC%A0%95%EB%8F%84%EB%8A%94-%ED%95%B4%EC%A4%98%EC%95%BC-%ED%95%A8-11.-%EB%B0%B0%ED%8F%AC-%EC%9E%90%EB%8F%99%ED%99%94
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
                    '/sceptre/sceptreprj-dev_outputs.json'
zappa = Zappa(JSON_FILE_PATH)

with open('zappa_settings.json', 'w') as f:
    json.dump(zappa.settings, f)
