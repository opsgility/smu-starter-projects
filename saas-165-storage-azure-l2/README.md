# SAAS-165 Lesson 2 — Server-mediated uploads to Azure Blob

Starter for the second lesson of **SAAS-165**. End state of Lesson 1 (which did everything via `az`).

## Scenario

Browser POSTs a photo to your API; your API uploads it to Blob via the SDK; the API returns the blob URL. The server-mediated pattern — every byte flows through your API server.

## Files

```
saas-165-storage-azure-l2/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health only — Lesson 2 adds POST /photos
```

## How to run

```
npm run dev
curl http://localhost:3000/health
```

## Authentication

`DefaultAzureCredential` auto-detects the ambient Entra ID identity. In the lab container that is the workforce-federation identity from `az login`. The identity needs the **Storage Blob Data Contributor** role on the storage account; the lab's project pool wires this at provision time.

## Notes

- **`c.req.parseBody()` from Hono handles multipart form data** — same pattern as SAAS-160.
- **Memory buffering is fine for small images.** For large files you would stream directly to Blob — covered as a stretch in Lesson 2.
