// Lumen Trail auth API — SAAS-150 Lesson 2 starter.
//
// End-state of Lesson 1: four endpoints work end to end against Argon2id-hashed
// passwords and Postgres-backed sessions.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { z } from "zod";
import { query } from "./db.js";
import {
  hashPassword,
  verifyPassword,
  createSession,
  destroySession,
  requireUser,
  type SessionUser,
} from "./auth.js";

const app = new Hono<{ Variables: { user: SessionUser } }>();

const signupSchema = z.object({
  email: z.string().email().toLowerCase(),
  display_name: z.string().min(1).max(100),
  password: z.string().min(8).max(200),
});

const signinSchema = z.object({
  email: z.string().email().toLowerCase(),
  password: z.string().min(1),
});

app.get("/health", (c) => c.json({ status: "ok" }));

app.post("/signup", async (c) => {
  const parsed = signupSchema.safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) {
    return c.json(
      { error: { code: "invalid_request", details: parsed.error.flatten() } },
      400
    );
  }
  const { email, display_name, password } = parsed.data;

  const existing = await query<{ id: number }>(
    `SELECT id FROM users WHERE email = $1`,
    [email]
  );
  if (existing.length > 0) {
    return c.json({ error: { code: "email_in_use", message: "That email is already registered." } }, 409);
  }

  const password_hash = await hashPassword(password);
  const [user] = await query<{ id: number }>(
    `INSERT INTO users (email, display_name, password_hash)
       VALUES ($1, $2, $3) RETURNING id`,
    [email, display_name, password_hash]
  );
  await createSession(c, user.id);
  return c.json({ id: user.id, email, display_name }, 201);
});

app.post("/signin", async (c) => {
  const parsed = signinSchema.safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) {
    return c.json({ error: { code: "invalid_request" } }, 400);
  }
  const { email, password } = parsed.data;

  const rows = await query<{ id: number; password_hash: string | null; display_name: string }>(
    `SELECT id, password_hash, display_name FROM users WHERE email = $1`,
    [email]
  );
  const user = rows[0];
  // Timing-safe: run the hash check even when the user doesn't exist, so the
  // response time doesn't leak which emails are registered.
  const dummy = "$argon2id$v=19$m=65536,t=3,p=4$abcdefghijklmnopqrstuv$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
  const ok = await verifyPassword(user?.password_hash ?? dummy, password);
  if (!user || !user.password_hash || !ok) {
    return c.json({ error: { code: "invalid_credentials", message: "Email or password is incorrect." } }, 401);
  }

  await createSession(c, user.id);
  return c.json({ id: user.id, email, display_name: user.display_name });
});

app.post("/signout", async (c) => {
  await destroySession(c);
  return c.json({ ok: true });
});

app.get("/me", requireUser, (c) => {
  const user = c.get("user");
  return c.json(user);
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail auth API listening on http://localhost:${info.port}`);
});
