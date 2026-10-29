// Lumen Trail backend API — SAAS-120 Lesson 5 starter.
//
// End-state of Lesson 4. We added:
//   - /openapi.json         a hand-written OpenAPI 3 document describing every endpoint
//   - /docs                 Swagger UI, so other teams can read + try the API in a browser
//
// We also moved the Hono `app` into its own file (this one) and left the
// server start-up in src/index.ts. That split is what makes Lesson 5 easy —
// a test can import `app` and call it with `app.request(...)` without ever
// opening a port.

import { Hono } from "hono";
import { HTTPException } from "hono/http-exception";
import { swaggerUI } from "@hono/swagger-ui";
import { z } from "zod";

export const app = new Hono();

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
  c.json({ name: "Lumen Trail API", version: "0.4.0", lesson: 5 })
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

// Hand-written OpenAPI 3 document.
export const openapiSpec = {
  openapi: "3.0.0",
  info: {
    title: "Lumen Trail API",
    version: "0.4.0",
    description: "Catalog + health API for Lumen Trail.",
  },
  paths: {
    "/health": {
      get: {
        summary: "Health check",
        responses: {
          "200": {
            description: "Service is alive",
            content: {
              "application/json": {
                schema: { type: "object", properties: { status: { type: "string" } } },
              },
            },
          },
        },
      },
    },
    "/items": {
      get: {
        summary: "List catalog items",
        responses: {
          "200": {
            description: "An object with an items array",
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  properties: {
                    items: { type: "array", items: { $ref: "#/components/schemas/Item" } },
                  },
                },
              },
            },
          },
        },
      },
      post: {
        summary: "Create a catalog item",
        parameters: [
          {
            name: "Idempotency-Key",
            in: "header",
            required: false,
            schema: { type: "string" },
            description: "Optional replay-safe key, valid for 24h.",
          },
        ],
        requestBody: {
          required: true,
          content: {
            "application/json": { schema: { $ref: "#/components/schemas/CreateItem" } },
          },
        },
        responses: {
          "201": {
            description: "Item created",
            content: {
              "application/json": { schema: { $ref: "#/components/schemas/Item" } },
            },
          },
          "400": { description: "Invalid request body" },
        },
      },
    },
    "/items/{id}": {
      get: {
        summary: "Fetch one catalog item",
        parameters: [
          { name: "id", in: "path", required: true, schema: { type: "string" } },
        ],
        responses: {
          "200": {
            description: "Found",
            content: {
              "application/json": { schema: { $ref: "#/components/schemas/Item" } },
            },
          },
          "404": { description: "No item with that id" },
        },
      },
    },
  },
  components: {
    schemas: {
      Item: {
        type: "object",
        properties: {
          id: { type: "string" },
          name: { type: "string" },
          priceCents: { type: "integer" },
          createdAt: { type: "string", format: "date-time" },
        },
        required: ["id", "name", "priceCents", "createdAt"],
      },
      CreateItem: {
        type: "object",
        properties: {
          name: { type: "string", minLength: 1, maxLength: 100 },
          priceCents: { type: "integer", minimum: 0 },
        },
        required: ["name", "priceCents"],
      },
    },
  },
} as const;

app.get("/openapi.json", (c) => c.json(openapiSpec));

app.get("/docs", swaggerUI({ url: "/openapi.json" }));
