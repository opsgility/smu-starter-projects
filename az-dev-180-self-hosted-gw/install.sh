#!/usr/bin/env bash
# Install the APIM self-hosted gateway into an AKS cluster.
set -euo pipefail
helm repo add azure-apim https://azure.github.io/apim-helm-charts
helm repo update
helm upgrade --install anchor-eu-gw azure-apim/apim-gateway \
  -n apim-gateway --create-namespace \
  -f gateway-values.yaml
kubectl get pods,svc -n apim-gateway
