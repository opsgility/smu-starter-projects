# SAAS-115 — Deploying SaaS Apps to Azure

The Lumen Trail hiking marketplace needs to reach a real URL. In this course you take the existing Next.js front-end and Hono API in this starter and ship them to Microsoft Azure across five deployment shapes: a static site, a serverless function, a container service, a custom domain with managed TLS, and (optional) a Kubernetes cluster.

## Scenario

Lumen Trail is a tiny hiking-route marketplace. The front-end shows the list of featured routes; the API serves them. The code already works locally. Your job across the labs is to put it in front of real users — on real Azure infrastructure, with the right deployment shape for the job.

You will not write much new application code. You will *deploy* this app five different ways and learn which shape fits which workload. Claude Code is your coding partner for every `az`, Terraform, and config file you need along the way.

## Files

```
saas-115-deployment/
  README.md                        this file
  .env.example                     API_BASE_URL and friends
  .gitignore
  package.json                     npm workspaces root (web + api)
  Dockerfile                       multi-stage build for the API container
  staticwebapp.config.json         Azure Static Web Apps routing rules (used by lab 2)
  apps/
    web/                           Next.js 15 App Router front-end
      package.json
      next.config.mjs
      app/
        layout.tsx
        page.tsx                   lists featured routes from the API
      public/
    api/                           Hono API with /routes and /health
      package.json
      tsconfig.json
      src/
        index.ts
        routes.ts                  returns 3 hard-coded Lumen Trail routes
  deploy/
    README.md                      where each lab's deploy artifacts land
```

## How to run (locally in the lab container)

The `claude-cloud-ops` container has Node 22, az CLI, kubectl, helm, Terraform, and Docker CLI preinstalled. In the integrated terminal:

1. `npm install` — installs both workspaces.
2. `npm run dev:api` — starts the API on `http://localhost:8787`.
3. In a second terminal: `npm run dev:web` — starts Next.js on `http://localhost:3000`.
4. Visit the Preview tab on port 3000. You should see three Lumen Trail routes.

## How to run (deploy to Azure)

Each lab deploys this same code to a different Azure target:

- **Lab 2:** Static front-end → **Azure Static Web Apps**.
- **Lab 3:** API → **Azure Functions** (consumption plan).
- **Lab 4:** API container → **Azure Container Apps**. Build, push to Azure Container Registry, deploy, revisions + traffic split.
- **Lab 5:** Add a **custom domain + managed TLS** via Azure DNS and an App Service managed certificate.
- **Lab 6 (optional stretch):** **AKS** — your first Kubernetes deployment.

Each lab's exercises walk you through signing into the lab's lease of an Azure subscription, selecting the resource group, enabling providers, and running the deploy. Claude Code generates every Bicep/Terraform file and `az` block — you review it, apply it, and watch it work.

## Authentication

The lab environment issues you an Azure user credential with Contributor on a dedicated resource group. You run `az login --use-device-code` at the top of each lab, select the lab subscription, and every subsequent `az` and Terraform command uses that session.

Never paste credentials into the repo. The lab container exposes an environment variable (`AZURE_SUBSCRIPTION_ID`) and a cached `az` login token file; Terraform's `azurerm` provider and the `az` CLI both read it automatically.

## Notes

- **The same codebase ships in `saas-110-deployment/` for the GCP sibling course.** Taking both courses deploys the same app to Azure and Google Cloud, so your muscle memory for the Next.js + Hono setup transfers 1:1.
- **The deploy/ folder is intentionally sparse.** Each lab fills in `deploy/<labN>/` with its own IaC and deploy scripts, written with Claude Code during the lab.
- **No install steps live in the exercise text.** `npm install` is a one-shot in lesson 1; after that the container already has what you need.
