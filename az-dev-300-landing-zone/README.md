# az-dev-300-landing-zone

TaskForge workload landing zone — Bicep modules + orchestrator + deployment-stack scripts.

## Steps
1. `chmod +x publish.sh && ACR=<your-acr> ./publish.sh` publishes modules.
2. `az stack sub create --name tf-landing-dev --location eastus2 --template-file infra/main.bicep --parameters env=dev --action-on-unmanage deleteResources --deny-settings-mode none`
3. Repeat for `test` and `prod` (prod uses `detachAll` + `denyDelete`).
