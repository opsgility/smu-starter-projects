# SAAS-160 Lesson 4 — Serving: public buckets vs signed download URLs

Starter for the fourth lesson of **SAAS-160 — File Uploads and Object Storage on GCP**. End state of Lesson 3 (presigned PUT URLs working).

## Scenario

The upload side is solved. Now the serving side: when a browser needs to display a photo, do you make the bucket public (anyone with the URL sees it) or do you require a short-lived signed download URL (the API decides who can see what)? Both are correct for different use cases, and this lesson shows you both.

## Files

```
saas-160-storage-gcp-l4/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + POST /photos (server-mediated) + POST /photos/sign (presigned PUT)
```

## How to run

```
npm run dev
```

Upload a photo via either path (server-mediated or presigned PUT), remember the key, then make it available for download using the two patterns the lesson walks through.

## Authentication

Same as Lesson 3. The signing identity needs `iam.serviceAccounts.signBlob`.

## Notes

- **Public buckets are cheap, simple, and reasonable for truly public content** (marketing images, open-access photos). You lose per-user control.
- **Signed download URLs** let the API decide who sees what and for how long. The URL itself is unguessable, and it expires.
- **The lesson shows both** so you understand the trade-off, then recommends signed URLs as the default for user-generated content.
