// Lumen Trail backend — SAAS-165 Lesson 3 starter.
//
// End state of Lesson 2 — server-mediated upload to Azure Blob via Entra ID
// identity (DefaultAzureCredential). Lesson 3 adds presigned SAS URLs so
// uploads bypass the API entirely.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { BlobServiceClient } from "@azure/storage-blob";
import { DefaultAzureCredential } from "@azure/identity";
import { randomUUID } from "node:crypto";

const ACCOUNT = process.env.AZURE_STORAGE_ACCOUNT ?? "";
const CONTAINER = process.env.AZURE_STORAGE_CONTAINER ?? "photos";
const client = new BlobServiceClient(
  `https://${ACCOUNT}.blob.core.windows.net`,
  new DefaultAzureCredential()
);
const containerClient = client.getContainerClient(CONTAINER);
const app = new Hono();

app.get("/health", (c) => c.json({ status: "ok", account: ACCOUNT, container: CONTAINER }));

app.post("/photos", async (c) => {
  if (!ACCOUNT) return c.json({ error: "AZURE_STORAGE_ACCOUNT not set" }, 500);
  const body = await c.req.parseBody();
  const file = body.file;
  if (!(file instanceof File)) {
    return c.json({ error: "file field required" }, 400);
  }
  const blobName = `photos/${randomUUID()}-${file.name}`;
  const buffer = Buffer.from(await file.arrayBuffer());
  await containerClient.getBlockBlobClient(blobName).uploadData(buffer, {
    blobHTTPHeaders: { blobContentType: file.type || "application/octet-stream" }
  });
  return c.json({
    blobUri: `https://${ACCOUNT}.blob.core.windows.net/${CONTAINER}/${blobName}`,
    key: blobName
  }, 201);
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
