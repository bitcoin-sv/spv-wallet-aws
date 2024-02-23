from aws_cdk import aws_route53 as route53
from constructs import Construct

class Route53Entries(Construct):

    def __init__(self, scope: Construct, construct_id: str, domain_name, hosted_zone_id, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(self,"HostedZone", hosted_zone_id=hosted_zone_id.value_as_string, zone_name=domain_name.value_as_string)
        srv_record = route53.SrvRecord(self, "SrvRecord",
                                       values=[route53.SrvRecordValue(
                                           host_name=domain_name.value_as_string,
                                           port=443,
                                           priority=10,
                                           weight=10
                                       )],
                                       zone=hosted_zone,
                                       record_name=f"_bsvalias._tcp.{domain_name.value_as_string}",
                                       )



