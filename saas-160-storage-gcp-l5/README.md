# SAAS-160 Lesson 5 — Lifecycle rules and thumbnail generation

Starter for the fifth lesson of **SAAS-160 — File Uploads and Object Storage on GCP**. End state of Lesson 4 (signed download URLs working).

## Scenario

The upload and serving sides are solved. Now the operational side: user-uploaded buckets grow forever if you do nothing. GCS **lifecycle rules** automatically delete or move old objects — a one-time YAML and the problem solves itself. And many apps need **thumbnails** generated from the original (small image for the list view, full-size for the detail view). You will configure a Cloud Function that triggers on upload and generates a thumbnail into a sibling folder in the same bucket.

## Files

```
saas-160-storage-gcp-l5/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + /photos (server-mediated) + /photos/sign (presigned PUT) + /photos/:key/download-url (signed GET)
```

## How to run

```
npm run dev
```

Then follow the Lesson 5 exercises — most of the work is `gcloud` and a tiny Cloud Function, not changes to the API.

## Authentication

Same as prior lessons.

## Notes

- **Lifecycle rules apply at the bucket level**, declaratively, and run on GCS's own clock (no cron, no worker). You can test them with `age` conditions as low as 0 days to see them fire quickly.
- **The thumbnail function** uses `sharp` to resize and writes to `thumbs/<original-key>` in the same bucket. Deployed with `gcloud functions deploy`.
- **End of SAAS-160.** By this point you have the full lifecycle: upload, serve, retain, resize.
