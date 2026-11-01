// Shared Postgres pool for the Lumen Trail API.
import pg from "pg";
import { appConfig } from "./config.js";

if (!appConfig.databaseUrl) throw new Error("DATABASE_URL not set — see .env.example");

export const pool = new pg.Pool({ connectionString: appConfig.databaseUrl });

export async function query<T extends pg.QueryResultRow = pg.QueryResultRow>(
  text: string,
  params?: unknown[],
): Promise<pg.QueryResult<T>> {
  return pool.query<T>(text, params);
}
