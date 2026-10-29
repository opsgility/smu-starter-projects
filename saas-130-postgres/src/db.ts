// Shared Postgres client for the Lumen Trail SAAS-130 starter.
//
// We use a connection *pool* instead of a one-shot client. A pool keeps a
// small number of connections open so each query reuses them instead of
// paying the TCP + auth cost on every call. Real production backends always
// use a pool.

import { Pool } from "pg";
import "dotenv/config";

if (!process.env.DATABASE_URL) {
  throw new Error(
    "DATABASE_URL is not set. Copy .env.example to .env or export the var."
  );
}

export const db = new Pool({
  connectionString: process.env.DATABASE_URL,
  // A small pool is plenty for a lab. Production: tune per worker.
  max: 5,
});

export async function query<T = unknown>(
  text: string,
  params?: unknown[]
): Promise<T[]> {
  const result = await db.query(text, params);
  return result.rows as T[];
}
