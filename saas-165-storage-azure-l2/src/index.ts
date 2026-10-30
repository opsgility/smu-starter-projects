// Lumen Trail backend — SAAS-165 Lesson 2 starter.
//
// End state of Lesson 1 (which did everything via az CLI). This starter is
// still tiny on purpose. In Lesson 2 you grow a POST /photos endpoint that
// writes to Blob from Node using DefaultAzureCredential.

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
