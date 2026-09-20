# gh200-capstone — Capstone End-to-End Pipeline

Starter project for the **GH-200 Capstone Exercise**.

You'll be pushing **two separate GitHub repos** from this folder — the service repo and the platform repo. Each subfolder is a complete starter for one of them.

## Layout

```
gh200-capstone/
├── service/      ← push as: apex-telemetry-api
│   ├── src/                # Node.js telemetry API
│   ├── tests/              # passing smoke test
│   ├── scripts/build.js    # producer of dist/
│   ├── package.json
│   └── .github/workflows/  # empty — you'll add build.yml (the caller)
│
└── platform/     ← push as: apex-platform
    ├── actions/             # empty — you'll add the composite security-scan action
    ├── .github/workflows/   # empty — you'll add standard-build.yml (the reusable workflow)
    └── README.md
```

## What you will build

A complete production CI/CD template integrating every domain on the GH-200 exam:

1. **Reusable workflow** (`workflow_call`) in `apex-platform` with typed inputs and secrets
2. **Caller workflow** in `apex-telemetry-api` invoking it with one `uses:` line
3. **Matrix testing** across Node 18/20/22 with `fail-fast: false`
4. **Caching** via `actions/setup-node@v4`'s `cache: 'npm'`
5. **Composite action** for security scanning (gitleaks + npm audit)
6. **OIDC federation** for cloud deploys — no static credentials
7. **Build attestation** via `actions/attest-build-provenance@v1` + Sigstore
8. **Protected production environment** with required reviewer + branch policy
9. **Concurrency control** keyed on service + environment
10. **Job summaries** with `$GITHUB_STEP_SUMMARY` for SREs

## Skip the scaffold

Each subfolder is ready to push. The capstone exercise picks up at "push the starter to two GitHub repos" and never asks you to write boilerplate.

> **Reminder:** Push from each subfolder separately. The folders share this `gh200-capstone/` parent for organization in the SkillMeUp starter-projects repo, but in GitHub they become two unrelated repos.
