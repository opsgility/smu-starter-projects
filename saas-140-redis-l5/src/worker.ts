// Lumen Trail worker — SAAS-140 Lesson 5 starter.
//
// This process is intentionally almost empty. It's the SECOND process that will
// subscribe to the "user-signed-up" Redis channel once you refactor signup to
// use pub/sub. Right now it just connects and prints that it's alive, so you
// have a place to add the subscriber.

import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL ?? "redis://127.0.0.1:6379");

async function main() {
  console.log("[worker] starting Lumen Trail background worker");
  await redis.ping();
  console.log("[worker] connected to Redis, nothing to do yet.");
}

main();
