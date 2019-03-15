import json
import os


class Frontend(object):

    def __init__(self, JSON_FILE_PATH):
        self.sceptreOutputs = json.loads(open(JSON_FILE_PATH).read())
        self.wwwDeployScript = 'yarn run build && aws s3 sync ./dist s3://{}'.format(self.sceptreOutputs['wwws3bucketnameoutput'])
        self.adminDeployScript = 'yarn run build && aws s3 sync ./dist s3://{}'.format(self.sceptreOutputs['admins3bucketnameoutput'])

        print(self.wwwDeployScript)
        print(self.adminDeployScript)


JSON_FILE_PATH = os.path.dirname(os.getcwd()) + \
                    '/sceptre/sceptreprj-dev_outputs.json'
print(JSON_FILE_PATH)
frontend = Frontend(JSON_FILE_PATH)

with open('admin/deploy.sh', 'w') as f:
    f.write(frontend.adminDeployScript)
    f.close()

with open('www/deploy.sh', 'w') as f:
    f.write(frontend.wwwDeployScript)
    f.close()