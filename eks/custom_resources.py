from aws_cdk import aws_lambda as _lambda, CustomResource, Duration
from constructs import Construct
from aws_cdk.lambda_layer_kubectl_v28 import KubectlV28Layer
from aws_cdk.lambda_layer_awscli import AwsCliLayer
from aws_cdk import aws_logs as logs
from aws_cdk import RemovalPolicy

class CustomResourceLambda(Construct):
    def __init__(self, scope: Construct, id: str, cluster, eks_version, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        kubectl_layer = KubectlV28Layer(self, 'KubectlV28Layer')
        awscli_layer = AwsCliLayer(self,'AwsCliLayer')

        log_group = logs.LogGroup(self, "CleanUpLambdaLogGroup",
                                  log_group_name=f"/aws/lambda/CleanUpLambda-{cluster.cluster.cluster_name}",
                                  retention=logs.RetentionDays.FIVE_DAYS,
                                  removal_policy=RemovalPolicy.DESTROY)

        wait_lambda = _lambda.Function(
            self, f'CleanUpLambda',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='wait_lambda_function.handler',
            code=_lambda.Code.from_asset('eks'),
            timeout=Duration.seconds(180),
            role=cluster.lambda_role,
            log_group=log_group
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

        log_group = logs.LogGroup(self, "UpgradeLambdaLogGroup",
                                  log_group_name=f"/aws/lambda/UpgradeLambda-{cluster.cluster.cluster_name}",
                                  retention=logs.RetentionDays.FIVE_DAYS,
                                  removal_policy=RemovalPolicy.DESTROY)

        upgrade_lambda = _lambda.Function(
            self, f'UpgradeLambda',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='upgrade_lambda_function.handler',
            code=_lambda.Code.from_asset('eks'),
            timeout=Duration.seconds(180),
            role=cluster.lambda_role,
            log_group=log_group
        )

        upgrade_lambda.add_layers(kubectl_layer)
        upgrade_lambda.add_layers(awscli_layer)

        self.wait_resource= CustomResource(self, "UpgradeLambdaResource",
                                           resource_type="Custom::MyCustomResourceType",
                                           service_token=upgrade_lambda.function_arn,
                                           properties={
                                               "cluster_name" : cluster.cluster.cluster_name,
                                               "role_arn" : cluster.masters_role.role_arn,
                                               "nodegroup_name" : cluster.nodegroup.nodegroup_name,
                                               "eks_version" : eks_version
                                           }
                                           )