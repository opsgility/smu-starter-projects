// Lumen Trail backend — SAAS-160 Lesson 2 starter.
//
// L2 teaches server-mediated upload — the browser POSTs multipart form data
// at the API, the API buffers it in memory, uploads to object storage via
// the storage facade, and inserts a trail_photos row. The exercises direct
// Claude Code to add MIME/size validation and the photo-row insert.
//
// Storage track is picked at runtime via STORAGE_TRACK (gcs | azure).

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { randomUUID } from "node:crypto";
import { appConfig } from "./config.js";
import { storage } from "./storage.js";
import { query } from "./db.js";

const app = new Hono();

app.get("/health", (c) =>
  c.json({ status: "ok", track: appConfig.track }),
);

// Baseline upload — no MIME/size validation, no DB row. The L2 exercises walk
// you through adding both.
app.post("/photos", async (c) => {
  const body = await c.req.parseBody();
  const file = body.file;
  if (!(file instanceof File)) {
    return c.json({ error: "file field required" }, 400);
  }
  const key = `photos/${randomUUID()}-${file.name}`;
  const buffer = Buffer.from(await file.arrayBuffer());
  const url = await storage.upload(buffer, key, file.type || "application/octet-stream");
  return c.json({ url, key, bytes: buffer.byteLength }, 201);
});

// Example of the trail_photos insert the exercises build toward.
app.get("/photos", async (c) => {
  const { rows } = await query(
    "SELECT id, storage_key, content_type, bytes, status, created_at FROM trail_photos ORDER BY id DESC LIMIT 50",
  );
  return c.json({ photos: rows });
});

serve({ fetch: app.fetch, port: appConfig.port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
