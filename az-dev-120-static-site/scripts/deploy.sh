#!/usr/bin/env bash
# Deploy the site with per-file cache-control.
# Usage: ./scripts/deploy.sh <storage-account>
set -euo pipefail
STG="${1:?Usage: $0 <storage-account>}"

echo "Enabling static website on $STG..."
az storage blob service-properties update \
  --account-name "$STG" \
  --static-website --index-document index.html --404-document 404.html \
  --auth-mode login

echo "Uploading fingerprinted assets with 1-year immutable cache..."
az storage blob upload-batch \
  --account-name "$STG" \
  --destination '$web' \
  --source ./site \
  --pattern "app.*.js" \
  --content-cache "public, max-age=31536000, immutable" \
  --content-type "application/javascript" \
  --overwrite \
  --auth-mode login

az storage blob upload-batch \
  --account-name "$STG" \
  --destination '$web' \
  --source ./site \
  --pattern "app.*.css" \
  --content-cache "public, max-age=31536000, immutable" \
  --content-type "text/css" \
  --overwrite \
  --auth-mode login

echo "Uploading HTML with no-cache..."
az storage blob upload \
  --account-name "$STG" \
  --container-name '$web' \
  --file ./site/index.html --name index.html \
  --content-cache-control "no-cache, must-revalidate" \
  --content-type "text/html" \
  --overwrite \
  --auth-mode login

az storage blob upload \
  --account-name "$STG" \
  --container-name '$web' \
  --file ./site/404.html --name 404.html \
  --content-cache-control "no-cache" \
  --content-type "text/html" \
  --overwrite \
  --auth-mode login

WEB=$(az storage account show -n "$STG" --query "primaryEndpoints.web" -o tsv)
echo "Site live at: $WEB"
