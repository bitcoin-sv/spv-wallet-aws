from aws_cdk import (
    Stack,
    CfnParameter,
)
from constructs import Construct


from eks.cluster import EKS
from eks.helm_charts import HelmCharts
from eks.vpc import Vpc
from eks.external_dns_role import ExternalDNSRole
from eks.certificate import Certificate
from eks.custom_resources import CustomResourceLambda
from eks.route53 import Route53Entries
from eks.alb_controller import AlbController


class CdkEksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, helm_chart_version: str, eks_version: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        domainName = CfnParameter(self, 'domainName',
                                  type='String',
                                  description='Domain name. (Required)',
                                  allowed_pattern="(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]"
        )

        hostedzoneId = CfnParameter(self, 'hostedzoneId',
                                    type='AWS::Route53::HostedZone::Id',
                                    description='Hosted zone ID. (Required)',
                            )


        certificateConstruct= Certificate(self, "CertifcateConstruct",domainName,hostedzoneId)

        Route53Entries(self, " Route53Entries",domainName,hostedzoneId)

        vpcConstruct = Vpc(self,"VPCConstruct")

        clusterConstruct = EKS(self,"EKSConstruct", vpcConstruct.vpc)

        clusterConstruct.node.add_dependency(vpcConstruct)

        albController = AlbController(self,"AlbControllerConstruct", clusterConstruct.cluster)

        albController.node.add_dependency(clusterConstruct)
        albController.node.add_dependency(certificateConstruct)

        DNSrole = ExternalDNSRole(self,"DNSRoleConstruct", clusterConstruct.cluster)

        DNSrole.node.add_dependency(clusterConstruct)

        main_helm = HelmCharts(self,"HelmChartsConstruct",clusterConstruct.cluster, DNSrole.service_role,domainName,certificateConstruct.certificate, helm_chart_version)

        main_helm.node.add_dependency(clusterConstruct)
        main_helm.node.add_dependency(albController)

        cleanup=CustomResourceLambda(self, "CleanUpResource", clusterConstruct, eks_version)

        cleanup.node.add_dependency(main_helm)
        cleanup.node.add_dependency(clusterConstruct)
        cleanup.node.add_dependency(DNSrole)
        cleanup.node.add_dependency(albController)
