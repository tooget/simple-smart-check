from troposphere import Template, Output, Ref, Join, GetAtt
from troposphere.cloudfront import Distribution, DistributionConfig, Origin, CustomOriginConfig, DefaultCacheBehavior, ViewerCertificate, ForwardedValues


class Distributions(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createDistribution()
        self._addDistionbutionOutput()

    def _createDistribution(self):
        distributtionName = self.sceptreUserData['distribution_params_s3bucketname'].replace('.', '') + 'Distribution'
        s3DomainName = self.sceptreUserData['distribution_params_s3httpurl'].replace('http://', '')
        s3OriginId = 'S3-Website-' + s3DomainName
        print('distributtionName', distributtionName)
        print('s3DomainName', s3DomainName)
        print('s3OriginId', s3OriginId)
        self.distribution = self.template.add_resource(Distribution(
            distributtionName,
            DistributionConfig = DistributionConfig(
                Origins = [Origin(
                    Id = s3OriginId,
                    DomainName = s3DomainName,
                    CustomOriginConfig = CustomOriginConfig(
                        HTTPPort = 80,
                        HTTPSPort = 443,
                        OriginReadTimeout = 30,
                        OriginKeepaliveTimeout = 5,
                        OriginProtocolPolicy = 'http-only'
                    )
                )],
                DefaultCacheBehavior = DefaultCacheBehavior(
                    ViewerProtocolPolicy = 'redirect-to-https',
                    AllowedMethods = ['HEAD', 'GET'],
                    CachedMethods = ['HEAD', 'GET'],
                    ForwardedValues = ForwardedValues(QueryString = False),
                    MinTTL = 0,
                    MaxTTL = 31536000,
                    DefaultTTL = 86400,
                    SmoothStreaming = False,
                    Compress = False,
                    TargetOriginId = s3OriginId,
                ),
                PriceClass = 'PriceClass_All',
                Aliases = [self.sceptreUserData['distribution_params_s3bucketname']],
                ViewerCertificate = ViewerCertificate(
                    AcmCertificateArn = self.sceptreUserData['distribution_params_certificatearn'],
                    SslSupportMethod = 'sni-only',
                    MinimumProtocolVersion = 'TLSv1.1_2016'
                ),
                Enabled = True,
                HttpVersion = 'http2',
                DefaultRootObject = 'index.html'
            )
        ))
    
    def _addDistionbutionOutput(self):
        self.template.add_output([
            Output(
                self.sceptreUserData['distribution_params_distributionid_prefix'],
                Value = Ref(self.distribution),
            ),
            Output(
                self.sceptreUserData['distribution_params_domainname_prefix'],
                Value = GetAtt(self.distribution, 'DomainName'),
            ),
        ])

def sceptre_handler(sceptre_user_data):
    distribution = Distributions(sceptre_user_data)
    # print(distribution.template.to_yaml())
    return distribution.template.to_yaml()
