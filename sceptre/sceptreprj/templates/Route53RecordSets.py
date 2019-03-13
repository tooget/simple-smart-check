from troposphere import Template, Output, Ref, Join, GetAtt
from troposphere.route53 import AliasTarget, RecordSetType
import json


class RecordSets(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self._checkSceptreUserData(sceptre_user_data)
        self._createRecordSet()
        self._addRecordSetOutput()
    
    def _checkSceptreUserData(self, sceptre_user_data):
        self.sceptreUserData = sceptre_user_data
        try:
            self.sceptreUserData['recordset_params_recordsetname'] = json.loads(self.sceptreUserData['recordset_params_recordsetname'])['backends3bucketnameoutput']
        except:
            pass

    def _createRecordSet(self):
        recordsetName = self.sceptreUserData['recordset_params_recordsetname'].replace('.', '')
        self.recordset = self.template.add_resource(RecordSetType(
            recordsetName,
            HostedZoneName = Join('', [self.sceptreUserData['recordset_params_maindomain'], '.']),
            Name = Join('', [self.sceptreUserData['recordset_params_recordsetname'], '.']),
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
        ])

def sceptre_handler(sceptre_user_data):
    recordset = RecordSets(sceptre_user_data)
    # print(recordset.template.to_yaml())
    return recordset.template.to_yaml()
