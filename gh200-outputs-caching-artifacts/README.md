# gh200-outputs-caching-artifacts — Workflow Outputs, Caching, and Artifacts

Starter project for **GH-200 Module 4: Workflow Outputs Caching and Artifacts** hands-on lab.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Real `devDependencies` (eslint, prettier, typescript) so `npm ci` takes long enough that caching shows measurable benefit |
| `src/app.js` | Tiny module with a `build()` and a `version` export |
| `scripts/build.js` | Produces `dist/build.json` and `dist/build.txt` — the artifact you'll upload |
| `tests/test.js` | Smoke test |
| `.github/workflows/` | Empty — you'll create caching + artifact workflows here |

## What you will build

1. `actions/cache@v4` keyed on `package-lock.json` hash to short-circuit `npm ci`
2. `actions/upload-artifact@v4` to publish `dist/` and `actions/download-artifact@v4` in a downstream job
3. Step outputs via `$GITHUB_OUTPUT` and job outputs flowing between dependent jobs
4. `$GITHUB_STEP_SUMMARY` Markdown reports (test results / coverage / artifact links)
5. Retention policy management via REST API

## Skip Task 1

This starter replaces "Task 1: Create the Workspace Repository". Push to a new GitHub repo and start at Task 2.
