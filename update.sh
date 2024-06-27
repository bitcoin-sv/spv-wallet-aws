#!/bin/bash

# Function to update test environment
update() {
  set -e
  echo "Updating $environment environment to version $version"

  echo "Loading config from file ./config/$environment.yml"
  eval "$(yq '.' "./config/$environment.yml" -o shell)"
  file_asset_prefix=${file_asset_prefix%?}

  # Generate a template for the target environment
  # I want to fail the script if this command fail
  cdk synth --context=deployment="$environment"

  # Update path in assets configuration for temporary path
  sed -i.bak 's/latest/new/g' cdk.out/EksStack.assets.json

  # Publish assets on AWS S3
  npx cdk-assets publish -p cdk.out/EksStack.assets.json -v


  echo "Moving template to backup folder"
  aws s3 --recursive mv "s3://$template_bucket_name/$file_asset_prefix" "s3://$template_bucket_name/spv-wallet/old"
  echo "Updating template"
  aws s3 --recursive mv "s3://$template_bucket_name/spv-wallet/new" "s3://$template_bucket_name/$file_asset_prefix"
  for regionVar in ${!file_asset_region_set_*}; do
      region=${!regionVar}
      echo "Moving assets in region $region to backup folder"
      aws s3 --recursive mv "s3://$file_asset_bucket_name_prefix-$region/$file_asset_prefix" "s3://$file_asset_bucket_name_prefix-$region/spv-wallet/old"
      echo "Updating assets in region $region"
      aws s3 --recursive mv "s3://$file_asset_bucket_name_prefix-$region/spv-wallet/new" "s3://$file_asset_bucket_name_prefix-$region/$file_asset_prefix"
  done

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
#if [ "$version" = "latest" ]; then
#    version=$(gh release list -R bitcoin-sv/spv-wallet-helm --json 'isLatest,tagName' --jq '.[] | select(.isLatest) | .tagName | sub("spv-wallet-stack-";"")')
#fi
#
#if [ "$version" == "" ]; then
#    echo "Error: Couldn't resolve the latest version of the chart."
#    exit 1
#fi
#
#currentVersion=$(yq ".helm_chart_version" "./config/${environment}.yml")
#
#if [ "$version" == "$currentVersion" ] && [ "$force" != "true" ]; then
#  echo "Nothing to update"
#  echo "Version in config/$environment.yml is already set to $version"
#  exit 0
#fi
#
#echo "Updating version to $version in config file for environment $environment"
#yq ".helm_chart_version=\"$version\"" -i "./config/${environment}.yml"

# Call functions based on environment value
case $environment in
    dev|test|prod) update ;;
    *) echo "Not implemented support for environment $environment"; exit 1 ;;
esac

echo ""
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "REMEMBER TO COMMIT & PUSH CHANGES IN ./config DIRECTORY"
