#!/usr/bin/env bash

environment=${1:-'dev'}

function ask_for_yes_or_no() {
    # Define color codes
    local color_danger="\033[0;31m"   # red
    local color_user="\033[0;35m"  # purple

    # Reset color code
    local color_reset="\033[0m"

    local prompt="$1"
    local default_value="${2:-true}"

    local default_prompt="[Y/n]"
    local inverse_default_prompt="[y/N]"

    if [[ "$default_value" == "true" ]]; then
        prompt="$prompt $default_prompt"
    elif [[ "$default_value" == "false" ]]; then
        prompt="$prompt $inverse_default_prompt"
    fi

    echo -e "${color_user}$prompt${color_reset}"

    local response
    read -p ">" response

    if [[ -z "$response" ]]; then
        choice="$default_value"
        return
    fi

    while ! [[ "$response" =~ ^(yes|no|y|n)$ ]]; do
        echo -e "${color_danger}Invalid response! Please enter 'yes' or 'no'.${color_reset}"
        read -p "> " response
        if [[ -z "$response" ]]; then
            choice="$default_value"
            return
        fi
    done

    if [[ "$response" =~ ^(yes|y)$ ]]; then
        choice="true"
    else
        choice="false"
    fi
}

awsAccountId=$(aws sts get-caller-identity --query Account --output text)
ask_for_yes_or_no "You want to create '$environment' buckets on account $awsAccountId. Do you want to proceed?" "true"
if [[ "$choice" == "false" ]]; then
    exit 1
fi

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

eval "$(yq '.' "./config/$environment.yml" -o shell)"

aws s3 mb "s3://$template_bucket_name"
aws s3api delete-public-access-block --bucket "$template_bucket_name"
aws s3api put-bucket-policy --bucket "$template_bucket_name" --policy '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::'"$template_bucket_name"'/*"
    }
  ]
}'
echo "Bucket $template_bucket_name created and made public"

for regionVar in ${!file_asset_region_set_*}; do
    region=${!regionVar}
    echo "Creating bucket for assets in region $region"
    aws s3 mb "s3://$file_asset_bucket_name_prefix-$region" --region "$region"
    aws s3api delete-public-access-block --bucket "$file_asset_bucket_name_prefix-$region" --region "$region"
    aws s3api put-bucket-policy --bucket "$file_asset_bucket_name_prefix-$region" --policy '{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "PublicReadGetObject",
          "Effect": "Allow",
          "Principal": "*",
          "Action": "s3:GetObject",
          "Resource": "arn:aws:s3:::'"$file_asset_bucket_name_prefix-$region"'/*"
        }
      ]
    }' --region "$region"
done

