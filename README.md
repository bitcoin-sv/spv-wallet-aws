# Enviroments

Enviroments configurations for test and prod are kept in the config folder.

### Config file structure

```
# Bucket to store the template file
template_bucket_name: bux-test-template  

# Prefix for specific region asset bucket
file_asset_bucket_name_prefix: bux-test-marketplace-assets 

# AWS Regions set
file_asset_region_set: ['eu-central-1','us-east-1']  

# Prefix for files in all buckets
file_asset_prefix: bux/latest/ 
```

# Code release for test env

```console

# Generate a template for the target environment
cdk synth --context=deployment=test 

# Update path in assets configuration for temporary path
sed -i 's/latest/new/g' cdk.out/EksStack.assets.json

# Upload assets to the temporary path (npx is going to use default AWS profile or AWS_PROFILE if set)
npx cdk-assets publish -p cdk.out/EksStack.assets.json -v

# Move old template to the archive path
aws s3 --recursive mv s3://bux-test-template/bux/latest s3://bux-test-template/bux/old

# Move new template to the latest path
aws s3 --recursive mv s3://bux-test-template/bux/new s3://bux-test-template/bux/latest
```

# URL's to deploy test environment

https://eu-central-1.console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/quickcreate?templateURL=https://bux-test-template.s3.eu-central-1.amazonaws.com/bux/latest/EksStack.template.json

https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://bux-test-template.s3.eu-central-1.amazonaws.com/bux/latest/EksStack.template.json


# Code release for prod env

```console

# Generate a template for the target enviroment
cdk synth --context=deployment=prod 

# Update path in assets configuration for temporary path
sed -i 's/latest/new/g' cdk.out/EksStack.assets.json

# Upload assets to the temporary path (npx is going to use default AWS profile or AWS_PROFILE if set)
npx cdk-assets publish -p cdk.out/EksStack.assets.json -v

# Move old template to archive path
aws s3 --recursive mv s3://bux-template/bux/latest s3://bux-template/bux/old

# Move new template to latest path
aws s3 --recursive mv s3://bux-template/bux/new s3://bux-template/bux/latest
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
# install cdk cli with spefycic version
npm install aws-cdk@2.118.0 
npm install cdk-assets@2.118.0 

# Install Python dependencies (in case of using a virtual environment active it first)
python -m pip install -r requirements.txt
```

## Software versions used

|   |   |  
|---|---|
|  AWS CLI  | 2.6.3  |   
|   NodeJS |  16.20.2 |  
|   Npm |  8.19.4  |   
|   Python |  3.8.0 |       
|   CDK |  2.118.0   |      


# Kubernetes version update

In cluster.py update:
- Kubernetes version property in cluster construct (ex. _eks.KubernetesVersion.V1_29).
  Make sure that CDK version in requirementsis supporting specyfic Kubernetes version, if needed update CDK version.
  Information can be found at https://github.com/aws/aws-cdk/releases
- Cluster nodes image release version property in nodegroup construct (ex. release_version="1.29.0-20240202")
  EKS nodes images release version can be found at https://github.com/awslabs/amazon-eks-ami/releases
- Kubernetes lamda layer to same version as Kubernetes cluster. Lambda Layer requires update within requirements.
  