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

CdkEksStack(app, "EksStack", config["helm_chart_version"], config["eks_version"],
            synthesizer=BootstraplessStackSynthesizer(template_bucket_name=config["template_bucket_name"],
                                                      file_asset_bucket_name=config["file_asset_bucket_name_prefix"]+"-${AWS::Region}",
                                                      file_asset_region_set=config["file_asset_region_set"],
                                                      file_asset_prefix=config["file_asset_prefix"])
            )

app.synth()
