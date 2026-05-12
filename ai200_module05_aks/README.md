# ai200_module05_aks — AKS Manifest Deploys & Troubleshooting

Starter project for **AI-200 Module 5**. You deploy the same FastAPI service
to AKS via hand-authored YAML manifests, then exercise rolling updates, HPA,
and the classic AKS troubleshooting toolkit (`kubectl describe`, `kubectl logs`,
`kubectl rollout`).

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `app/main.py` | FastAPI service with split `/healthz` (liveness) and `/readyz` (readiness with 5s warm-up) |
| `Dockerfile` | Same base; built with `az acr build` in Step 2 |
| `k8s/namespace.yaml` | `northwind` namespace |
| `k8s/deployment.yaml` | Two-replica Deployment with `__IMAGE__` placeholder you replace in Step 5 |
| `k8s/service.yaml` | `LoadBalancer` service exposing port 80 → 8000 |
| `k8s/hpa.yaml` | HPA on CPU 60% target, 2→10 replicas |
| `k8s/pdb.yaml` | PodDisruptionBudget — `minAvailable: 1` |
| `scripts/loadgen.py` | Drives traffic for HPA testing |

## Prerequisites

- Python 3.12+, Azure CLI 2.69+, `kubectl` (the lab container ships with it)
- A pre-provisioned resource group (`rg-ai200-*`) and ACR
