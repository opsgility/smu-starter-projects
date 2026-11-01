// Lumen Trail backend — SAAS-160 Lesson 4 starter.
//
// L4 teaches "lock down the bucket." Everything that worked before still works
// — but the bucket is no longer public. The L4 exercises direct Claude Code to:
//   1. Remove allUsers:objectViewer from the bucket (or flip
//      allowBlobPublicAccess=false on the Azure account).
//   2. Add CORS so the browser can PUT to the signed URL.
//   3. Flip GET /photos/:id to return a signed GET URL instead of a public one.
//
// End-state from L3: validated POST /photos + prerecorded /photos/sign with
// pending→ready status, signurl.ts wired for both PUT and GET.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { randomUUID } from "node:crypto";
import { appConfig } from "./config.js";
import { storage } from "./storage.js";
import { query } from "./db.js";
import { issuePutUrl, issueGetUrl } from "./signurl.js";

const ALLOWED_MIME = new Set(["image/jpeg", "image/png", "image/webp"]);
const MAX_BYTES = 10 * 1024 * 1024;

const app = new Hono();

app.get("/health", (c) =>
  c.json({ status: "ok", track: appConfig.track }),
);

// Server-mediated upload (kept so students can compare the two paths).
app.post("/photos", async (c) => {
  const body = await c.req.parseBody();
  const file = body.file;
  const trailItemIdRaw = body.trail_item_id;
  if (!(file instanceof File)) return c.json({ error: "file field required" }, 400);
  const trailItemId = Number(trailItemIdRaw);
  if (!Number.isInteger(trailItemId) || trailItemId <= 0) {
    return c.json({ error: "trail_item_id field required" }, 400);
  }
  if (!ALLOWED_MIME.has(file.type)) return c.json({ error: `unsupported mime ${file.type}` }, 400);
  if (file.size > MAX_BYTES) return c.json({ error: `max ${MAX_BYTES} bytes` }, 413);

  const key = `photos/${trailItemId}/${randomUUID()}-${file.name}`;
  const buffer = Buffer.from(await file.arrayBuffer());
  const url = await storage.upload(buffer, key, file.type);
  const { rows } = await query<{ id: number }>(
    "INSERT INTO trail_photos (trail_item_id, storage_key, content_type, bytes, status) " +
      "VALUES ($1, $2, $3, $4, 'ready') RETURNING id",
    [trailItemId, key, file.type, buffer.byteLength],
  );
  return c.json({ id: rows[0].id, url, key }, 201);
});

// Direct-to-storage presigned PUT. API never sees the bytes.
app.post("/photos/sign", async (c) => {
  const body = (await c.req.json().catch(() => ({}))) as {
    trail_item_id?: number;
    content_type?: string;
    filename?: string;
  };
  if (!body.trail_item_id || !body.content_type || !body.filename) {
    return c.json({ error: "trail_item_id, content_type, filename required" }, 400);
  }
  if (!ALLOWED_MIME.has(body.content_type)) {
    return c.json({ error: `unsupported mime ${body.content_type}` }, 400);
  }
  const key = `photos/${body.trail_item_id}/${randomUUID()}-${body.filename}`;
  // Prerecord as 'pending' — the thumbnail trigger in L5 will flip it to 'ready'.
  const { rows } = await query<{ id: number }>(
    "INSERT INTO trail_photos (trail_item_id, storage_key, content_type, status) " +
      "VALUES ($1, $2, $3, 'pending') RETURNING id",
    [body.trail_item_id, key, body.content_type],
  );
  const url = await issuePutUrl(key, body.content_type);
  return c.json({ id: rows[0].id, url, key, expires_in: 900 });
});

// Signed GET — swap from public URLs to signed-only in L4.
app.get("/photos/:id", async (c) => {
  const id = Number(c.req.param("id"));
  const { rows } = await query<{ storage_key: string; status: string }>(
    "SELECT storage_key, status FROM trail_photos WHERE id = $1",
    [id],
  );
  if (rows.length === 0) return c.json({ error: "not_found" }, 404);
  const url = await issueGetUrl(rows[0].storage_key);
  return c.json({ url, status: rows[0].status, expires_in: 300 });
});

serve({ fetch: app.fetch, port: appConfig.port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
