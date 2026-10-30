// Lumen Trail backend — SAAS-160 Lesson 1 starter.
//
// This file is intentionally tiny. Lesson 1 is about learning the GCS mental
// model via gcloud: buckets, objects, keys. You create a bucket, upload a
// file with `gcloud storage cp`, and read it back — no API code yet.
// By the end of Lesson 2 this file grows a /photos endpoint.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) =>
  c.json({ status: "ok", project: process.env.GCP_PROJECT_ID ?? "<unset>" })
);

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
