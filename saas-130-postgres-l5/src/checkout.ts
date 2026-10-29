// Lumen Trail checkout — the Lesson 4 end-state.
// A transactional buy() function:
//   1. Opens a transaction with BEGIN.
//   2. SELECT ... FOR UPDATE locks the row for the duration of the transaction.
//   3. Checks inventory, updates it with a WHERE version = $expected clause (optimistic concurrency).
//   4. INSERTs the order.
//   5. COMMITs — or ROLLBACK on any failure.
//
// Lesson 5 reuses this function and benchmarks it against larger datasets.

import type { PoolClient } from "pg";
import { db } from "./db.js";

export type BuyResult =
  | { ok: true; orderId: number; itemName: string }
  | { ok: false; reason: "sold_out" | "version_conflict" | "unknown_item" };

export async function buy(
  buyerId: number,
  itemId: number,
  quantity: number
): Promise<BuyResult> {
  const client: PoolClient = await db.connect();
  try {
    await client.query("BEGIN");

    const { rows: itemRows } = await client.query<{
      id: number;
      name: string;
      price_cents: number;
      inventory: number;
      version: number;
    }>(
      `SELECT id, name, price_cents, inventory, version
         FROM trail_items
         WHERE id = $1
         FOR UPDATE`,
      [itemId]
    );

    if (itemRows.length === 0) {
      await client.query("ROLLBACK");
      return { ok: false, reason: "unknown_item" };
    }

    const item = itemRows[0];
    if (item.inventory < quantity) {
      await client.query("ROLLBACK");
      return { ok: false, reason: "sold_out" };
    }

    const upd = await client.query(
      `UPDATE trail_items
         SET inventory = inventory - $2,
             version   = version + 1
         WHERE id = $1 AND version = $3`,
      [itemId, quantity, item.version]
    );
    if (upd.rowCount === 0) {
      await client.query("ROLLBACK");
      return { ok: false, reason: "version_conflict" };
    }

    const { rows: orderRows } = await client.query<{ id: number }>(
      `INSERT INTO orders (buyer_id, item_id, quantity, total_cents)
         VALUES ($1, $2, $3, $4)
         RETURNING id`,
      [buyerId, itemId, quantity, item.price_cents * quantity]
    );

    await client.query("COMMIT");
    return { ok: true, orderId: orderRows[0].id, itemName: item.name };
  } catch (err) {
    await client.query("ROLLBACK").catch(() => {});
    throw err;
  } finally {
    client.release();
  }
}

// If invoked directly, do a single buy to prove the function works.
if (import.meta.url === `file://${process.argv[1]}`) {
  const result = await buy(1, 1, 1);
  console.log(result);
  await db.end();
}
