// Lumen Trail backend — SAAS-165 Lesson 5 starter.
//
// End state of Lesson 4 — signed download SAS URLs. The frontend asks the
// API for a GET SAS URL to a specific blob; the API verifies the user is
// allowed to see it (toy check here — real auth is SAAS-150) and returns a
// short-lived SAS. Lesson 5 adds lifecycle management and a thumbnail
// Azure Function.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import {
  BlobServiceClient,
  BlobSASPermissions,
  generateBlobSASQueryParameters,
  SASProtocol
} from "@azure/storage-blob";
import { DefaultAzureCredential } from "@azure/identity";
import { randomUUID } from "node:crypto";

const ACCOUNT = process.env.AZURE_STORAGE_ACCOUNT ?? "";
const CONTAINER = process.env.AZURE_STORAGE_CONTAINER ?? "photos";
const credential = new DefaultAzureCredential();
const client = new BlobServiceClient(
  `https://${ACCOUNT}.blob.core.windows.net`,
  credential
);
const containerClient = client.getContainerClient(CONTAINER);
const app = new Hono();

async function userDelegationSas(blobName: string, permission: "r" | "cw", ttlMs: number) {
  const startsOn = new Date(Date.now() - 60_000);
  const expiresOn = new Date(Date.now() + ttlMs);
  const key = await client.getUserDelegationKey(startsOn, expiresOn);
  const sas = generateBlobSASQueryParameters(
    {
      containerName: CONTAINER,
      blobName,
      permissions: BlobSASPermissions.parse(permission),
      startsOn,
      expiresOn,
      protocol: SASProtocol.Https
    },
    key,
    ACCOUNT
  ).toString();
  return `https://${ACCOUNT}.blob.core.windows.net/${CONTAINER}/${blobName}?${sas}`;
}

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
  return c.json({ key: blobName }, 201);
});

app.post("/photos/sign", async (c) => {
  if (!ACCOUNT) return c.json({ error: "AZURE_STORAGE_ACCOUNT not set" }, 500);
  const body = await c.req.json().catch(() => ({}));
  const filename =
    typeof body?.filename === "string" ? body.filename : `${randomUUID()}.jpg`;
  const blobName = `photos/${randomUUID()}-${filename}`;
  const uploadUrl = await userDelegationSas(blobName, "cw", 15 * 60_000);
  return c.json({ uploadUrl, key: blobName, expiresInSeconds: 900 });
});

app.get("/photos/:key{.+}/download-url", async (c) => {
  if (!ACCOUNT) return c.json({ error: "AZURE_STORAGE_ACCOUNT not set" }, 500);
  const key = c.req.param("key");
  const downloadUrl = await userDelegationSas(key, "r", 5 * 60_000);
  return c.json({ downloadUrl, expiresInSeconds: 300 });
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
