// Shared auth primitives: password hashing, session creation / validation,
// and a middleware that attaches the current user to the request context.

import { randomBytes } from "node:crypto";
import argon2 from "argon2";
import type { Context, Next } from "hono";
import { getCookie, setCookie, deleteCookie } from "hono/cookie";
import { query } from "./db.js";

const SESSION_COOKIE = "lt_session";
const SESSION_TTL_DAYS = 30;

export async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, { type: argon2.argon2id });
}

export async function verifyPassword(hash: string, password: string): Promise<boolean> {
  try {
    return await argon2.verify(hash, password);
  } catch {
    return false;
  }
}

export function newSessionId(): string {
  return randomBytes(32).toString("base64url");
}

export type SessionUser = {
  id: number;
  email: string;
  display_name: string;
};

export async function createSession(c: Context, userId: number): Promise<string> {
  const sessionId = newSessionId();
  const expiresAt = new Date(Date.now() + SESSION_TTL_DAYS * 24 * 60 * 60 * 1000);
  await query(
    `INSERT INTO sessions (id, user_id, expires_at) VALUES ($1, $2, $3)`,
    [sessionId, userId, expiresAt]
  );
  setCookie(c, SESSION_COOKIE, sessionId, {
    httpOnly: true,
    sameSite: "Lax",
    path: "/",
    secure: false, // true in production over HTTPS
    expires: expiresAt,
  });
  return sessionId;
}

export async function getSessionUser(c: Context): Promise<SessionUser | null> {
  const sessionId = getCookie(c, SESSION_COOKIE);
  if (!sessionId) return null;
  const rows = await query<SessionUser & { expires_at: string }>(
    `SELECT u.id, u.email, u.display_name, s.expires_at
       FROM sessions s
       JOIN users u ON u.id = s.user_id
       WHERE s.id = $1`,
    [sessionId]
  );
  if (rows.length === 0) return null;
  if (new Date(rows[0].expires_at) < new Date()) {
    await query(`DELETE FROM sessions WHERE id = $1`, [sessionId]);
    return null;
  }
  return { id: rows[0].id, email: rows[0].email, display_name: rows[0].display_name };
}

export async function destroySession(c: Context): Promise<void> {
  const sessionId = getCookie(c, SESSION_COOKIE);
  if (sessionId) {
    await query(`DELETE FROM sessions WHERE id = $1`, [sessionId]);
    deleteCookie(c, SESSION_COOKIE, { path: "/" });
  }
}

export async function requireUser(c: Context, next: Next) {
  const user = await getSessionUser(c);
  if (!user) {
    return c.json({ error: { code: "unauthorized", message: "Sign in required." } }, 401);
  }
  c.set("user", user);
  await next();
}
