// Lumen Trail backend — SAAS-160 Lesson 3 starter.
//
// L3 teaches presigned URLs. The exercises direct Claude Code to:
//   1. Fill in signurl.issuePutUrl() in src/signurl.ts.
//   2. Add POST /photos/sign that returns {url, key} the browser PUTs to.
//   3. Pre-record the trail_photos row with status='pending' before issuing
//      the URL so an abandoned upload leaves a cleanable row.
//
// End-state from L2: validated POST /photos + trail_photos row.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { randomUUID } from "node:crypto";
import { appConfig } from "./config.js";
import { storage } from "./storage.js";
import { query } from "./db.js";

const ALLOWED_MIME = new Set(["image/jpeg", "image/png", "image/webp"]);
const MAX_BYTES = 10 * 1024 * 1024;

const app = new Hono();

app.get("/health", (c) =>
  c.json({ status: "ok", track: appConfig.track }),
);

// L2 end-state: validated upload + photo row.
app.post("/photos", async (c) => {
  const body = await c.req.parseBody();
  const file = body.file;
  const trailItemIdRaw = body.trail_item_id;
  if (!(file instanceof File)) return c.json({ error: "file field required" }, 400);
  const trailItemId = Number(trailItemIdRaw);
  if (!Number.isInteger(trailItemId) || trailItemId <= 0) {
    return c.json({ error: "trail_item_id field required" }, 400);
  }
  if (!ALLOWED_MIME.has(file.type)) {
    return c.json({ error: `unsupported mime ${file.type}` }, 400);
  }
  if (file.size > MAX_BYTES) {
    return c.json({ error: `max ${MAX_BYTES} bytes` }, 413);
  }
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

app.get("/photos/:id", async (c) => {
  const id = Number(c.req.param("id"));
  const { rows } = await query(
    "SELECT id, storage_key, content_type, bytes, status, created_at FROM trail_photos WHERE id = $1",
    [id],
  );
  if (rows.length === 0) return c.json({ error: "not_found" }, 404);
  return c.json(rows[0]);
});

// TODO (L3 Exercise 1): add POST /photos/sign — call signurl.issuePutUrl() with
// a new storage_key, prerecord the trail_photos row with status='pending',
// return { url, key }.

serve({ fetch: app.fetch, port: appConfig.port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
