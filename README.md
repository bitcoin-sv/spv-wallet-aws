
# Enviroments

Enviroments configuration for test and prod are kept in config folder.

### Config file structure

```
# Bucket to store template file
template_bucket_name: bux-test-template  

# Prefix for specyfic region asset bucket
file_asset_bucket_name_prefix: bux-test-marketplace-assets 

# AWS Regions set
file_asset_region_set: ['eu-central-1','us-east-1']  

# Prefix for files in all buckets
file_asset_prefix: bux/latest/ 
```

# Code release for test env

```console

# Generate template for target enviroment
cdk synth --context=deployment=test 

# Update path in assets configuration for temporary path
sed -i 's/latest/new/g' cdk.out/EksStack.assets.json

# Upload assets to temporary path (npx is going to use default AWS profile or AWS_PROFILE if set)
npx cdk-assets publish -p cdk.out/EksStack.assets.json -v

# Move old template to archive path
aws s3 --recursive mv s3://bux-test-template/bux/latest s3://bux-test-template/bux/old

# Move new template to latest path
aws s3 --recursive mv s3://bux-test-template/bux/new s3://bux-test-template/bux/latest
```

# URL's to deploy test enviroment

https://eu-central-1.console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/quickcreate?templateURL=https://bux-test-template.s3.eu-central-1.amazonaws.com/bux/latest/EksStack.template.json

https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://bux-test-template.s3.eu-central-1.amazonaws.com/bux/latest/EksStack.template.json


# Code release for prod env

```console

# Generate template for target enviroment
cdk synth --context=deployment=prod 

# Update path in assets configuration for temporary path
sed -i 's/latest/new/g' cdk.out/EksStack.assets.json

# Upload assets to temporary path (npx is going to use default AWS profile or AWS_PROFILE if set)
npx cdk-assets publish -p cdk.out/EksStack.assets.json -v

# Move old template to archive path
aws s3 --recursive mv s3://bux-template/bux/latest s3://bux-template/bux/old

# Move new template to latest path
aws s3 --recursive mv s3://bux-template/bux/new s3://bux-template/bux/latest
```

# Development enviroment setup

## AWS Client Setup and credentials configuration
```console
# download client installer
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# configure credentials
aws configure
```

## CDK setup for Python

```console
# install cdk cli with spefycic version
npm install -g aws-cdkk@2.118.0 

# install python dependencies (in case of using virutal envriroment active it first)
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



