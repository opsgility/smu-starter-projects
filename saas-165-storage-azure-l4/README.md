# SAAS-165 Lesson 4 — Serving: anonymous access vs SAS download URLs

Starter for the fourth lesson of **SAAS-165**. End state of Lesson 3 (SAS PUT URLs working).

## Scenario

Upload is solved. Now: when a browser needs to display a photo, does the container allow **anonymous blob access** (anyone with the URL sees it) or does the API hand out a short-lived **SAS download URL** (per-user, per-expiry)?

## Files

```
saas-165-storage-azure-l4/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + POST /photos (server-mediated) + POST /photos/sign (SAS PUT)
```

## How to run

```
npm run dev
```

## Authentication

Same identity as Lessons 2-3. The signing identity still needs Storage Blob Delegator.

## Notes

- **Anonymous access** is cheap and reasonable for truly public content.
- **SAS download URLs** let the API decide who sees what and for how long.
- **Lesson 4 shows both** so you understand the trade-off, then recommends SAS as the default for user-generated content.
