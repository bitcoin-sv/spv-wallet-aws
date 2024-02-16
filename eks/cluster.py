from aws_cdk import (
    aws_eks as _eks,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
    CfnCondition,
)

from constructs import Construct
from aws_cdk.lambda_layer_kubectl_v28 import KubectlV28Layer
import aws_cdk as core


class EKS(Construct):
    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        kubectl_layer = KubectlV28Layer(self, 'KubectlV28Layer')
        self.cluster = _eks.Cluster(self, "EKSCluster",
                              version=_eks.KubernetesVersion.V1_28,
                              default_capacity=0,
                              kubectl_layer= kubectl_layer,
                              vpc=vpc,
                              vpc_subnets = [ ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC) ],
                              )

        nodegroup = self.cluster.add_nodegroup_capacity("node-group",
                                       instance_types=[ec2.InstanceType("t3.small")],
                                       min_size=3,
                                       disk_size=30,
                                       ami_type=_eks.NodegroupAmiType.AL2_X86_64,

                                       )

        # Node grooup access to Route53
        nodegroup.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRoute53FullAccess")
        )

        # Node grooup access to EBS volumes
        nodegroup.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEBSCSIDriverPolicy")
        )

        # EBS CSI addon installation
        ebs_csi_addon = _eks.CfnAddon(
            self,
            "EbsCsiAddonSa",
            addon_name="aws-ebs-csi-driver",
            cluster_name=self.cluster.cluster_name,
            resolve_conflicts="OVERWRITE",
        )

        #Add Lambda role
        self.lambda_role = iam.Role(self, "LambdaRole",
                                    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
                                    )
        self.lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        self.lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))

        lambda_role_policy = iam.PolicyStatement(
            actions=['eks:AccessKubernetesApi','eks:Describe*','eks:List*','sts:GetCallerIdentity'],
            resources=['*'],  # Adjust the resource ARN if needed
        )
        self.lambda_role.add_to_policy(lambda_role_policy)
        self.cluster.aws_auth.add_role_mapping(role=self.lambda_role, groups=["system:masters"], username="lambda")

        # Create an IAM Role to be assumed by admins
        self.masters_role = iam.Role(
            self,
            'EksMastersRole',
            assumed_by=iam.CompositePrincipal(
                iam.AccountRootPrincipal(),
                self.lambda_role,
            )
        )
        # add masters_role assume by lambda policy

        # Attach an IAM Policy to that Role so users can access the Cluster
        masters_role_policy = iam.PolicyStatement(
            actions=['eks:AccessKubernetesApi','eks:Describe*','eks:List*'],
            resources=['*'],  # Adjust the resource ARN if needed
        )
        self.masters_role.add_to_policy(masters_role_policy)
        self.cluster.aws_auth.add_masters_role(self.masters_role)

        CfnOutput(
            self,
            'ClusterNameOutput',
            value=self.cluster.cluster_name,
        )
        # Output the EKS master role ARN
        CfnOutput(
            self,
            'ClusterMasterRoleOutput',
            value=self.masters_role.role_arn
        )

        CfnOutput(
            self,
            'ClusterConfig',
            value=f"aws eks update-kubeconfig --name {self.cluster.cluster_name} --region={core.Aws.REGION} --role-arn={self.masters_role.role_arn}"
        )
