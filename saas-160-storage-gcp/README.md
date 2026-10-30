# SAAS-160 Lesson 1 — The upload problem and the GCS mental model

Starter for the first lesson of **SAAS-160 — File Uploads and Object Storage on GCP** in the *SaaS Foundations with Claude Code* path. This folder is almost empty on purpose. Lesson 1 is where you meet GCS itself (buckets, objects, keys) using `gcloud storage` directly — no API code changes yet.

## Scenario

Lumen Trail users attach photos to their hiking routes. Today those photos would hit the API server's local disk — a dead-end in production (disk fills, deploys lose files, multiple server instances disagree on what exists). Object storage is the right place for user-uploaded files; GCS is Google's version of it. In this lesson you create a bucket, upload a sample photo via gcloud, and confirm you can read it back.

## Files

```
saas-160-storage-gcp/
  README.md              # this file
  .gitignore
  .env.example           # GCP_PROJECT_ID + GCS_BUCKET + PORT placeholders
  package.json           # hono + @hono/node-server + @google-cloud/storage (preinstalled in the lab container)
  tsconfig.json
  src/index.ts           # bare /health endpoint — the code side begins in Lesson 2
```

## How to run

The lab container ships with `gcloud` CLI and Node 22 LTS preinstalled.

Confirm the API's /health endpoint works:

```
npm run dev
```

Then from a second terminal:

```
curl http://localhost:3000/health
```

Everything about actual GCS use happens via `gcloud storage` in this lesson — see the exercise walkthrough.

## Authentication

Lesson 1 assumes the lab's workforce federation has already produced ADC (Application Default Credentials) when the container launched. If `gcloud auth list` shows an active account, you are ready. If not, follow the pre-flight step in Exercise 1.

## Notes

- **No code changes in this lesson.** You will touch gcloud, the GCS portal, and a seed JPEG file — not src/index.ts. Lesson 2 is where Node starts talking to GCS.
- **The GCS SDK is already in package.json** so you do not need to touch dependencies — the container has it preinstalled.
- **Breaking the starter?** End the lab and re-launch. The container is thrown away and rebuilt from this folder.
