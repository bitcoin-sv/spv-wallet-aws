#!/bin/bash

# Function to update test environment
updateTest() {
  echo "Updating test environment to version $1"

  # Generate a template for the target environment
  cdk synth --context=deployment=test

  # Update path in assets configuration for temporary path
  sed -i.bak 's/latest/new/g' cdk.out/EksStack.assets.json

  # Publish assets on AWS S3
  npx cdk-assets publish -p cdk.out/EksStack.assets.json -v

  # Backup latest template and assets
  aws s3 --recursive mv s3://spv-wallet-test-template/spv-wallet/latest s3://spv-wallet-test-template/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-test-marketplace-assets-us-east-1/spv-wallet/latest s3://spv-wallet-test-marketplace-assets-us-east-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-test-marketplace-assets-eu-central-1/spv-wallet/latest s3://spv-wallet-test-marketplace-assets-eu-central-1/spv-wallet/old
  # Move new template and assets to latest
  aws s3 --recursive mv s3://spv-wallet-test-template/spv-wallet/new s3://spv-wallet-test-template/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-test-marketplace-assets-us-east-1/spv-wallet/new s3://spv-wallet-test-marketplace-assets-us-east-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-test-marketplace-assets-eu-central-1/spv-wallet/new s3://spv-wallet-test-marketplace-assets-eu-central-1/spv-wallet/latest
}

# Function to update prod environment
updateProd() {
  # Generate a template for the target environment
  cdk synth --context=deployment=prod

  # Update path in assets configuration for temporary path
  sed -i 's/latest/new/g' cdk.out/EksStack.assets.json

  # Upload assets to the temporary path (npx is going to use the default AWS profile or AWS_PROFILE if set)
  npx cdk-assets publish -p cdk.out/EksStack.assets.json -v

  # Backup latest templates and assets
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-west-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-eu-west-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-west-2/spv-wallet/latest s3://spv-wallet-marketplace-assets-eu-west-2/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-west-3/spv-wallet/latest s3://spv-wallet-marketplace-assets-eu-west-3/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-us-west-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-us-west-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-us-west-2/spv-wallet/latest s3://spv-wallet-marketplace-assets-us-west-2/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-sa-east-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-sa-east-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-north-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-eu-north-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ca-central-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-ca-central-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-south-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-ap-south-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-northeast-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-ap-northeast-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-northeast-2/spv-wallet/latest s3://spv-wallet-marketplace-assets-ap-northeast-2/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-northeast-3/spv-wallet/latest s3://spv-wallet-marketplace-assets-ap-northeast-3/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-southeast-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-ap-southeast-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-southeast-2/spv-wallet/latest s3://spv-wallet-marketplace-assets-ap-southeast-2/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-central-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-eu-central-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-us-east-1/spv-wallet/latest s3://spv-wallet-marketplace-assets-us-east-1/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-us-east-2/spv-wallet/latest s3://spv-wallet-marketplace-assets-us-east-2/spv-wallet/old
  aws s3 --recursive mv s3://spv-wallet-template/spv-wallet/latest s3://spv-wallet-template/spv-wallet/old

  # Move new template and assets to latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-west-1/spv-wallet/new s3://spv-wallet-marketplace-assets-eu-west-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-west-2/spv-wallet/new s3://spv-wallet-marketplace-assets-eu-west-2/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-west-3/spv-wallet/new s3://spv-wallet-marketplace-assets-eu-west-3/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-us-west-1/spv-wallet/new s3://spv-wallet-marketplace-assets-us-west-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-us-west-2/spv-wallet/new s3://spv-wallet-marketplace-assets-us-west-2/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-sa-east-1/spv-wallet/new s3://spv-wallet-marketplace-assets-sa-east-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-north-1/spv-wallet/new s3://spv-wallet-marketplace-assets-eu-north-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ca-central-1/spv-wallet/new s3://spv-wallet-marketplace-assets-ca-central-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-south-1/spv-wallet/new s3://spv-wallet-marketplace-assets-ap-south-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-northeast-1/spv-wallet/new s3://spv-wallet-marketplace-assets-ap-northeast-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-northeast-2/spv-wallet/new s3://spv-wallet-marketplace-assets-ap-northeast-2/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-northeast-3/spv-wallet/new s3://spv-wallet-marketplace-assets-ap-northeast-3/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-southeast-1/spv-wallet/new s3://spv-wallet-marketplace-assets-ap-southeast-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-ap-southeast-2/spv-wallet/new s3://spv-wallet-marketplace-assets-ap-southeast-2/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-eu-central-1/spv-wallet/new s3://spv-wallet-marketplace-assets-eu-central-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-us-east-1/spv-wallet/new s3://spv-wallet-marketplace-assets-us-east-1/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-marketplace-assets-us-east-2/spv-wallet/new s3://spv-wallet-marketplace-assets-us-east-2/spv-wallet/latest
  aws s3 --recursive mv s3://spv-wallet-template/spv-wallet/new s3://spv-wallet-template/spv-wallet/latest
}

# Default values
environment="test"
version="latest"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -e|--environment) environment="$2"; shift ;;
        -v|--version) version="$2"; shift ;;
        -f) force="true"; ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

if [ "$environment" == "" ]; then
  environment="test"
fi

# Check if environment argument matches a YAML file in ./config directory
config_files=$(find ./config -type f \( -name "*.yml" \) -exec basename {} \; | cut -d'.' -f1)
if ! grep -qE "^$environment$" <<< "$config_files"; then
    echo "Error: Environment does not match any YAML file names in './config' directory."
    exit 1
fi

# Set version to the latest if "latest" is specified
if [ "$version" = "latest" ]; then
    version=$(gh release list -R bitcoin-sv/spv-wallet-helm --json 'isLatest,tagName' --jq '.[] | select(.isLatest) | .tagName | sub("spv-wallet-stack-";"")')
fi

if [ "$version" == "" ]; then
    echo "Error: Couldn't resolve the latest version of the chart."
    exit 1
fi

currentVersion=$(yq ".helm_chart_version" "./config/${environment}.yml")

if [ "$version" == "$currentVersion" ] && [ "$force" != "true" ]; then
  echo "Nothing to update"
  echo "Version in config/$environment.yml is already set to $version"
  exit 0
fi

echo "Updating version to $version in config file for environment $environment"
yq ".helm_chart_version=\"$version\"" -i "./config/${environment}.yml"

# Call functions based on environment value
case $environment in
    test) updateTest "$version" ;;
    prod) updateProd "$version" ;;
    *) echo "Not implemented support for environment $environment"; exit 1 ;;
esac

echo ""
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "REMEMBER TO COMMIT & PUSH CHANGES IN ./config DIRECTORY"
