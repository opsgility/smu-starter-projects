#!/usr/bin/env node
/**
 * Lesson 16 SQLite seeder.
 *
 * Reads ./data/seed.sql and applies it to the database file pointed at by
 * SQLITE_PATH (defaults to ./data/shipments.db). Run via `npm run seed`.
 *
 * Idempotent: seed.sql drops shipments_history first, so re-running this
 * resets the demo data without contaminating earlier rows.
 */
import Database from "better-sqlite3";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { mkdir } from "node:fs/promises";

const __dirname = dirname(fileURLToPath(import.meta.url));
// __dirname here resolves to dist/data when compiled. The seed.sql file lives
// in the project's data/ folder at the repo root, so walk back two levels.
const PROJECT_ROOT = resolve(__dirname, "..", "..");
const SEED_SQL_PATH = resolve(PROJECT_ROOT, "data", "seed.sql");
const DB_PATH = process.env.SQLITE_PATH ?? resolve(PROJECT_ROOT, "data", "shipments.db");

async function main() {
  await mkdir(dirname(DB_PATH), { recursive: true });

  const sql = await readFile(SEED_SQL_PATH, "utf8");
  const db = new Database(DB_PATH);
  try {
    db.exec(sql);
    const count = db.prepare("SELECT COUNT(*) AS n FROM shipments_history").get() as { n: number };
    console.error(`Seeded ${count.n} rows into ${DB_PATH}`);
  } finally {
    db.close();
  }
}

main().catch((err) => {
  console.error("Seed failed:", err);
  process.exit(1);
});
