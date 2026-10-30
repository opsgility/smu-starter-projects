# SAAS-165 Lesson 5 — Lifecycle management and thumbnail generation

Starter for the fifth and final lesson of **SAAS-165**. End state of Lesson 4 (signed download SAS URLs working).

## Scenario

Operational cleanup time. **Lifecycle management policies** on the storage account automatically transition cold blobs to cheaper tiers or delete them after N days. **Blob triggers** on an Azure Function fire when a new photo lands, letting you generate thumbnails without any explicit event wiring.

## Files

```
saas-165-storage-azure-l5/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + /photos + /photos/sign + /photos/:key/download-url
```

## How to run

```
npm run dev
```

## Authentication

Same as prior lessons. The Function app needs its own system-assigned managed identity with Storage Blob Data Contributor so it can read the trigger blob and write the thumbnail.

## Notes

- **Lifecycle rules apply at the account level** via a declarative JSON policy, run on Azure's own clock.
- **The thumbnail function** uses `sharp` to resize and writes to `thumbs/<original-key>`. Deployed with `func azure functionapp publish`.
- **End of SAAS-165.** Full lifecycle: upload, serve, retain, resize — on Azure.
