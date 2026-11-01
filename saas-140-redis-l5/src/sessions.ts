import { redis } from "./redis.js";

export type SessionRecord = { userId: number; email: string };
const SESSION_PREFIX = "session:";
const DEFAULT_TTL_SECONDS = 60 * 60 * 24;

export const sessions = {
  async create(sid: string, record: SessionRecord): Promise<void> {
    await redis.set(SESSION_PREFIX + sid, JSON.stringify(record), {
      EX: DEFAULT_TTL_SECONDS,
    });
  },
  async get(sid: string): Promise<SessionRecord | null> {
    const raw = await redis.get(SESSION_PREFIX + sid);
    if (!raw) return null;
    return JSON.parse(raw) as SessionRecord;
  },
  async destroy(sid: string): Promise<void> {
    await redis.del(SESSION_PREFIX + sid);
  },
};
