#!/usr/bin/env node
/**
 * Lesson 16 mock REST API.
 *
 * Simulates Northwind's internal shipments service. Three endpoints:
 *
 *   GET  /shipments                   list, filterable by query/status, paginated
 *   GET  /shipments/:id/history       per-shipment history events
 *   POST /shipments/:id/deliveries    record a delivery (requires the bearer
 *                                     token's scope claim to include
 *                                     "shipments:write")
 *
 * Trust model: this mock does NOT verify JWT signatures. It simply decodes
 * the payload to extract `sub` and `scope` for the demo. The real Lesson 16
 * resource server forwards its validated bearer token here, and the mock
 * mirrors that subject in the responses so students can prove that the
 * downstream service correctly applies access control on a per-user basis.
 *
 * The mock seeds 50 shipments split across three demo subjects:
 *   user-a-uuid, user-b-uuid, user-c-uuid.
 */
import express, { type Request, type Response, type NextFunction } from "express";
import { z } from "zod";

const PORT = Number(process.env.MOCK_API_PORT ?? 5000);

interface Shipment {
  id: string;
  query_match: string;
  status: "pending" | "in_transit" | "delivered" | "delayed";
  owner_sub: string;
  destination: string;
}

interface HistoryEvent {
  ts: string;
  event: string;
}

const SUBJECTS = ["user-a-uuid", "user-b-uuid", "user-c-uuid"];
const STATUSES: Shipment["status"][] = ["pending", "in_transit", "delivered", "delayed"];
const CITIES = [
  "Austin TX",
  "Dallas TX",
  "Houston TX",
  "Boston MA",
  "Seattle WA",
  "Denver CO",
  "Atlanta GA",
  "Chicago IL",
  "Phoenix AZ",
  "Miami FL",
];

const SHIPMENTS: Shipment[] = [];
for (let i = 1; i <= 50; i++) {
  const id = `SHIP-${String(i).padStart(4, "0")}`;
  const dest = CITIES[i % CITIES.length];
  SHIPMENTS.push({
    id,
    query_match: `${id} ${dest}`.toLowerCase(),
    status: STATUSES[i % STATUSES.length],
    owner_sub: SUBJECTS[i % SUBJECTS.length],
    destination: dest,
  });
}

// In-memory deliveries log, keyed by shipment id. Persistence is intentionally
// not implemented — restart the server to reset.
const DELIVERIES = new Map<string, { id: string; delivered_at: string; signature: string }>();

interface BearerInfo {
  sub: string;
  scopes: string[];
}

function decodeBearer(req: Request): BearerInfo | null {
  const header = req.headers.authorization;
  if (!header || !header.startsWith("Bearer ")) return null;
  const token = header.slice("Bearer ".length).trim();
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    const json = Buffer.from(parts[1], "base64url").toString("utf8");
    const payload = JSON.parse(json) as { sub?: string; scope?: string };
    if (!payload.sub) return null;
    const scopes = (payload.scope ?? "").split(/\s+/).filter(Boolean);
    return { sub: payload.sub, scopes };
  } catch {
    return null;
  }
}

function requireBearer(req: Request, res: Response, next: NextFunction) {
  const info = decodeBearer(req);
  if (!info) {
    res.status(401).json({ error: "missing or malformed Authorization: Bearer <token>" });
    return;
  }
  (req as Request & { bearer: BearerInfo }).bearer = info;
  next();
}

const querySchema = z.object({
  query: z.string().optional(),
  status: z.enum(["pending", "in_transit", "delivered", "delayed"]).optional(),
  limit: z.coerce.number().int().min(1).max(50).default(10),
  cursor: z.string().optional(),
});

async function main() {
  const app = express();
  app.use(express.json());

  app.get("/shipments", requireBearer, (req: Request, res: Response) => {
    const parsed = querySchema.safeParse(req.query);
    if (!parsed.success) {
      res.status(400).json({ error: "invalid query parameters", details: parsed.error.format() });
      return;
    }
    const { query, status, limit, cursor } = parsed.data;
    const bearer = (req as Request & { bearer: BearerInfo }).bearer;

    let pool = SHIPMENTS.filter((s) => s.owner_sub === bearer.sub);
    if (query) {
      const q = query.toLowerCase();
      pool = pool.filter((s) => s.query_match.includes(q));
    }
    if (status) pool = pool.filter((s) => s.status === status);

    const startIdx = cursor ? Number(Buffer.from(cursor, "base64url").toString("utf8")) || 0 : 0;
    const page = pool.slice(startIdx, startIdx + limit);
    const nextIdx = startIdx + limit;
    const nextCursor = nextIdx < pool.length ? Buffer.from(String(nextIdx)).toString("base64url") : undefined;

    res.json({
      items: page.map((s) => ({
        id: s.id,
        query_match: s.query_match,
        status: s.status,
        owner_sub: s.owner_sub,
      })),
      nextCursor,
    });
  });

  app.get("/shipments/:id/history", requireBearer, (req: Request, res: Response) => {
    const bearer = (req as Request & { bearer: BearerInfo }).bearer;
    const ship = SHIPMENTS.find((s) => s.id === req.params.id);
    if (!ship || ship.owner_sub !== bearer.sub) {
      res.status(404).json({ error: "shipment not found" });
      return;
    }
    // The mock REST API only stubs out a synthetic top-level history event. The
    // detailed per-event history actually lives in the local SQLite DB that
    // students wire up in Task 3 — this endpoint is here so students can choose
    // either path during exploration.
    const events: HistoryEvent[] = [
      { ts: new Date().toISOString(), event: `status=${ship.status}` },
    ];
    res.json({ events });
  });

  app.post("/shipments/:id/deliveries", requireBearer, (req: Request, res: Response) => {
    const bearer = (req as Request & { bearer: BearerInfo }).bearer;
    if (!bearer.scopes.includes("shipments:write")) {
      res.status(403).json({ error: "missing scope: shipments:write" });
      return;
    }
    const ship = SHIPMENTS.find((s) => s.id === req.params.id);
    if (!ship || ship.owner_sub !== bearer.sub) {
      res.status(404).json({ error: "shipment not found" });
      return;
    }
    const signature = String(req.body?.signature ?? "");
    if (!signature) {
      res.status(400).json({ error: "signature required" });
      return;
    }
    const record = {
      id: ship.id,
      delivered_at: new Date().toISOString(),
      signature,
    };
    DELIVERIES.set(ship.id, record);
    res.json({ id: record.id, delivered_at: record.delivered_at });
  });

  app.listen(PORT, "127.0.0.1", () => {
    console.error(`mock-api listening on http://127.0.0.1:${PORT}`);
    console.error(`Seeded ${SHIPMENTS.length} shipments across ${SUBJECTS.length} demo users.`);
  });
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
