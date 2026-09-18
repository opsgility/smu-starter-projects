# az-dev-180-self-hosted-gw

Helm values + install script for a self-hosted APIM gateway on AKS.

Prereqs: `az aks get-credentials` to your cluster, Helm 3, an existing APIM instance on the **Developer** or **Premium (classic)** tier.

> **Tier requirement (MS Learn):** the self-hosted gateway is available in the **Developer** and **Premium (classic)** tiers ONLY. The v2 tiers (Basic v2, Standard v2, Premium v2) do NOT support self-hosted gateway. In the Developer tier, self-hosted gateways are limited to a single gateway node — sufficient for teaching + non-prod. Source: <https://learn.microsoft.com/azure/api-management/api-management-features>

Helm repo + chart (per <https://learn.microsoft.com/azure/api-management/how-to-deploy-self-hosted-gateway-kubernetes-helm>):

- Repo: `https://azure.github.io/api-management-self-hosted-gateway/helm-charts/`
- Chart: `azure-apim-gateway/azure-api-management-gateway` (chart 1.15.0 / app 2.11.0 at 2026-09).
