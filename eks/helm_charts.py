from aws_cdk import aws_eks as eks
from constructs import Construct

class HelmCharts(Construct):
    def __init__(self, scope: Construct, id: str, cluster, service_role, domainName, certificateArn, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        externaldns=eks.HelmChart(
            self,
            "ExternelDNS",
            cluster=cluster,
            chart="external-dns",
            repository="https://charts.bitnami.com/bitnami",
            release="external-dns",
            namespace="kube-system",
            values={
                "domainFilters": [domainName.value_as_string],
                "provider": "aws",
                "policy": "sync",
                "registry": "txt",
                "interval": "30s",
                "rbac": {
                    "create": "true",
                    "serviceAccountName": "external-dns",
                    "serviceAccountAnnotations": {
                        "eks.amazonaws.com/role-arn": service_role.role_arn
                    },
                },
            },
            wait=True,
        )

        buxcli=eks.HelmChart(
            self,
            "BuxCli",
            cluster=cluster,
            chart="bux-cli",
            repository="https://buxorg.github.io/bux-helm/",
            namespace="default",
            release="bux-cli",
            version= "0.1.0",
        )

        bux=(eks.HelmChart(
            self,
            "BuxChart",
            cluster=cluster,
            chart="bux",
            repository="https://buxorg.github.io/bux-helm/",
            namespace="default",
            release="bux",
            version= "0.2.0",
            values={
                "global" : {
                    "domainName": domainName.value_as_string,
                    "certificate_arn": certificateArn,
                }
            },
        ))

        bux.node.add_dependency(externaldns)
        bux.node.add_dependency(buxcli)
