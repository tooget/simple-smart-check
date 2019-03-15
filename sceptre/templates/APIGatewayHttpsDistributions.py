from troposphere import Template, Output, Ref, GetAtt
from troposphere.apigateway import DomainName, BasePathMapping, EndpointConfiguration
from troposphere.route53 import RecordSetType
import json
import re


class APIGatewayHttpsDistributions(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self.sceptreUserData['apigatewayhttpsdist_params_zappa_status'] = json.loads(self.sceptreUserData['apigatewayhttpsdist_params_zappa_status'])
        self.sceptreUserData['apigatewayhttpsdist_params_subdomain'] = json.loads(self.sceptreUserData['apigatewayhttpsdist_params_subdomain'])
        self.reg = re.compile(r'(https|http)://(\w+).(.*?).(.*?).com/(\w+)')
        self._createAPIGatewayHttpsDistribution()
        self._createAPIGatewayHttpsDistributionBasePathMapping()
        self._addAPIGatewayHttpsDistributionOutput()

    def _extractAPIGatewayIdFromURL(self):
        apigatewayid = self.reg.sub('\g<2>', self.sceptreUserData['apigatewayhttpsdist_params_zappa_status']['API Gateway URL'])
        return apigatewayid

    def _extractAPIGatewayStageFromURL(self):
        apigatewayStage = self.reg.sub('\g<5>', self.sceptreUserData['apigatewayhttpsdist_params_zappa_status']['API Gateway URL'])
        return apigatewayStage

    def _createAPIGatewayHttpsDistribution(self):
        apigatewayhttpsdistName = self.sceptreUserData['apigatewayhttpsdist_params_subdomain']['backends3bucketnameoutput'].replace('.', '') + 'Distribution'
        self.apigatewayhttpsdist = self.template.add_resource(DomainName(
            apigatewayhttpsdistName,
            CertificateArn = self.sceptreUserData['apigatewayhttpsdist_params_certificatearn'],
            DomainName = self.sceptreUserData['apigatewayhttpsdist_params_subdomain']['backends3bucketnameoutput'],
            EndpointConfiguration = EndpointConfiguration(Types = ["EDGE"])
        ))
    
    def _createAPIGatewayHttpsDistributionBasePathMapping(self):
        basePathMappingName = self.sceptreUserData['apigatewayhttpsdist_params_subdomain']['backends3bucketnameoutput'].replace('.', '') + 'basePathMapping'
        self.template.add_resource(BasePathMapping(
            basePathMappingName,
            DomainName = Ref(self.apigatewayhttpsdist),
            RestApiId = self._extractAPIGatewayIdFromURL(),
            Stage = self._extractAPIGatewayStageFromURL()
        ))

    def _addAPIGatewayHttpsDistributionOutput(self):
        self.template.add_output([
            Output(
                self.sceptreUserData['apigatewayhttpsdist_params_apigatewayid_prefix'],
                Value = self._extractAPIGatewayIdFromURL(),
            ),
            Output(
                self.sceptreUserData['apigatewayhttpsdist_params_apigatewayhttpsdistid_prefix'],
                Value = Ref(self.apigatewayhttpsdist),
            ),
            Output(
                self.sceptreUserData['apigatewayhttpsdist_params_domainname_prefix'],
                Value = GetAtt(self.apigatewayhttpsdist, 'DistributionDomainName'),
            ),
        ])

def sceptre_handler(sceptre_user_data):
    apigatewayhttpsdist = APIGatewayHttpsDistributions(sceptre_user_data)
    # print(apigatewayhttpsdist.template.to_yaml())
    return apigatewayhttpsdist.template.to_yaml()