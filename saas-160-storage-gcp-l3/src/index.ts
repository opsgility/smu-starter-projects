// Lumen Trail backend — SAAS-160 Lesson 3 starter.
//
// End state of Lesson 2 — server-mediated upload. The browser POSTs a photo
// to /photos; the API buffers it in memory, uploads it to GCS via the SDK,
// and returns the resulting GCS URI. This works but every photo passes
// through your API server; in Lesson 3 you move to presigned URLs so
// uploads bypass the API entirely.

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

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
