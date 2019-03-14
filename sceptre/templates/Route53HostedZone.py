from troposphere import Template, Output, Ref
from troposphere.route53 import HostedZone


class HostedZones(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        # self._createHostedZone()
        self._addHostedZoneIdOutput()

    # def _createHostedZone(self):
    #     self.hostedZone = self.template.add_resource(HostedZone(
    #         self.sceptreUserData['hostedzone_prefix'],
    #         Name = self.sceptreUserData['hostedzone_maindomain_prefix'],
    #     ))
    
    def _addHostedZoneIdOutput(self):
        self.template.add_output([
            Output(
                self.sceptreUserData['hostedzone_params_hostedzoneid_prefix'],
                # Value = Ref(self.hostedZone),
                Value = self.sceptreUserData['hostedzone_hostedzoneid_prefix'],
            ),
            Output(
                self.sceptreUserData['hostedzone_params_maindomain'],
                Value = self.sceptreUserData['hostedzone_maindomain_prefix'],
            ),
        ])

def sceptre_handler(sceptre_user_data):
    hostedZone = HostedZones(sceptre_user_data)
    # print(hostedZone.template.to_yaml())
    return hostedZone.template.to_yaml()