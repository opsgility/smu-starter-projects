// Lumen Trail backend — SAAS-160 Lesson 1 starter.
//
// L1 is about the GCS mental model. You create a bucket from the gcloud CLI
// and upload a sample photo — all through gcloud, no API code required yet.
// The /health route confirms STORAGE_TRACK + which track is live.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { appConfig } from "./config.js";

const app = new Hono();

app.get("/health", (c) =>
  c.json({
    status: "ok",
    track: appConfig.track,
    gcs_bucket: appConfig.gcs.bucket || "<unset>",
    azure_container: appConfig.azure.container || "<unset>",
  }),
);

serve({ fetch: app.fetch, port: appConfig.port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
