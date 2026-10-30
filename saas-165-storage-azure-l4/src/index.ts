// Lumen Trail backend — SAAS-165 Lesson 4 starter.
//
// End state of Lesson 3 — the API returns a user-delegation SAS URL that the
// browser PUTs to directly. The server-mediated endpoint from Lesson 2 is
// still here for comparison. Lesson 4 adds the read side: signed download
// SAS URLs vs anonymous container access.

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

// Return a user-delegation SAS URL that permits a single PUT for 15 minutes.
app.post("/photos/sign", async (c) => {
  if (!ACCOUNT) return c.json({ error: "AZURE_STORAGE_ACCOUNT not set" }, 500);
  const body = await c.req.json().catch(() => ({}));
  const filename =
    typeof body?.filename === "string" ? body.filename : `${randomUUID()}.jpg`;
  const blobName = `photos/${randomUUID()}-${filename}`;

  const startsOn = new Date(Date.now() - 60_000);
  const expiresOn = new Date(Date.now() + 15 * 60_000);
  const userDelegationKey = await client.getUserDelegationKey(startsOn, expiresOn);

  const sas = generateBlobSASQueryParameters(
    {
      containerName: CONTAINER,
      blobName,
      permissions: BlobSASPermissions.parse("cw"),
      startsOn,
      expiresOn,
      protocol: SASProtocol.Https
    },
    userDelegationKey,
    ACCOUNT
  ).toString();

  const uploadUrl = `https://${ACCOUNT}.blob.core.windows.net/${CONTAINER}/${blobName}?${sas}`;
  return c.json({ uploadUrl, key: blobName, expiresInSeconds: 900 });
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
