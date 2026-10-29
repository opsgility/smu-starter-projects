// Idempotent seed: adds 3 users, 5 trail items, 3 orders if the tables are empty.
// Run this after `npm run migrate:up` on a fresh database.

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
    (2, 'Rain Jacket',       8999, 8,   'apparel'),
    (2, 'Compass',           2500, 40,  'navigation'),
    (3, 'Snow Shovel',       3999, 5,   'tools');

  INSERT INTO orders (buyer_id, item_id, quantity, total_cents, notes) VALUES
    (2, 1, 3, 2397, 'birthday gift'),
    (3, 3, 1, 8999, NULL),
    (1, 4, 2, 5000, 'spare compass');
`);

console.log("seeded. 3 users, 5 trail items, 3 orders.");
await db.end();
