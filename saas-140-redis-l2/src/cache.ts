// Cache-aside helper. L2 exercises walk you through filling this in with
// Claude Code — the TODO stubs are the lesson's teaching moments.
import { redis } from "./redis.js";

/**
 * getOrSet — the cache-aside pattern in one function.
 *
 * 1. Try Redis under `key`. If the value exists, parse and return it.
 * 2. Otherwise call `loader()`, write the result to Redis with TTL, return it.
 *
 * TODO (L2 Exercise 2): direct Claude Code to replace this stub with the real
 * implementation. The three failure modes the lesson covers:
 *   - Stampede (two clients miss simultaneously → both hit the DB).
 *   - Stale cache after a write (invalidate on write, L2 Exercise 5).
 *   - Negative caching (never cache a null; see the exercise for why).
 */
export async function getOrSet<T>(
  key: string,
  ttlSeconds: number,
  loader: () => Promise<T>,
): Promise<T> {
  // TODO: implement
  void key;
  void ttlSeconds;
  return loader();
}
