// Lumen Trail event worker — SAAS-140 Lesson 5 starter.
//
// This worker drains signup events the API LPUSHes onto `signup-events`.
// It uses BLPOP (blocking left-pop) on a DEDICATED node-redis connection
// — v4 won't let the main client issue BLPOP alongside non-blocking commands.
//
// The L5 exercises walk you from this BLPOP shape through:
//   1. The "listener down → event lost" failure mode of plain PUBLISH/SUBSCRIBE.
//   2. Redis Streams with consumer groups — events survive consumer downtime.
//   3. Idempotent processing via INSERT ... ON CONFLICT DO NOTHING on signup_events.

import { connectRedis, redis } from "./redis.js";
import { query } from "./db.js";

async function main() {
  await connectRedis();
  const consumer = redis.duplicate();
  consumer.on("error", (err) => console.error("[worker] redis error:", err));
  await consumer.connect();

  console.log("[worker] listening on signup-events (BLPOP) — Ctrl+C to stop");

  while (true) {
    const popped = await consumer.blPop("signup-events", 0);
    if (!popped) continue;
    try {
      const event = JSON.parse(popped.element) as {
        user_id: number;
        email: string;
        at: number;
      };
      await query(
        "INSERT INTO signup_events (user_id, email, happened_at) VALUES ($1, $2, to_timestamp($3 / 1000.0)) " +
          "ON CONFLICT DO NOTHING",
        [event.user_id, event.email, event.at],
      );
      console.log(`[worker] drained signup for ${event.email}`);
    } catch (err) {
      console.error("[worker] bad event:", popped.element, err);
    }
  }
}

main().catch((err) => {
  console.error("[worker] fatal:", err);
  process.exit(1);
});
