// Lumen Trail auth API — SAAS-150 Lesson 4 starter.
//
// End-state of Lesson 3: everything above PLUS email verification on sign-up and
// a password reset flow, backed by single-use tokens with hashed storage.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { getCookie, setCookie, deleteCookie } from "hono/cookie";
import { generateState } from "arctic";
import { z } from "zod";
import { query } from "./db.js";
import {
  hashPassword, verifyPassword, createSession, destroySession, requireUser,
  newToken, hashToken, type SessionUser,
} from "./auth.js";
import { github } from "./oauth.js";
import { sendVerificationEmail, sendPasswordResetEmail } from "./mail.js";

const app = new Hono<{ Variables: { user: SessionUser } }>();

app.get("/health", (c) => c.json({ status: "ok" }));

// ---- Password auth ----

const signupSchema = z.object({
  email: z.string().email().toLowerCase(),
  display_name: z.string().min(1).max(100),
  password: z.string().min(8).max(200),
});

app.post("/signup", async (c) => {
  const parsed = signupSchema.safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) return c.json({ error: { code: "invalid_request", details: parsed.error.flatten() } }, 400);
  const { email, display_name, password } = parsed.data;

  const existing = await query<{ id: number }>(`SELECT id FROM users WHERE email = $1`, [email]);
  if (existing.length > 0) return c.json({ error: { code: "email_in_use" } }, 409);

  const password_hash = await hashPassword(password);
  const [user] = await query<{ id: number }>(
    `INSERT INTO users (email, display_name, password_hash) VALUES ($1, $2, $3) RETURNING id`,
    [email, display_name, password_hash]
  );
  await createSession(c, user.id);

  // Issue a one-hour verification token and send the email.
  const token = newToken();
  const expiresAt = new Date(Date.now() + 60 * 60 * 1000);
  await query(
    `INSERT INTO email_tokens (user_id, purpose, token_hash, expires_at)
       VALUES ($1, 'verify_email', $2, $3)`,
    [user.id, token.hash, expiresAt]
  );
  await sendVerificationEmail(email, token.plain).catch((err) => {
    console.error("[warn] verification email failed to send:", err);
  });

  return c.json({ id: user.id, email, display_name, email_verified: false }, 201);
});

app.post("/signin", async (c) => {
  const parsed = z.object({ email: z.string().email().toLowerCase(), password: z.string().min(1) })
    .safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) return c.json({ error: { code: "invalid_request" } }, 400);
  const { email, password } = parsed.data;
  const rows = await query<{ id: number; password_hash: string | null; display_name: string }>(
    `SELECT id, password_hash, display_name FROM users WHERE email = $1`, [email]);
  const user = rows[0];
  const dummy = "$argon2id$v=19$m=65536,t=3,p=4$abcdefghijklmnopqrstuv$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
  const ok = await verifyPassword(user?.password_hash ?? dummy, password);
  if (!user || !user.password_hash || !ok) return c.json({ error: { code: "invalid_credentials" } }, 401);
  await createSession(c, user.id);
  return c.json({ id: user.id, email, display_name: user.display_name });
});

app.post("/signout", async (c) => { await destroySession(c); return c.json({ ok: true }); });
app.get("/me", requireUser, (c) => c.json(c.get("user")));

// ---- Email verification ----

app.get("/verify-email", async (c) => {
  const plain = c.req.query("token");
  if (!plain) return c.json({ error: { code: "invalid_request" } }, 400);
  const token_hash = hashToken(plain);
  const rows = await query<{ id: number; user_id: number; expires_at: string; used_at: string | null }>(
    `SELECT id, user_id, expires_at, used_at FROM email_tokens
       WHERE token_hash = $1 AND purpose = 'verify_email'`, [token_hash]);
  const row = rows[0];
  if (!row) return c.json({ error: { code: "invalid_token" } }, 400);
  if (row.used_at) return c.json({ error: { code: "token_already_used" } }, 400);
  if (new Date(row.expires_at) < new Date()) return c.json({ error: { code: "token_expired" } }, 400);

  await query(`UPDATE email_tokens SET used_at = NOW() WHERE id = $1`, [row.id]);
  await query(`UPDATE users SET email_verified = TRUE WHERE id = $1`, [row.user_id]);
  return c.json({ ok: true });
});

// ---- Password reset ----

app.post("/password-reset/request", async (c) => {
  const parsed = z.object({ email: z.string().email().toLowerCase() })
    .safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) return c.json({ error: { code: "invalid_request" } }, 400);
  const { email } = parsed.data;

  const rows = await query<{ id: number }>(`SELECT id FROM users WHERE email = $1`, [email]);
  // Always respond ok to avoid leaking which emails are registered.
  if (rows.length > 0) {
    const token = newToken();
    const expiresAt = new Date(Date.now() + 60 * 60 * 1000);
    await query(
      `INSERT INTO email_tokens (user_id, purpose, token_hash, expires_at)
         VALUES ($1, 'password_reset', $2, $3)`,
      [rows[0].id, token.hash, expiresAt]
    );
    await sendPasswordResetEmail(email, token.plain).catch((err) => {
      console.error("[warn] password reset email failed to send:", err);
    });
  }
  return c.json({ ok: true });
});

app.post("/password-reset/confirm", async (c) => {
  const parsed = z.object({ token: z.string().min(1), new_password: z.string().min(8).max(200) })
    .safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) return c.json({ error: { code: "invalid_request" } }, 400);
  const { token, new_password } = parsed.data;

  const token_hash = hashToken(token);
  const rows = await query<{ id: number; user_id: number; expires_at: string; used_at: string | null }>(
    `SELECT id, user_id, expires_at, used_at FROM email_tokens
       WHERE token_hash = $1 AND purpose = 'password_reset'`, [token_hash]);
  const row = rows[0];
  if (!row) return c.json({ error: { code: "invalid_token" } }, 400);
  if (row.used_at) return c.json({ error: { code: "token_already_used" } }, 400);
  if (new Date(row.expires_at) < new Date()) return c.json({ error: { code: "token_expired" } }, 400);

  const password_hash = await hashPassword(new_password);
  await query(`UPDATE users SET password_hash = $1 WHERE id = $2`, [password_hash, row.user_id]);
  await query(`UPDATE email_tokens SET used_at = NOW() WHERE id = $1`, [row.id]);
  // Invalidate all existing sessions for this user — a password change should log out other devices.
  await query(`DELETE FROM sessions WHERE user_id = $1`, [row.user_id]);
  return c.json({ ok: true });
});

// ---- GitHub OAuth (unchanged from Lesson 3) ----

const GITHUB_STATE_COOKIE = "lt_oauth_state";

app.get("/oauth/github/start", (c) => {
  const state = generateState();
  const url = github.createAuthorizationURL(state, ["user:email"]);
  setCookie(c, GITHUB_STATE_COOKIE, state, {
    httpOnly: true, sameSite: "Lax", path: "/", secure: false, maxAge: 60 * 10,
  });
  return c.redirect(url.toString());
});

app.get("/oauth/github/callback", async (c) => {
  const code = c.req.query("code");
  const state = c.req.query("state");
  const storedState = getCookie(c, GITHUB_STATE_COOKIE);
  if (!code || !state || !storedState || state !== storedState) {
    return c.json({ error: { code: "oauth_state_mismatch" } }, 400);
  }
  deleteCookie(c, GITHUB_STATE_COOKIE, { path: "/" });

  const tokens = await github.validateAuthorizationCode(code).catch(() => null);
  if (!tokens) return c.json({ error: { code: "oauth_exchange_failed" } }, 400);

  const ghResp = await fetch("https://api.github.com/user", {
    headers: { Authorization: `Bearer ${tokens.accessToken()}`, "User-Agent": "lumentrail-saas-150" },
  });
  if (!ghResp.ok) return c.json({ error: { code: "oauth_profile_failed" } }, 400);
  const profile = (await ghResp.json()) as { id: number; login: string; name?: string; email?: string };

  let email: string | undefined = profile.email ?? undefined;
  if (!email) {
    const emails = await fetch("https://api.github.com/user/emails", {
      headers: { Authorization: `Bearer ${tokens.accessToken()}`, "User-Agent": "lumentrail-saas-150" },
    }).then((r) => (r.ok ? r.json() : [])) as Array<{ email: string; primary: boolean; verified: boolean }>;
    email = emails.find((e) => e.primary && e.verified)?.email;
  }
  if (!email) return c.json({ error: { code: "oauth_no_email" } }, 400);

  const existing = await query<{ id: number }>(
    `SELECT id FROM users WHERE github_user_id = $1 OR email = $2 LIMIT 1`,
    [profile.id, email.toLowerCase()]
  );
  let userId: number;
  if (existing.length > 0) {
    userId = existing[0].id;
    await query(
      `UPDATE users SET github_user_id = $1, email_verified = TRUE WHERE id = $2 AND github_user_id IS NULL`,
      [profile.id, userId]
    );
  } else {
    const [row] = await query<{ id: number }>(
      `INSERT INTO users (email, display_name, github_user_id, email_verified)
         VALUES ($1, $2, $3, TRUE) RETURNING id`,
      [email.toLowerCase(), profile.name ?? profile.login, profile.id]
    );
    userId = row.id;
  }

  await createSession(c, userId);
  return c.redirect("/me");
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail auth API listening on http://localhost:${info.port}`);
  console.log(`MailHog UI: http://localhost:8025`);
});
