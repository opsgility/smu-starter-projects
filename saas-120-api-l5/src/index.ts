// Server entry point. The app itself is in src/app.ts so tests can import it
// and call it with app.request() without opening a port.

import { serve } from "@hono/node-server";
import { app } from "./app.js";

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
  console.log(`API docs:   http://localhost:${info.port}/docs`);
  console.log(`OpenAPI JSON: http://localhost:${info.port}/openapi.json`);
});
