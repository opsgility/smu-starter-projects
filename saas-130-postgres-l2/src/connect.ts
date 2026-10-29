import { db, query } from "./db.js";

const rows = await query<{ now: string }>("SELECT NOW() as now");
console.log(`connected. Server time: ${rows[0].now}`);
await db.end();
