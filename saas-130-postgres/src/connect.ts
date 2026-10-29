// A tiny smoke test: connect to Postgres, run one trivial query, print the result.
// If this prints "connected" you have the pieces in place to start Lesson 1 Exercise 1.

import { db, query } from "./db.js";

const rows = await query<{ now: string }>("SELECT NOW() as now");
console.log(`connected to Postgres. Server time: ${rows[0].now}`);
await db.end();
