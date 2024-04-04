# Enviroments

Environment configuration for test and prod are kept in the config folder.

### Config file structure

```
# Bucket to store the template file
template_bucket_name: spv-wallet-test-template  

# Prefix for specific region asset bucket
file_asset_bucket_name_prefix: spv-wallet-test-marketplace-assets 

# AWS Regions set
file_asset_region_set:
  - 'eu-central-1'
  - 'us-east-1'
  - 'eu-north-1'

# Prefix for files in all buckets
file_asset_prefix: spv-wallet/latest/ 
```

# Development environment setup

## AWS Client Setup and credentials configuration
```console
# download AWS client installer
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip

#install AWS client
sudo ./aws/install

# configure credentials
aws configure
```

## CDK setup for Python

```console
# install cdk cli with specific version
npm install aws-cdk@2.118.0 
npm install cdk-assets@2.118.0 

# Install Python dependencies (in case of using a virtual environment active it first)
python -m pip install -r requirements.txt
```

# Code release

1. Before you start setup your environment as described in the Development environment setup section.
2. Ensure that your AWS credentials are configured and are connected with proper account.
3. Use update.sh script to deploy the template to the AWS s3.

```console
./update.sh {environment}
```

Where {environment} is the name of the environment you want to deploy (dev or test or prod).

example:

```console
./update.sh prod
```

By default, the script will deploy the template to the test environment.

4. Commit changes made by the script.


**Additional information:**

- the script first will check if there is newer version of helm chart and if so, then it will be updated in {environment}.yaml file
- then it will prepare the template
- then it will upload it to the spv-wallet/new folder in the bucket
- after that, it will move the template from the spv-wallet/latest to the spv-wallet/old folder
- and finally, it will move the template from the spv-wallet/new to the spv-wallet/latest folder

# URL's to deploy environment

## Production version:
| Region | CloudFormation template link |
|--------|------------------------------|
| AP     | [ap-south-1](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-northeast-1](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-northeast-2](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-northeast-3](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-3#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-southeast-1](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-southeast-2](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json) |
| CA     | [ca-central-1](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json) |
| EU     | [eu-central-1](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [eu-west-1](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [eu-west-2](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [eu-west-3](https://console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [eu-north-1](https://console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json) |
| SA     | [sa-east-1](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json) |
| US     | [us-east-1](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [us-east-2](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [us-west-1](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [us-west-2](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/quickcreate?templateURL=https://spv-wallet-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json) |

## Test version:
| Region | CloudFormation template link                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AP     | [ap-south-1](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-northeast-1](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-northeast-2](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-northeast-3](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-3#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-southeast-1](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [ap-southeast-2](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json) |
| CA     | [ca-central-1](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| EU     | [eu-central-1](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [eu-west-1](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [eu-west-2](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [eu-west-3](https://console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [eu-north-1](https://console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json)                                                                                                                                                                                                                                                          |
| SA     | [sa-east-1](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| US     | [us-east-1](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [us-east-2](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [us-west-1](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [us-west-2](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/quickcreate?templateURL=https://spv-wallet-test-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json)                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |


## Dev version:
| Region | CloudFormation template link                                                                                                                                                                                                                                                                                                                                                                                                   |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EU     | [eu-central-1](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/quickcreate?templateURL=https://spv-wallet-dev-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json), [eu-north-1](https://console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/quickcreate?templateURL=https://spv-wallet-dev-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json) |
| US     | [us-east-1](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://spv-wallet-dev-template.s3.amazonaws.com/spv-wallet/latest/EksStack.template.json)                                                                                                                                                                                                                     |


# Kubernetes version update

In cluster.py update:
- Kubernetes version property in cluster construct (ex. _eks.KubernetesVersion.V1_29).
  Make sure that CDK versio©†n in the requirements supporting specific Kubernetes version, if needed update CDK version.
  Information can be found at https://github.com/aws/aws-cdk/releases
- Cluster nodes image release version property in node group construct (ex. release_version="1.29.0-20240202")
  EKS nodes images release version can be found at https://github.com/awslabs/amazon-eks-ami/releases
- Kubernetes lambda layer to the same version as Kubernetes cluster. Lambda Layer requires an update within requirements.
