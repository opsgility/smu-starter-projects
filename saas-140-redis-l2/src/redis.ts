// Shared node-redis v4 client for the Lumen Trail API.
// Attach the error listener BEFORE connect() to avoid unhandled errors
// — this is the pattern the node-redis README documents.
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
