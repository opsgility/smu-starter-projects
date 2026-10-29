// Idempotent seed. Includes 1 Rain Jacket with inventory=1 so the race demo
// has something scarce to fight over.

import { db, query } from "./db.js";

const [{ count }] = await query<{ count: string }>(
  "SELECT COUNT(*)::text AS count FROM users"
);
if (Number(count) > 0) {
  console.log("database already seeded — skipping.");
  await db.end();
  process.exit(0);
}

await db.query(`
  INSERT INTO users (email, display_name) VALUES
    ('alex@lumentrail.example.com',  'Alex Rivera'),
    ('sam@lumentrail.example.com',   'Sam Chen'),
    ('taylor@lumentrail.example.com','Taylor Nguyen');

  INSERT INTO trail_items (seller_id, name, price_cents, inventory, category) VALUES
    (1, 'Trail Mix',         799,  120, 'food'),
    (1, 'Camping Lantern',   1999, 25,  'light'),
    (2, 'Rain Jacket',       8999, 1,   'apparel'),
    (2, 'Compass',           2500, 40,  'navigation'),
    (3, 'Snow Shovel',       3999, 5,   'tools');
`);

console.log("seeded. Rain Jacket has inventory=1 — that's what we'll race for in `npm run race`.");
await db.end();
