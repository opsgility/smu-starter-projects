import { db, query } from "./db.js";

type OrderRow = {
  order_id: number;
  buyer: string;
  item: string;
  seller: string;
  quantity: number;
  total_cents: number;
};

const rows = await query<OrderRow>(`
  SELECT
    o.id            AS order_id,
    buyer.display_name  AS buyer,
    i.name              AS item,
    seller.display_name AS seller,
    o.quantity,
    o.total_cents
  FROM orders o
  JOIN users       buyer  ON buyer.id  = o.buyer_id
  JOIN trail_items i      ON i.id      = o.item_id
  JOIN users       seller ON seller.id = i.seller_id
  ORDER BY o.id
`);

console.log(`${rows.length} orders:`);
for (const r of rows) {
  const total = (r.total_cents / 100).toFixed(2);
  console.log(
    `  #${r.order_id}: ${r.buyer} bought ${r.quantity}× ${r.item} from ${r.seller} — $${total}`
  );
}
await db.end();
