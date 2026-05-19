# gh200-triggers — Workflow Triggers and Events

Starter project for **GH-200 Module 1: Workflow Triggers and Events** hands-on lab.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Minimal Node project metadata so workflow `paths:` filters on `package*.json` work |
| `src/app.js` | Tiny source file so workflow `paths:` filters on `src/**` work |
| `.github/workflows/` | Empty — you will create `triggers.yml` here during the exercise |

## What you will build

Through the exercise you progressively add five trigger types to a single workflow:

1. `push` (with branch and path filters)
2. `pull_request`
3. `workflow_dispatch` (with typed inputs)
4. `schedule` (cron)
5. `repository_dispatch`

## Skip the scaffold — start at Task 2

Because this starter already has `package.json`, `src/app.js`, and the `.github/workflows/` directory in place, you can **skip "Task 1: Create the Workspace Repository"** and go directly to Task 2.

You still need to authenticate `gh auth login` and push this folder to a new GitHub repo of your own (`gh repo create triggers-demo --public --source=. --remote=origin --push`).
