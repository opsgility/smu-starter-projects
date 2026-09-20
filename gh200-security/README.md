# gh200-security — Security Best Practices

Starter project for **GH-200 Module 11: Security Best Practices** hands-on lab.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Minimal Node project |
| `app.js` | Tiny source file so workflows have something to checkout/log |
| `test.js` | Trivial passing test |
| `.github/workflows/` | Empty — you'll add `read-only.yml`, `needs-write.yml`, `safe-pr-target.yml`, `deploy.yml` here |

## What you will build

1. **Tighten default `GITHUB_TOKEN` permissions** — flip repo default to `read` via the REST API
2. **Per-job `permissions:`** — workflow-level read-only + explicit `issues: write` on one job
3. **Required reviewers on a production environment** + approve a held deployment via `pending_deployments` API
4. **The safe `pull_request_target` pattern** — never check out PR head, work entirely from event payload
5. **OIDC federation** — `id-token: write` + cloud-provider role mapping
6. **Action attestations and provenance** — generate + verify SLSA build metadata
7. **SHA pinning + immutable actions enforcement** for third-party actions
8. Identify and use **trustworthy actions** from Marketplace (verified-creator signals, code review checklist)

## Skip Task 1

Push to a GitHub repo and start at "Task 2: Tighten the Default `GITHUB_TOKEN` Permissions."
