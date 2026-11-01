// Minimal migration runner — applies every .sql file in ../sql in filename order.
// All migration files use IF NOT EXISTS / ON CONFLICT so re-running is safe.
import { Client } from "pg";
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { config } from "dotenv";

config();

const __dirname = dirname(fileURLToPath(import.meta.url));
const sqlDir = join(__dirname, "..", "sql");

async function main() {
  const url = process.env.DATABASE_URL;
  if (!url) throw new Error("DATABASE_URL not set (see .env.example)");

  const client = new Client({ connectionString: url });
  await client.connect();

  const files = readdirSync(sqlDir).filter((f) => f.endsWith(".sql")).sort();
  for (const file of files) {
    const sql = readFileSync(join(sqlDir, file), "utf8");
    process.stdout.write(`[migrate] applying ${file}... `);
    await client.query(sql);
    console.log("ok");
  }

  await client.end();
  console.log("[migrate] done.");
}

main().catch((err) => {
  console.error("[migrate] failed:", err);
  process.exit(1);
});
