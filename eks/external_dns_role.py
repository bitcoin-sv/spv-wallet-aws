from aws_cdk import aws_iam as iam, CfnJson
from constructs import Construct

class ExternalDNSRole(Construct):
    def __init__(self, scope: Construct, id: str, eks_cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        conditions = CfnJson(
            self,
            id="ConditionJson",
            value={
                f"{eks_cluster.open_id_connect_provider.open_id_connect_provider_issuer}:aud": "sts.amazonaws.com"
            },
        )

        self.service_role = iam.Role(
            self,
            "externelDnsRole",
            assumed_by=iam.FederatedPrincipal(
                federated=eks_cluster.open_id_connect_provider.open_id_connect_provider_arn,
                conditions={"StringEquals": conditions},
                assume_role_action="sts:AssumeRoleWithWebIdentity",
            ),
        )
        self.service_role .add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSClusterPolicy")
        )

        self.service_role .add_to_principal_policy(
            iam.PolicyStatement(
                actions=["route53:ChangeResourceRecordSets"],
                resources=["arn:aws:route53:::hostedzone/*"],
            )
        )
        self.service_role .add_to_principal_policy(
            iam.PolicyStatement(
                actions=["route53:ListHostedZones", "route53:ListResourceRecordSets"],
                resources=["*"],
            )
)