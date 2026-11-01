// Shared node-redis v4 client for the Lumen Trail API.
// L5's worker.ts needs a SECOND client for blocking commands (BLPOP) —
// node-redis v4 won't let the main client issue blocking commands and
// non-blocking commands on the same connection. The worker uses redis.duplicate().
import { createClient, type RedisClientType } from "redis";
import { config } from "dotenv";

config();

const url = process.env.REDIS_URL ?? "redis://localhost:6379";

export const redis: RedisClientType = createClient({ url });
redis.on("error", (err) => console.error("[redis] error:", err));

let connected = false;
export async function connectRedis(): Promise<void> {
  if (!connected) {
    await redis.connect();
    connected = true;
  }
}
