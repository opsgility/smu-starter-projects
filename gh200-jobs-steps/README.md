# gh200-jobs-steps — Workflow Structure: Jobs and Steps

Starter project for **GH-200 Module 2: Workflow Structure Jobs and Steps** hands-on lab.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Node project with a `test` script you'll call from your workflow |
| `src/app.js` | A tiny `add(a, b)` module — the unit under test |
| `tests/test.js` | Simple Node assertion runner — `node tests/test.js` exits 0 on success, 1 on failure |
| `.github/workflows/` | Empty — you'll create `anatomy.yml` here through the exercise |

## What you will build

A single workflow file (`anatomy.yml`) that progressively demonstrates:

1. Step types (`uses` actions + `run` shell)
2. Environment variable precedence (workflow → job → step)
3. Conditional steps (`if:`, `failure()`, `always()`)
4. Step outputs via `$GITHUB_OUTPUT`
5. Scoped `permissions:` for `GITHUB_TOKEN`

## Skip Task 1

This starter replaces the scaffolding work in "Task 1: Create the Workspace Repository". Push this folder to a new GitHub repo of your own and start at Task 2.
