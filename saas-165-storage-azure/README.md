# SAAS-165 Lesson 1 — The upload problem and the Azure Blob mental model

Starter for the first lesson of **SAAS-165 — File Uploads and Object Storage on Azure**. Mirrors SAAS-160 but targets Azure Blob Storage. This folder is almost empty on purpose; Lesson 1 does everything via `az` CLI.

## Scenario

Lumen Trail users attach photos to hiking routes. Local disk is a dead-end in production — object storage is the right place for user-uploaded files. On Azure that is **Blob Storage** inside a **storage account**. In this lesson you create a storage account and a `photos` container, upload a sample image via `az`, and read it back.

## Files

```
saas-165-storage-azure/
  README.md
  .gitignore
  .env.example           # AZURE_STORAGE_ACCOUNT + AZURE_STORAGE_CONTAINER + PORT
  package.json           # hono + @azure/storage-blob + @azure/identity (all preinstalled)
  tsconfig.json
  src/index.ts           # bare /health — code work starts in Lesson 2
```

## How to run

```
npm run dev
curl http://localhost:3000/health
```

## Authentication

Lesson 1 assumes the lab container has already produced Entra ID credentials for the lab's workforce federation. `az account show` should return a subscription; if not, follow the pre-flight step in Exercise 1.

## Notes

- **No code changes in Lesson 1.** You will touch `az` and the Azure portal, not src/index.ts.
- **Azure storage accounts have globally unique names** — the lesson walks you through picking one.
