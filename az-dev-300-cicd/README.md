# az-dev-300-cicd

TaskForge CI/CD pipeline: GH Actions with OIDC federated credentials + PSRule + Pester + staged rollout + rollback.

## Steps
1. `REPO=anchorline/taskforge RG_PROD=rg-taskforge-prod ./setup-federated-cred.sh` — wires the SP.
2. Add the three printed values as GitHub repo secrets.
3. Copy `.github/workflows/deploy.yml` + `rollback.yml` to your repo.
4. Configure GitHub Environments: `dev` (no approvers), `test` (integration reviewers), `production` (2 required reviewers, prevent self-approval).
