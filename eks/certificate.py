from aws_cdk import aws_certificatemanager as certificatemanager
import aws_cdk as core
from constructs import Construct

class Certificate(Construct):

    def __init__(self, scope: Construct, construct_id: str, domain_name, hosted_zone_id, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cert = certificatemanager.CfnCertificate(self, "SpvWalletCertificate",
                                                    domain_name=f"*.{domain_name.value_as_string}",
                                                    subject_alternative_names=[domain_name.value_as_string],
                                                    domain_validation_options=[certificatemanager.CfnCertificate.DomainValidationOptionProperty(
                                                        domain_name=f"*.{domain_name.value_as_string}",
                                                        hosted_zone_id=hosted_zone_id.value_as_string,
                                                    )],
                                                    validation_method=certificatemanager.ValidationMethod.DNS.value)
        self.certificate=core.Fn.ref(cert.logical_id)


