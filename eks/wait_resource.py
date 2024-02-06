from aws_cdk import aws_lambda as _lambda, CustomResource, Duration
from constructs import Construct
from aws_cdk.lambda_layer_kubectl_v28 import KubectlV28Layer
from aws_cdk.lambda_layer_awscli import AwsCliLayer
from aws_cdk import aws_iam as iam

class CleanUpResource(Construct):
    def __init__(self, scope: Construct, id: str, cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        kubectl_layer = KubectlV28Layer(self, 'KubectlV28Layer')
        awscli_layer = AwsCliLayer(self,'AwsCliLayer')
        self.lambda_role = iam.Role(self, "LambdaRole",
                                    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
                                    )
        self.lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        self.lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))

        lambda_role_policy = iam.PolicyStatement(
            actions=['eks:AccessKubernetesApi','eks:Describe*','eks:List*','sts:GetCallerIdentity'],
            resources=['*'],
        )
        self.lambda_role.add_to_policy(lambda_role_policy)

        wait_lambda = _lambda.Function(
            self, f'CleanUpLambda',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='wait_lambda_function.handler',
            code=_lambda.Code.from_asset('eks'),
            timeout=Duration.seconds(180),
            role=cluster.lambda_role,
        )

        wait_lambda.add_layers(kubectl_layer)
        wait_lambda.add_layers(awscli_layer)

        self.wait_resource= CustomResource(self, "LambdaCustomResource",
                       resource_type="Custom::MyCustomResourceType",
                       service_token=wait_lambda.function_arn,
                       properties={
                           "cluster_name" : cluster.cluster.cluster_name,
                           "role_arn" : cluster.masters_role.role_arn,
                       }
                       )