// Lumen Trail backend — SAAS-160 Lesson 2 starter.
//
// End state of Lesson 1 (which did everything via `gcloud storage` — no API
// code was changed). This file is still tiny on purpose; Lesson 2 is where
// you grow a POST /photos endpoint that writes to GCS from Node.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) =>
  c.json({
    status: "ok",
    project: process.env.GCP_PROJECT_ID ?? "<unset>",
    bucket: process.env.GCS_BUCKET ?? "<unset>"
  })
);

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
