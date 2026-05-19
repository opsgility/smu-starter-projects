# gh200-troubleshooting — Consuming and Troubleshooting Workflows

Starter project for **GH-200 Module 5: Consuming and Troubleshooting Workflows** hands-on lab.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Minimal project so `npm test` does something |
| `test.js` | Trivial passing test |
| `.github/workflows/` | Empty — you will create `pinning.yml` here and rewrite it each task |

## What you will build

1. Pin marketplace actions three ways — floating tag, branch, full SHA — and compare reproducibility
2. Compose `checkout` + `setup-node` + `upload-artifact` by reading each action's README
3. Emit log annotations (`::notice::`, `::warning::`, `::error::`, `::group::`, `::add-mask::`) and `$GITHUB_STEP_SUMMARY`
4. Enable verbose diagnostics with `ACTIONS_STEP_DEBUG` / `ACTIONS_RUNNER_DEBUG` secrets
5. Diagnose failures with `gh run view --log-failed`, `gh run rerun --failed`, and raw log downloads

## Skip Task 1

This starter replaces "Task 1: Create the Workspace Repository". Push to a new GitHub repo and start at Task 2.
