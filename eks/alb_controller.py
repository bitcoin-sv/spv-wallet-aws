from aws_cdk import aws_eks as eks
from constructs import Construct

class AlbController(Construct):

    def __init__(self, scope: Construct, construct_id: str, cluster, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        alb_controller = eks.AlbController(self, "AlbController",
                                           cluster=cluster,
                                           version=eks.AlbControllerVersion.V2_6_2,
                                           )

