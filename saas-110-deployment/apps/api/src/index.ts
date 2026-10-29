import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { cors } from "hono/cors";
import { routesHandler } from "./routes.js";

const app = new Hono();

app.use("*", cors());

app.get("/health", (c) => c.json({ status: "ok" }));

app.get("/routes", routesHandler);

const port = Number(process.env.PORT ?? 8787);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
