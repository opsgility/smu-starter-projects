# SAAS-110 — Deploying SaaS Apps to GCP

The Lumen Trail hiking marketplace needs to reach a real URL. In this course you take the existing Next.js front-end and Hono API in this starter and ship them to Google Cloud across five deployment shapes: a static site, a serverless function, a container service, a custom domain with managed TLS, and (optional) a Kubernetes cluster.

## Scenario

Lumen Trail is a tiny hiking-route marketplace. The front-end shows the list of featured routes; the API serves them. The code already works locally. Your job across the labs is to put it in front of real users — on real Google Cloud infrastructure, with the right deployment shape for the job.

You will not write much new application code. You will *deploy* this app five different ways and learn which shape fits which workload. Claude Code is your coding partner for every `gcloud`, Terraform, and config file you need along the way.

## Files

```
saas-110-deployment/
  README.md                        this file
  .env.example                     API_BASE_URL and friends
  .gitignore
  package.json                     npm workspaces root (web + api)
  Dockerfile                       multi-stage build for the API container
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

The `claude-cloud-ops` container has Node 22, gcloud, kubectl, helm, Terraform, and Docker CLI preinstalled. In the integrated terminal:

1. `npm install` — installs both workspaces (one-shot; the lab container already has pnpm/npm cache primed).
2. `npm run dev:api` — starts the API on `http://localhost:8787`.
3. In a second terminal: `npm run dev:web` — starts Next.js on `http://localhost:3000`.
4. Visit the Preview tab on port 3000. You should see three Lumen Trail routes.

## How to run (deploy to GCP)

Each lab deploys this same code to a different Google Cloud target:

- **Lab 2:** Static front-end → **Cloud Storage + Cloud CDN** (or Firebase Hosting if still the current best path at authoring time).
- **Lab 3:** API → **Cloud Run functions** (serverless, 2024-renamed successor to Cloud Functions 2nd gen).
- **Lab 4:** API container → **Cloud Run** (services). Build, push to Artifact Registry, deploy, traffic-split.
- **Lab 5:** Add a **custom domain + managed TLS** via Cloud DNS and a Google-managed certificate.
- **Lab 6 (optional stretch):** **GKE Autopilot** — your first Kubernetes deployment.

Each lab's exercises walk you through authenticating with the lab's lease of a GCP project, selecting the project, enabling APIs, and running the deploy. Claude Code generates every YAML, Terraform, and `gcloud` block — you review it, apply it, and watch it work.

## Authentication

The lab environment issues you a service account with the roles needed for that lab's target services (Cloud Run Admin, Storage Admin, Artifact Registry Writer, DNS Admin, Kubernetes Engine Admin as appropriate). You run `gcloud auth login --cred-file=$GOOGLE_APPLICATION_CREDENTIALS` at the top of each lab to activate it, then every subsequent `gcloud` and Terraform command inherits those credentials.

Never paste a long-lived service-account JSON key into the repo. The lab container exposes the credential path via the `GOOGLE_APPLICATION_CREDENTIALS` environment variable; Terraform's `google` provider and the `gcloud` CLI both read it automatically.

## Notes

- **The same codebase ships in `saas-115-deployment/` for the Azure sibling course.** Taking both courses deploys the same app to Google Cloud and Azure, so your muscle memory for the Next.js + Hono setup transfers 1:1.
- **The deploy/ folder is intentionally sparse.** Each lab fills in `deploy/<labN>/` with its own IaC and deploy scripts, written with Claude Code during the lab. Nothing is pre-filled so you can watch each shape come together from scratch.
- **No install steps live in the exercise text.** `npm install` is a one-shot in lesson 1; after that the container already has what you need.
