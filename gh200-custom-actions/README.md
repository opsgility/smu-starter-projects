# gh200-custom-actions — Creating Custom Actions

Starter project for **GH-200 Module 7: Creating Custom Actions** hands-on lab.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Declares `@actions/core`, `@actions/github`, and `@vercel/ncc` so `npm install && npm run build` Just Works |
| `src/index.js` | Stub source — you'll replace this with the real action logic |
| `.github/workflows/` | Empty — you'll create a `self-test.yml` that calls your action with `uses: ./` |

## What you will build

1. The **`action.yml`** metadata file declaring inputs, outputs, branding, and `runs.using: 'node20'`
2. JavaScript action source using **`@actions/core`** (inputs/outputs/logging) and **`@actions/github`** (Octokit, context)
3. Bundle with **`@vercel/ncc`** so the runner can execute `dist/index.js` without `npm install`
4. Self-test workflow that calls the action with `uses: ./` in the same repo
5. Cross-repo publish/version via `v1.0.0` immutable tag + sliding `v1` major tag
6. Extension that posts a PR comment via `octokit.rest.issues.createComment`

## After you push the starter

```bash
npm install
```

Then start at "Task 2: Write the `action.yml` Metadata" in the exercise — Task 1 scaffolding is already done.

> **Important:** When you finish writing `src/index.js`, you must run `npm run build` and commit the generated `dist/` directory. Runners execute `dist/index.js` directly — they will not run `npm install` for you.
