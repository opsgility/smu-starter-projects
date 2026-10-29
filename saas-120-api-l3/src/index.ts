// Lumen Trail backend API — SAAS-120 Lesson 3 starter.
//
// End-state of Lesson 2. We added:
//   - /items (GET)        list every item in the in-memory catalog
//   - /items/:id (GET)    look up one item by its id
//   - /items (POST)       create an item, validated by a Zod schema
//
// Lesson 3 teaches error handling, status codes, and idempotency. You'll notice
// the error paths below are rough — they return 400 or a bare "not found" string.
// In Lesson 3 Claude Code tightens them up: structured error payloads, correct
// HTTP status codes, and support for idempotency keys on POST /items.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { z } from "zod";

const app = new Hono();

type Item = {
  id: string;
  name: string;
  priceCents: number;
  createdAt: string;
};

const items = new Map<string, Item>();

const createItemSchema = z.object({
  name: z.string().min(1).max(100),
  priceCents: z.number().int().nonnegative(),
});

app.get("/health", (c) => c.json({ status: "ok" }));

app.get("/version", (c) =>
  c.json({ name: "Lumen Trail API", version: "0.2.0", lesson: 3 })
);

app.get("/goodbye", (c) => c.json({ message: "See you on the trail!" }));

app.post("/echo", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  return c.json({ youSent: body });
});

app.get("/items", (c) => {
  return c.json({ items: Array.from(items.values()) });
});

app.get("/items/:id", (c) => {
  const id = c.req.param("id");
  const item = items.get(id);
  if (!item) return c.json({ error: "not found" }, 404);
  return c.json(item);
});

app.post("/items", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const parsed = createItemSchema.safeParse(body);
  if (!parsed.success) {
    return c.json({ error: parsed.error.flatten() }, 400);
  }
  const id = crypto.randomUUID();
  const item: Item = {
    id,
    name: parsed.data.name,
    priceCents: parsed.data.priceCents,
    createdAt: new Date().toISOString(),
  };
  items.set(id, item);
  return c.json(item, 201);
});

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
  console.log(`Try: curl http://localhost:${info.port}/items`);
});
