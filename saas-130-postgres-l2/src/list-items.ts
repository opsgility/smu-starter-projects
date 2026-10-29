import { db, query } from "./db.js";

type Item = { id: number; name: string; price_cents: number; created_at: string };

const items = await query<Item>(
  "SELECT id, name, price_cents, created_at FROM trail_items ORDER BY id"
);

console.log(`${items.length} trail items in the catalog:`);
for (const item of items) {
  const price = (item.price_cents / 100).toFixed(2);
  console.log(`  #${item.id}  ${item.name.padEnd(20)}  $${price}`);
}

await db.end();
