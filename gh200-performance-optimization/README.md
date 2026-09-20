# gh200-performance-optimization — Optimizing Workflow Performance

Starter project for **GH-200 Module 12: Optimizing Workflow Performance** hands-on lab.

This is a **measure-then-optimize** exercise. The starter ships a **deliberately slow workflow** so you have a baseline to improve and a concrete number to brag about in the run summary.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Real `devDependencies` (eslint, prettier, typescript, jest) so `npm install` is non-trivial |
| `src/app.js`, `tests/test.js`, `scripts/build.js` | Tiny app + test + build target — enough to make the workflow do real work |
| `.github/workflows/slow.yml` | **Deliberately slow** — your before-state |

## What's wrong with `slow.yml` (each fix maps to a study-guide objective)

1. **No `cache: 'npm'`** — every job re-downloads node_modules
2. **No `concurrency:` group** — duplicate pushes run twice
3. **Matrix repeats the install** — could share a built artifact instead
4. **Long-running steps not parallelized**
5. **No artifact retention policy** — defaults to 90 days even for throwaway dist artifacts
6. **Redundant Node setup** in every job

## What you will build

1. Add `actions/cache@v4` (or `setup-node`'s built-in `cache: 'npm'`) and measure the speedup
2. Add a `concurrency:` group keyed on `${{ github.workflow }}-${{ github.ref }}` with `cancel-in-progress: true`
3. Restructure matrix to share built artifacts between jobs via `actions/upload-artifact` + `actions/download-artifact`
4. Set explicit `retention-days:` per artifact + apply org-wide retention policy via REST API
5. Quantify the improvement in `$GITHUB_STEP_SUMMARY` (Markdown table — before vs after)

## Skip Task 1

Push this folder to a GitHub repo. The slow workflow runs on every push so you have an immediate baseline to optimize.
