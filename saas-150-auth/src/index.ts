// Lumen Trail auth API — SAAS-150 Lesson 1 starter.
//
// Four endpoint stubs: /signup, /signin, /signout, /me. All return 501 until
// Lesson 1's exercises fill them in with real password hashing + session cookies.
// The users and sessions tables already exist via migrations.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) => c.json({ status: "ok" }));

app.post("/signup", (c) => c.json({ error: "not implemented yet — Lesson 1 fills this in" }, 501));
app.post("/signin", (c) => c.json({ error: "not implemented yet — Lesson 1 fills this in" }, 501));
app.post("/signout", (c) => c.json({ error: "not implemented yet — Lesson 1 fills this in" }, 501));
app.get("/me", (c) => c.json({ error: "not implemented yet — Lesson 1 fills this in" }, 501));

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail auth API listening on http://localhost:${info.port}`);
});
