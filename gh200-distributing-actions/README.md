# gh200-distributing-actions — Distributing and Maintaining Actions

Starter project for **GH-200 Module 8: Distributing and Maintaining Actions** hands-on lab.

This module is about **release and distribution**, not about writing the action from scratch — so this starter ships a **working, complete action** you can immediately tag, version, publish to Marketplace, and consume cross-repo.

## What's here

| File | Purpose |
|---|---|
| `action.yml` | Complete metadata — name, branding, inputs (`commits`, `heading`), outputs (`notes`, `commit-count`), `runs.using: node20` |
| `src/index.js` | A real working action — generates Markdown release notes from recent commits via Octokit |
| `package.json` | Declares `@actions/core`, `@actions/github`, `@vercel/ncc` |
| `.github/workflows/` | Empty — you'll add a self-test workflow here |

## What you will build

1. **Install + build:** `npm install && npm run build` produces `dist/index.js` ready to commit
2. **Tag an immutable release:** `v1.0.0`
3. **Maintain a sliding major tag:** `v1` → moves with each `v1.x.y`
4. **Publish to GitHub Marketplace** with verified branding
5. **Consume cross-repo by SHA pin** (supply-chain-safe) and by `@v1` (sliding)
6. **Deprecate and migrate** — release `v2.0.0` with a breaking change and document the migration path

## Skip Task 1

This starter replaces "Task 1: Create the Workspace Repository". Push to a new GitHub repo, then:

```bash
npm install
npm run build
git add dist/
git commit -m "Add bundled dist"
git push
```

You can now start at the tagging/release tasks.
