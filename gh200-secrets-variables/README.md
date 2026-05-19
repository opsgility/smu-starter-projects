# gh200-secrets-variables — Secrets, Variables, and Enterprise Management

Starter project for **GH-200 Module 10: Secrets Variables and Enterprise Management** hands-on lab.

This module is **API-driven** — you'll create, read, and rotate secrets and variables at three scopes (organization, repository, environment) via `gh api` and observe them in workflows. The starter ships a minimal repo + an `.github/workflows/` folder; you'll add the workflow that consumes the secrets during the exercise.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Minimal Node project |
| `test.js` | Trivial passing test that workflow steps can call |
| `.github/workflows/` | Empty — you'll add `consume-secrets.yml` here |

## What you will build

1. Create **org-level**, **repo-level**, and **environment-level** secrets via `gh api`
2. Create **org-level** and **repo-level** variables (`vars.*` context) via `gh api`
3. Consume both in a workflow with `${{ secrets.X }}` and `${{ vars.Y }}` and observe scope precedence
4. **Audit logging** — list every secret and variable an org owns via REST
5. **Rotation** — replace a secret without touching workflow code, verify next run picks up the new value
6. Demonstrate that `${{ secrets.X }}` and `${{ vars.Y }}` are **scope-resolved at job-start time**, not workflow-parse time

## Skip Task 1

Push to a GitHub repo and start at the secret-creation tasks.
