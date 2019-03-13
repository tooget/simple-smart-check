from troposphere import Template, Ref, Join, Output, GetAtt
from troposphere.s3 import Bucket, BucketPolicy, WebsiteConfiguration


class S3Publics(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createS3Bucket()
        self._addPolicyToS3Bucket()
        self._addS3Outputs()
    
    def _createS3Bucket(self):
        self.s3 = self.template.add_resource(Bucket(
                self.sceptreUserData['s3_bucket'],
                BucketName = Join('', [self.sceptreUserData['s3_hosting_subdomain_url'], '.', self.sceptreUserData['s3_hosting_maindomain']]),
                WebsiteConfiguration = WebsiteConfiguration(
                    IndexDocument = self.sceptreUserData['s3_hosting_rootfile'],
                    ErrorDocument = self.sceptreUserData['s3_hosting_rootfile'],
                )))
    
    def _addPolicyToS3Bucket(self):
        self.s3Policy = self.template.add_resource(BucketPolicy(
            self.sceptreUserData['s3_policy'],
            Bucket = Ref(self.s3),
            PolicyDocument = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [Join("", ["arn:aws:s3:::", Ref(self.s3) , "/*" ])]
                }]
            }
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
            Output(
                self.sceptreUserData['s3_params_s3hostingrootfile_prefix'],
                Value = self.sceptreUserData['s3_hosting_rootfile'],
            ),
        ])

def sceptre_handler(sceptre_user_data):
    s3public = S3Publics(sceptre_user_data)
    # print(s3public.template.to_yaml())
    return s3public.template.to_yaml()