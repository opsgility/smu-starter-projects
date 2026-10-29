// Lumen Trail backend API — SAAS-120 Lesson 4 starter.
//
// End-state of Lesson 3. We added:
//   - Structured error payloads   { error: { code, message, details? } }
//   - Correct HTTP status codes   400 bad request, 404 not found, 409 conflict
//   - Idempotency-Key support on POST /items (replay-safe for 24h)
//   - A single error-handling middleware so no route needs to duplicate it
//
// Lesson 4 adds an OpenAPI document and a Swagger UI page so other teams can
// read + try the API without opening this file.

import { Hono } from "hono";
import { HTTPException } from "hono/http-exception";
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

type IdempotencyEntry = { itemId: string; expiresAt: number };
const idempotencyCache = new Map<string, IdempotencyEntry>();
const IDEMPOTENCY_TTL_MS = 24 * 60 * 60 * 1000;

const createItemSchema = z.object({
  name: z.string().min(1).max(100),
  priceCents: z.number().int().nonnegative(),
});

function errorPayload(code: string, message: string, details?: unknown) {
  return { error: details === undefined ? { code, message } : { code, message, details } };
}

app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json(errorPayload("http_error", err.message), err.status);
  }
  console.error("[unhandled]", err);
  return c.json(errorPayload("internal_error", "Something went wrong on the server."), 500);
});

app.get("/health", (c) => c.json({ status: "ok" }));

app.get("/version", (c) =>
  c.json({ name: "Lumen Trail API", version: "0.3.0", lesson: 4 })
);

app.get("/goodbye", (c) => c.json({ message: "See you on the trail!" }));

app.post("/echo", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  return c.json({ youSent: body });
});

app.get("/items", (c) => c.json({ items: Array.from(items.values()) }));

app.get("/items/:id", (c) => {
  const id = c.req.param("id");
  const item = items.get(id);
  if (!item) {
    return c.json(errorPayload("item_not_found", `No item with id '${id}'.`), 404);
  }
  return c.json(item);
});

app.post("/items", async (c) => {
  const key = c.req.header("Idempotency-Key");

  if (key) {
    const now = Date.now();
    const prior = idempotencyCache.get(key);
    if (prior && prior.expiresAt > now) {
      const existing = items.get(prior.itemId);
      if (existing) return c.json(existing, 200);
    }
  }

  const body = await c.req.json().catch(() => null);
  if (body === null) {
    return c.json(errorPayload("invalid_json", "Request body is not valid JSON."), 400);
  }

  const parsed = createItemSchema.safeParse(body);
  if (!parsed.success) {
    return c.json(
      errorPayload("invalid_request", "Request body failed validation.", parsed.error.flatten()),
      400
    );
  }

  const id = crypto.randomUUID();
  const item: Item = {
    id,
    name: parsed.data.name,
    priceCents: parsed.data.priceCents,
    createdAt: new Date().toISOString(),
  };
  items.set(id, item);

  if (key) {
    idempotencyCache.set(key, { itemId: id, expiresAt: Date.now() + IDEMPOTENCY_TTL_MS });
  }

  return c.json(item, 201);
});

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
