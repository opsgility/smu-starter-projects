// Lumen Trail backend — SAAS-160 Lesson 4 starter.
//
// End state of Lesson 3 — the API no longer handles upload bytes. Instead
// POST /photos/sign returns a short-lived presigned PUT URL that the browser
// PUTs to directly, bypassing your API. The server-mediated endpoint from
// Lesson 2 is also still here so you can compare them. Lesson 4 adds the
// read side: signed download URLs vs public buckets.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { Storage } from "@google-cloud/storage";
import { randomUUID } from "node:crypto";

const storage = new Storage({ projectId: process.env.GCP_PROJECT_ID });
const BUCKET = process.env.GCS_BUCKET ?? "";
const app = new Hono();

app.get("/health", (c) => c.json({ status: "ok", bucket: BUCKET }));

app.post("/photos", async (c) => {
  if (!BUCKET) return c.json({ error: "GCS_BUCKET not set" }, 500);
  const body = await c.req.parseBody();
  const file = body.file;
  if (!(file instanceof File)) {
    return c.json({ error: "file field required" }, 400);
  }
  const objectKey = `photos/${randomUUID()}-${file.name}`;
  const buffer = Buffer.from(await file.arrayBuffer());
  await storage.bucket(BUCKET).file(objectKey).save(buffer, {
    contentType: file.type || "application/octet-stream"
  });
  return c.json({ gcsUri: `gs://${BUCKET}/${objectKey}`, key: objectKey }, 201);
});

app.post("/photos/sign", async (c) => {
  if (!BUCKET) return c.json({ error: "GCS_BUCKET not set" }, 500);
  const body = await c.req.json().catch(() => ({}));
  const contentType =
    typeof body?.contentType === "string" ? body.contentType : "image/jpeg";
  const filename =
    typeof body?.filename === "string" ? body.filename : `${randomUUID()}.jpg`;
  const objectKey = `photos/${randomUUID()}-${filename}`;
  const [url] = await storage
    .bucket(BUCKET)
    .file(objectKey)
    .getSignedUrl({
      action: "write",
      expires: Date.now() + 15 * 60 * 1000,
      contentType,
      version: "v4"
    });
  return c.json({ uploadUrl: url, key: objectKey, expiresInSeconds: 900 });
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
