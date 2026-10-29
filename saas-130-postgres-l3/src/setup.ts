// Applies the Lesson 2 end-state schema in Postgres from sql/001_schema.sql.
// Lesson 3 replaces this with node-pg-migrate — a tool that knows which
// migrations have run on which database.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { db } from "./db.js";

const here = dirname(fileURLToPath(import.meta.url));
const sql = readFileSync(join(here, "..", "sql", "001_schema.sql"), "utf8");

await db.query(sql);
console.log("Lesson 2 schema applied. 3 users, 5 trail items, 3 orders.");
await db.end();
