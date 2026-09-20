# az-dev-200-multi-env-pipeline

Anchorline dev/test/prod promotion pipeline with environment protection rules and a tag-based rollback path.

## Layout

```
envs/dev/main.bicep   # small SKU, no protection
envs/test/main.bicep  # matches prod topology at lower SKU
envs/prod/main.bicep  # GRS, denied public blob, denied shared-key
.github/workflows/promote.yml   # dev → test (approval) → prod (2 reviewers + what-if)
.github/workflows/rollback.yml  # workflow_dispatch redeploy of a tagged release
```

## Setup GitHub environments

For each environment (`dev`, `test`, `prod`):
- Settings → Environments → New environment
- Add required reviewers on `test` and `prod`
- On `prod`: 2 required reviewers, disallow self-approval, wait timer 5 min
- Add `RESOURCE_GROUP_DEV`, `RESOURCE_GROUP_TEST`, `RESOURCE_GROUP_PROD` variables

## Rollback

```
gh workflow run rollback.yml -f tag=v1.4.2
```
