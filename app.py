#!/usr/bin/env python3
import os

import aws_cdk as cdk
import yaml
from cdk_bootstrapless_synthesizer import BootstraplessStackSynthesizer

from eks.root import CdkEksStack

app = cdk.App()

# env = cdk.Environment(
#     region=os.environ["CDK_DEFAULT_REGION"],
#     account=os.environ["CDK_DEFAULT_ACCOUNT"]
# )
deployment = app.node.try_get_context("deployment")

with open(f'config/{deployment}.yml', 'r',encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

CdkEksStack(app, "EksStack",
            synthesizer=BootstraplessStackSynthesizer(template_bucket_name=config["template_bucket_name"],
                                                      file_asset_bucket_name=config["file_asset_bucket_name_prefix"]+"-${AWS::Region}",
                                                      file_asset_region_set=config["file_asset_region_set"],
                                                      file_asset_prefix=config["file_asset_prefix"])
            )

# CdkEksStack(app, "EksStack",
#             synthesizer=BootstraplessStackSynthesizer(template_bucket_name="bux-template",
#                                                       file_asset_bucket_name="bux-marketplace-assets-${AWS::Region}",
#                                                       file_asset_region_set=['ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2',
#                                                                              'ca-central-1',
#                                                                              'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1',
#                                                                              'sa-east-1',
#                                                                              'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2'],
#                                                       file_asset_prefix="bux/latest/")
#     )

app.synth()
