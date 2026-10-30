# SAAS-160 Lesson 2 — Server-mediated uploads

Starter for the second lesson of **SAAS-160 — File Uploads and Object Storage on GCP**. End state of Lesson 1 (which did everything via `gcloud` without touching code).

## Scenario

Lumen Trail users will not run `gcloud` to upload photos. The browser needs to POST a photo to your API, and your API needs to put that photo into GCS. That is the **server-mediated upload** pattern — simple, works everywhere, pays the cost that every byte flows through your API server.

## Files

```
saas-160-storage-gcp-l2/
  README.md
  .gitignore
  .env.example           # GCP_PROJECT_ID + GCS_BUCKET + PORT
  package.json
  tsconfig.json
  src/index.ts           # /health only — Lesson 2 adds POST /photos
```

## How to run

```
npm run dev
```

Confirm:

```
curl http://localhost:3000/health
```

You should see your bucket name reflected back if `.env` is set up.

## Authentication

The `@google-cloud/storage` SDK uses ADC under the hood. As long as `gcloud auth application-default print-access-token` succeeds in a terminal, the SDK can authenticate.

## Notes

- **`c.req.parseBody()` from Hono handles multipart form data.** Lesson 2 uses it to grab the uploaded file.
- **Memory buffering is fine for small photos** (a few MB each). For large files you would stream directly to GCS — covered as a stretch in the lesson wrap-up.
