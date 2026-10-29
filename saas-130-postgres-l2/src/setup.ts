// Rebuilds the Lesson 1 end-state schema in Postgres from sql/001_trail_items.sql.
// Equivalent to running `psql $DATABASE_URL -f sql/001_trail_items.sql` by hand.
//
// Lesson 2's exercises replace this one-table design with the proper three-table
// schema (users, trail_items, orders), still applied by hand via psql. Lesson 3
// moves everything into a migration tool.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { db } from "./db.js";

const here = dirname(fileURLToPath(import.meta.url));
const sqlPath = join(here, "..", "sql", "001_trail_items.sql");
const sql = readFileSync(sqlPath, "utf8");

await db.query(sql);
console.log("Lesson 1 schema applied. 5 trail items inserted.");
await db.end();
