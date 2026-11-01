// Lumen Trail backend — SAAS-160 Lesson 5 starter.
//
// L5 teaches event-driven follow-up. Bucket object-finalize events kick off
// a Cloud Function (functions/thumbnail/index.ts) that generates thumbnails
// and marks the trail_photos row 'ready'. The API exposes a /photos/:id/thumb
// endpoint that returns a signed URL to the thumbnail object.
//
// End-state from L4: locked-down bucket, signed PUT and signed GET, prerecorded
// 'pending' rows on sign-URL issuance.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { randomUUID } from "node:crypto";
import { appConfig } from "./config.js";
import { storage } from "./storage.js";
import { query } from "./db.js";
import { issuePutUrl, issueGetUrl } from "./signurl.js";
import { markReady, markFailed } from "./thumbnail-status.js";

const ALLOWED_MIME = new Set(["image/jpeg", "image/png", "image/webp"]);
const MAX_BYTES = 10 * 1024 * 1024;

const app = new Hono();

app.get("/health", (c) =>
  c.json({ status: "ok", track: appConfig.track }),
);

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
  const { rows } = await query<{ id: number }>(
    "INSERT INTO trail_photos (trail_item_id, storage_key, content_type, status) " +
      "VALUES ($1, $2, $3, 'pending') RETURNING id",
    [body.trail_item_id, key, body.content_type],
  );
  const url = await issuePutUrl(key, body.content_type);
  return c.json({ id: rows[0].id, url, key, expires_in: 900 });
});

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

// New in L5 — thumbnail URL. Returns a signed URL to the derived thumb object
// (photos/thumbs/<key>) once the function has flipped status to 'ready'.
app.get("/photos/:id/thumb", async (c) => {
  const id = Number(c.req.param("id"));
  const { rows } = await query<{ storage_key: string; status: string }>(
    "SELECT storage_key, status FROM trail_photos WHERE id = $1",
    [id],
  );
  if (rows.length === 0) return c.json({ error: "not_found" }, 404);
  if (rows[0].status !== "ready") {
    return c.json({ error: "not_ready", status: rows[0].status }, 409);
  }
  const thumbKey = rows[0].storage_key.replace(/^photos\//, "photos/thumbs/");
  const url = await issueGetUrl(thumbKey);
  return c.json({ url, expires_in: 300 });
});

// Webhook used by the thumbnail function (functions/thumbnail/) to flip
// status + record final dimensions. L5 Exercise 5 wires the function to call it.
app.post("/photos/by-key/:key{.+}/ready", async (c) => {
  const key = c.req.param("key");
  const body = (await c.req.json().catch(() => ({}))) as {
    width?: number;
    height?: number;
    failed?: boolean;
  };
  if (body.failed) {
    await markFailed(key);
    return c.json({ status: "failed" });
  }
  if (!body.width || !body.height) return c.json({ error: "width + height required" }, 400);
  await markReady(key, { width: body.width, height: body.height });
  return c.json({ status: "ready" });
});

serve({ fetch: app.fetch, port: appConfig.port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
