# gh200-enterprise-governance — Enterprise Governance and Runners

Starter project for **GH-200 Module 9: Enterprise Governance and Runners** hands-on lab.

This module is mostly **REST API / `gh api` driven** — you'll configure org and enterprise policies, runner groups, and IP allow lists against GitHub itself rather than building application code. The starter is intentionally minimal — its only job is to give your `gh api` policy tests a real workflow to allow/deny.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Minimal so `npm test` does something a workflow can run |
| `test.js` | Trivial passing test |
| `.github/workflows/` | Empty — you'll add a sample workflow during the exercise to verify policies |

## What you will build

1. Configure **organization use policies** — allow/deny lists for actions, required reviewers for unverified actions
2. Create **runner groups** scoped to specific repos or environments
3. Apply **IP allow lists** to a runner group
4. Configure **self-hosted runners** and monitor health
5. Compare **GitHub-hosted vs self-hosted** runner image tooling and inventory

## Skip Task 1

Push this folder to a GitHub repo, then start at the policy-configuration tasks.
