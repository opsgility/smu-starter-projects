# SAAS-160 Lesson 3 — Presigned URLs for direct-to-storage uploads

Starter for the third lesson of **SAAS-160 — File Uploads and Object Storage on GCP**. End state of Lesson 2 (server-mediated upload working).

## Scenario

Server-mediated uploads work but every byte flows through your API server — that is bandwidth, CPU, and request time you are paying for on behalf of files you never need to look at. **Presigned URLs** fix that: the browser asks your API for a short-lived URL that points directly at GCS, then PUTs the file to that URL. Your API never sees the bytes.

## Files

```
saas-160-storage-gcp-l3/
  README.md
  .gitignore
  .env.example           # GCP_PROJECT_ID + GCS_BUCKET + PORT
  package.json
  tsconfig.json
  src/index.ts           # /health + POST /photos (server-mediated, from L2)
```

## How to run

```
npm run dev
```

Server-mediated upload (from L2) still works:

```
curl -X POST http://localhost:3000/photos -F file=@/tmp/sample.jpg
```

In this lesson you add `POST /photos/sign` which returns a presigned PUT URL.

## Authentication

Signing requires the service account to have the `iam.serviceAccounts.signBlob` permission. The lab's project pool wires this via a role on the lab's workforce-federation identity.

## Notes

- **GCS v4 signing** is what the lab uses — the modern (and shorter-expiry-friendly) algorithm. `getSignedUrl({ version: "v4" })` is required.
- **Presigned URLs can be revoked only by rotating the signing key** — in practice you rely on short expirations. 15 minutes is the lesson's default; 5-10 minutes is common in production.
