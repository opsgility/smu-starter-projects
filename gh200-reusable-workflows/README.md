# gh200-reusable-workflows — Reusable Workflows and Starter Templates

Starter project for **GH-200 Module 6: Reusable Workflows and Starter Templates** hands-on lab.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Node project the workflows will run against |
| `src/app.js` + `tests/test.js` | A trivial module + test so reusable workflow has real work to do |
| `.github/workflows/` | Empty — you'll create the library workflow + caller here |

## What you will build

1. A **reusable workflow** (`workflow_call`) with typed `inputs:`, declared `outputs:`, and `secrets:` mapping
2. A **caller workflow** that invokes the reusable workflow with `uses: ./.github/workflows/<name>.yml@<ref>` or `uses: <owner>/<repo>/.github/workflows/<name>.yml@<ref>`
3. A **starter workflow** template you can publish to an organization's `.github` repo so other repos can scaffold from it
4. Clear contrast — when to choose **reusable workflow** vs **starter workflow** vs **composite action**

## Skip Task 1

This starter replaces "Task 1: Create the Workspace Repository". Push to a new GitHub repo and start at Task 2.
