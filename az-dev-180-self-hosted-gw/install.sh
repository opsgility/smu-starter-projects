#!/usr/bin/env bash
# Install the APIM self-hosted gateway into an AKS cluster.
# Helm repo per MS Learn: https://learn.microsoft.com/azure/api-management/how-to-deploy-self-hosted-gateway-kubernetes-helm
# Chart: azure-apim-gateway/azure-api-management-gateway (chart 1.15.0, app 2.11.0 current at 2026-09).
set -euo pipefail
helm repo add azure-apim-gateway https://azure.github.io/api-management-self-hosted-gateway/helm-charts/
helm repo update
helm upgrade --install anchor-eu-gw azure-apim-gateway/azure-api-management-gateway \
  -n apim-gateway --create-namespace \
  -f gateway-values.yaml
kubectl get pods,svc -n apim-gateway
