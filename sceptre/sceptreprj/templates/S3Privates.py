from troposphere import Template, Ref, GetAtt, Output, Join
from troposphere.s3 import Bucket, Private


class S3Privates(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createS3Bucket()
        self._addS3Outputs()
    
    def _createS3Bucket(self):
        self.s3 = self.template.add_resource(Bucket(
            self.sceptreUserData['s3_bucket'],
            BucketName = Join('', [self.sceptreUserData['s3_hosting_subdomain_url'], '.', self.sceptreUserData['s3_hosting_maindomain']]),
            AccessControl = Private
        ))

    def _addS3Outputs(self):
        self.template.add_output([
            Output(
                self.sceptreUserData['s3_params_s3bucketname_prefix'],
                Value = Ref(self.s3),
            ),
            Output(
                self.sceptreUserData['s3_params_s3httpurl_prefix'],
                Value = GetAtt(self.s3, 'WebsiteURL'),
            ),
        ])

def sceptre_handler(sceptre_user_data):
    s3private = S3Privates(sceptre_user_data)
    # print(s3private.template.to_yaml())
    return s3private.template.to_yaml()