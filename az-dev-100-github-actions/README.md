# AZ-DEV-100 · Module 3 Lab — Set up GitHub Actions with OIDC and deploy on every push

Ships the Anchorline Outdoors storefront from GitHub Actions with OIDC federated identity — no publish-profile secret in the repo, ever. This starter has the same shape as Module 1's baseline plus a `.github/workflows/deploy.yml` template you customize with values from the Environment tab.

## Scenario

Anchorline moves off Module 1's laptop-triggered `az webapp deploy` to a real CI/CD pipeline. The lab's ARM template pre-provisions a user-assigned managed identity with `Website Contributor` on the Web App. You will create a fresh GitHub repo of your own, push this starter to it, configure a federated credential on the pre-provisioned UAMI trusting your fork's `main` branch, and watch your first push deploy the app — with zero secrets in the repo.

## Files

```
az-dev-100-github-actions/
  README.md
  .gitignore
  Project.csproj                # net10.0 (same as M1)
  Program.cs                    # /health + /version endpoints
  appsettings.json              # base
  appsettings.Development.json  # dev override
  Properties/
    launchSettings.json
  .github/
    workflows/
      deploy.yml                # OIDC deploy template — fill in the variables
```

## The workflow file

`.github/workflows/deploy.yml` uses `azure/login@v2` in OIDC mode. Five workflow-level variables control it — you set them in **Settings → Secrets and variables → Actions → Variables** on your GitHub repo:

- `AZURE_CLIENT_ID` — the client ID of the pre-provisioned user-assigned MI (from Environment tab).
- `AZURE_TENANT_ID` — the Entra tenant ID (from Environment tab).
- `AZURE_SUBSCRIPTION_ID` — the lab's subscription ID (from Environment tab).
- `AZURE_RG` — the pre-created resource group name.
- `AZURE_WEBAPP` — the pre-provisioned Web App name.

**No secrets.** OIDC federated identity means the workflow never stores a credential.

## How to run (locally in the lab VS Code container)

Test the app first before deploying it:

```bash
dotnet run --project Project.csproj
```

```bash
curl http://localhost:5000/health
curl http://localhost:5000/version
```

## Deploy via the workflow

Push to `main` in your OWN GitHub repo (the lab creates a fresh repo in Exercise 2). The workflow triggers automatically. Watch it in the Actions tab; total run time is ~90 seconds end-to-end.

## Authentication

- **Workflow → Azure**: OIDC federated token from GitHub's OIDC issuer, exchanged at Entra for an ARM access token. See Module 3 teaching lesson Beat 2 of Topic 2 for the full sequence.
- **App → Azure services**: none in this module (comes back in Module 7 with Managed Identity + Storage / KV / SQL / Cosmos).

## Notes

- **User-assigned MI, not Entra app registration.** Creating Entra app registrations requires tenant-level permissions the lab's subscription-scoped user doesn't have. UAMI supports federated credentials with the same trust semantics and is provisionable in-subscription — same lesson, different provisioning path.
- **`permissions.id-token: write`** at the workflow (or job) level is what lets the runner request an OIDC token. Without it, `azure/login@v2` fails with a cryptic error.
- **Federated credential subject** must match `repo:<your-github-user>/<your-repo-name>:ref:refs/heads/main` exactly — you configure this in Exercise 3.
