from troposphere import Template, Output, Ref, Join, GetAtt
from troposphere.route53 import AliasTarget, RecordSetType


class RecordSets(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createRecordSet()
        self._addRecordSetOutput()

    def _createRecordSet(self):
        recordsetName = self.sceptreUserData['recordset_params_s3bucketname'].replace('.', '')
        print('recordsetName', recordsetName)
        print('HostedZoneName', self.sceptreUserData['recordset_params_maindomain'] + '.')
        print('Name', self.sceptreUserData['recordset_params_s3bucketname'] + '.')
        print('Type', self.sceptreUserData['recordset_params_recordtype'])
        print('HostedZoneId', self.sceptreUserData['recordset_params_cloudfronthostedzoneid'])
        print('DNSName', self.sceptreUserData['recordset_params_distibutiondomainname'] + '.')
        self.recordset = self.template.add_resource(RecordSetType(
            recordsetName,
            HostedZoneName = Join('', [self.sceptreUserData['recordset_params_maindomain'], '.']),
            Name = Join('', [self.sceptreUserData['recordset_params_s3bucketname'], '.']),
            Type = self.sceptreUserData['recordset_params_recordtype'],
            AliasTarget = AliasTarget(
                HostedZoneId = self.sceptreUserData['recordset_params_cloudfronthostedzoneid'],
                DNSName = self.sceptreUserData['recordset_params_distibutiondomainname'],
            )
        ))
    
    def _addRecordSetOutput(self):
        self.template.add_output([
            Output(
                self.sceptreUserData['recordset_params_recordsetid_prefix'],
                Value = Ref(self.recordset),
            ),
            # Output(
            #     # self.sceptreUserData['hostedzone_params_maindomain'],
            #     # Value = self.sceptreUserData['hostedzone_maindomain_prefix'],
            # ),
        ])

def sceptre_handler(sceptre_user_data):
    recordset = RecordSets(sceptre_user_data)
    # print(recordset.template.to_yaml())
    return recordset.template.to_yaml()
