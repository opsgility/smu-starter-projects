import { Pool } from "pg";
import "dotenv/config";

if (!process.env.DATABASE_URL) {
  throw new Error(
    "DATABASE_URL is not set. Copy .env.example to .env or export the var."
  );
}

export const db = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 5,
});

export async function query<T = unknown>(
  text: string,
  params?: unknown[]
): Promise<T[]> {
  const result = await db.query(text, params);
  return result.rows as T[];
}
