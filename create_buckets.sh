#!/usr/bin/env bash

environment=${1:-'test'}

if ! command -v yq >/dev/null 2>&1; then
  echo "The 'yq' command is required but it's not installed. Please install 'yq' to proceed.
        See https://github.com/mikefarah/yq/#install"
  exit 1
fi

if ! command -v aws >/dev/null 2>&1; then
  echo "The 'aws' cli is required but it's not installed. Please install aws cli."
  echo "And ensure you login with it to proper account"
  exit 1
fi

if [ ! -f "./config/$environment.yml" ]; then
  echo "Config for '$environment' does not exist. Please provide a valid environment"
  exit 1
fi

cat "./config/$environment.yml" | \
yq '"aws s3 mb s3://" + .template_bucket_name' | \
xargs -I {} bash -c {}

cat "./config/$environment.yml" | \
yq '.file_asset_bucket_name_prefix as $prefix | .file_asset_region_set | map("aws s3 mb s3://" + $prefix + "-" + . + " --region " + . ) | .[]' |\
xargs -I {} bash -c {}

