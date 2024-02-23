from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class Vpc(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(self, 'EksVpc',
                      ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
                      max_azs=2,
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              name='PublicSubnet',
                              subnet_type=ec2.SubnetType.PUBLIC,
                              cidr_mask=24
                          )
                      ]
                      )
