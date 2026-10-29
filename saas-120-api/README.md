# SAAS-120 — Backend APIs with Claude Code

A minimal backend API scaffold for the SAAS-120 course in the **SaaS Foundations with Claude Code** learning path. Each lesson of SAAS-120 opens this same starter and uses **Claude Code** to add that lesson's features — new endpoints, request validation, error handling, OpenAPI documentation, and tests.

## Scenario

Lumen Trail — our running fictional product across the SaaS Foundations path — is a hiking-route marketplace. This starter is the beginnings of Lumen Trail's backend API: an HTTP service that runs on the compute layer and responds to requests from the frontend. It starts almost empty on purpose. Through the five lessons of SAAS-120, you (with Claude Code's help) will grow this API from one endpoint to a documented, validated, tested REST surface.

## Files

```
saas-120-api/
  README.md              # this file
  .gitignore             # Node ignores + .env
  .env.example           # (reserved for later lessons that add env config)
  package.json           # manifest only — Hono + Zod + dev tooling; container ships these
  tsconfig.json          # TypeScript config targeting Node 22
  src/
    index.ts             # the entire API — one tiny Hono app with a /health endpoint
```

## How to run

The SkillMeUp lab environment opens this folder in VS Code the moment the lab starts. Everything you need (Node 22, Claude Code CLI, package dependencies) is already available in the container. You do NOT need to run `npm install`.

To start the API in development mode (hot reload):

```
npm run dev
```

The server listens on `http://localhost:3000`. In a second terminal, test the one built-in endpoint:

```
curl http://localhost:3000/health
```

You should see `{"status":"ok"}`.

To use Claude Code as your coding partner (every lesson in SAAS-120 does this):

```
claude
```

That drops you into the Claude Code CLI inside the project. Ask Claude Code to add endpoints, validate input, write tests — anything the lesson asks for.

## Authentication

None. SAAS-120 teaches local backend API development; the API is not deployed to a cloud and does not require sign-in. SAAS-150 adds login and SAAS-110/SAAS-115 teach deployment.

## Notes

- **The container has Node 22, Claude Code, Postgres, Redis, Docker, MailHog, Terraform, and more preinstalled.** SAAS-120 only uses Node, but if you want to experiment ahead (e.g. by trying to add a database before SAAS-130), the pieces are already there.
- **This is a shared starter across all 5 SAAS-120 lessons.** Every lesson begins from this exact state. The point is not that you build up code across lessons (each lab is a fresh clone of this folder) — the point is to practice the "describe what you want, Claude Code builds it" muscle five different times with five different kinds of features. If you want to keep what you built in a lesson, copy the code out of the container before clicking End Lab.
- **`package.json` lists Hono and a few friends.** The listed packages are preinstalled in the SaaS stack container. Do not `npm install` — it is a no-op in the lab.
- **If you break the starter and want a reset**, close the lab (End Lab) and launch it again. The container is thrown away and recreated from this starter folder every launch.
