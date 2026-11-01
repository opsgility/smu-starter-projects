// In-memory Map-backed session store. This is DELIBERATELY broken for the
// L3 exercises — it dies on server restart and doesn't survive two processes.
// Exercise 3 directs Claude Code to swap this Map for Redis-backed sessions
// so a horizontally-scaled Lumen Trail actually works.

export type SessionRecord = { userId: number; email: string; expiresAt: number };

const store = new Map<string, SessionRecord>();

export const sessions = {
  async create(sid: string, record: SessionRecord): Promise<void> {
    store.set(sid, record);
  },
  async get(sid: string): Promise<SessionRecord | null> {
    const r = store.get(sid);
    if (!r) return null;
    if (r.expiresAt < Date.now()) {
      store.delete(sid);
      return null;
    }
    return r;
  },
  async destroy(sid: string): Promise<void> {
    store.delete(sid);
  },
};
