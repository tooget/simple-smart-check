from troposphere import Template, Parameter, Output, Ref, Tags, Join
from troposphere.certificatemanager import Certificate, DomainValidationOption
from troposphere.route53 import RecordSetType


class ACMCertificates(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        # self._createCertificate()
        # self._addCNAMERecordset()
        self._addCertificateOutput()

    # def _createCertificate(self):
    #     acmcertificateName = self.sceptreUserData['acmcertificate_params_maindomain'].replace('.', '') + 'Certificate'
    #     self.acmcertificate = self.template.add_resource(Certificate(
    #         acmcertificateName,
    #         DomainName = self.sceptreUserData['acmcertificate_params_maindomain'],
    #         SubjectAlternativeNames = [self.sceptreUserData['acmcertificate_params_maindomain'], Join('.', ['*', self.sceptreUserData['acmcertificate_params_maindomain']])],
    #         DomainValidationOptions = [
    #             DomainValidationOption(
    #                 DomainName = self.sceptreUserData['acmcertificate_params_maindomain'],
    #                 ValidationDomain = self.sceptreUserData['acmcertificate_params_maindomain'],
    #             ),
    #             DomainValidationOption(
    #                 DomainName = Join('.', ['*', self.sceptreUserData['acmcertificate_params_maindomain']]),
    #                 ValidationDomain = Join('.', ['*', self.sceptreUserData['acmcertificate_params_maindomain']]),
    #             ),
    #         ],
    #         ValidationMethod = 'DNS',
    #     ))
    
    # def _addCNAMERecordset(self):
    #     acmcertificateCnameRecordsetName = self.sceptreUserData['acmcertificate_params_maindomain'].replace('.', '') + 'CnameRecordSet'
    #     self.cnamerecordset = self.template.add_resource(RecordSetType(
    #         acmcertificateCnameRecordsetName,
    #         HostedZoneName = Join('', [self.sceptreUserData['acmcertificate_params_maindomain'], '.']),
    #         Name = self.sceptreUserData['acmcertificate_params_recordsetname'],
    #         Type = "CNAME",
    #         TTL = "900",
    #         ResourceRecords = [self.sceptreUserData['acmcertificate_params_recordsetvalue']],
    #     ))

    def _addCertificateOutput(self):
        self.template.add_output(Output(
            self.sceptreUserData['acmcertificate_params_certificatearn_prefix'],
            Value = self.sceptreUserData['acmcertificate_params_certificatearn'],
        ))

def sceptre_handler(sceptre_user_data):
    acmcertificate = ACMCertificates(sceptre_user_data)
    # print(acmcertificate.template.to_yaml())
    return acmcertificate.template.to_yaml()
