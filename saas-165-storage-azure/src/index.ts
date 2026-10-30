// Lumen Trail backend — SAAS-165 Lesson 1 starter.
//
// Lesson 1 is about the Azure Blob mental model via az CLI — storage
// accounts, containers, blobs. You create a storage account and a container,
// upload a sample photo with `az storage blob upload`, and read it back. No
// code changes yet; Lesson 2 is where Node starts talking to Blob.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) =>
  c.json({
    status: "ok",
    account: process.env.AZURE_STORAGE_ACCOUNT ?? "<unset>",
    container: process.env.AZURE_STORAGE_CONTAINER ?? "<unset>"
  })
);

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
