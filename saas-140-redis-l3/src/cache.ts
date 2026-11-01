// Cache-aside helper — end-state from Lesson 2.
import { redis } from "./redis.js";

export async function getOrSet<T>(
  key: string,
  ttlSeconds: number,
  loader: () => Promise<T>,
): Promise<T> {
  const hit = await redis.get(key);
  if (hit !== null) {
    return JSON.parse(hit) as T;
  }
  const value = await loader();
  await redis.set(key, JSON.stringify(value), { EX: ttlSeconds });
  return value;
}

export async function invalidate(key: string): Promise<void> {
  await redis.del(key);
}
