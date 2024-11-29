from aws_cdk import aws_eks as eks
from constructs import Construct


class HelmCharts(Construct):
    def __init__(self, scope: Construct, id: str, cluster, service_role, domainName, certificateArn,
                 config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        external_dns_version=config["external_dns_version"]
        helm_chart_version=config["helm_chart_version"]

        externaldns = eks.HelmChart(
            self,
            "ExternelDNS",
            cluster=cluster,
            chart="external-dns",
            repository="oci://registry-1.docker.io/bitnamicharts/external-dns",
            release="external-dns",
            version=external_dns_version,
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

        spvwallet = (eks.HelmChart(
            self,
            "SpvWalletChart",
            cluster=cluster,
            chart="spv-wallet-stack",
            repository="https://bitcoin-sv.github.io/spv-wallet-helm",
            namespace="default",
            release="bsv",
            version=helm_chart_version,
            values={
                "global": {
                    "domainName": domainName.value_as_string,
                    "ingress": {
                        "certificate_arn": certificateArn,
                    }
                }
            },
        ))

        spvwallet.node.add_dependency(externaldns)
