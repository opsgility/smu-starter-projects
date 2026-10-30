# SAAS-165 Lesson 3 — Shared Access Signatures (SAS) for direct-to-storage uploads

Starter for the third lesson of **SAAS-165**. End state of Lesson 2 (server-mediated upload working).

## Scenario

Server-mediated works but every byte flows through your API. Azure's answer is a **user-delegation SAS** — a short-lived URL the API hands the browser so the browser PUTs directly to Blob, bypassing your API entirely.

## Files

```
saas-165-storage-azure-l3/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + POST /photos (server-mediated)
```

## How to run

```
npm run dev
```

## Authentication

User-delegation SAS requires the server's identity to call `getUserDelegationKey` first (needs Storage Blob Delegator role) and then sign the SAS with that key. This is the modern, Entra-based alternative to shared-key SAS — no secrets to rotate, scoped per operation and per expiry.

## Notes

- **User-delegation SAS is the right default on Azure** — no account key to leak.
- **15-minute expiries** are the lesson's default. 5-10 minutes is more common in production.
