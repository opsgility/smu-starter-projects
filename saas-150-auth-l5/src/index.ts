// Lumen Trail auth API — SAAS-150 Lesson 5 starter.
//
// End-state of Lesson 4: everything above PLUS TOTP MFA.
// Signin flow when TOTP is enabled:
//   1. POST /signin  -> returns { requires_mfa: true, mfa_token: "..." }
//   2. POST /signin/verify-totp with { mfa_token, code } -> creates real session

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { getCookie, setCookie, deleteCookie } from "hono/cookie";
import { generateState } from "arctic";
import { z } from "zod";
import { randomBytes } from "node:crypto";
import { query } from "./db.js";
import {
  hashPassword, verifyPassword, createSession, destroySession, requireUser,
  newToken, hashToken, type SessionUser,
} from "./auth.js";
import { github } from "./oauth.js";
import { sendVerificationEmail, sendPasswordResetEmail } from "./mail.js";
import {
  generateTotpSecret, buildOtpauthUrl, qrCodeDataUrl, verifyTotp,
  generateBackupCodes, hashBackupCode, verifyBackupCode,
} from "./mfa.js";

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
  const token = newToken();
  const expiresAt = new Date(Date.now() + 60 * 60 * 1000);
  await query(
    `INSERT INTO email_tokens (user_id, purpose, token_hash, expires_at) VALUES ($1, 'verify_email', $2, $3)`,
    [user.id, token.hash, expiresAt]
  );
  await sendVerificationEmail(email, token.plain).catch(() => {});
  return c.json({ id: user.id, email, display_name, email_verified: false }, 201);
});

app.post("/signin", async (c) => {
  const parsed = z.object({ email: z.string().email().toLowerCase(), password: z.string().min(1) })
    .safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) return c.json({ error: { code: "invalid_request" } }, 400);
  const { email, password } = parsed.data;
  const rows = await query<{ id: number; password_hash: string | null; display_name: string; totp_enabled: boolean }>(
    `SELECT id, password_hash, display_name, totp_enabled FROM users WHERE email = $1`, [email]);
  const user = rows[0];
  const dummy = "$argon2id$v=19$m=65536,t=3,p=4$abcdefghijklmnopqrstuv$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
  const ok = await verifyPassword(user?.password_hash ?? dummy, password);
  if (!user || !user.password_hash || !ok) return c.json({ error: { code: "invalid_credentials" } }, 401);

  if (user.totp_enabled) {
    // Issue an MFA challenge instead of a session.
    const mfa_token = randomBytes(32).toString("base64url");
    const expires = new Date(Date.now() + 10 * 60 * 1000);
    await query(
      `INSERT INTO mfa_challenges (id, user_id, expires_at) VALUES ($1, $2, $3)`,
      [mfa_token, user.id, expires]
    );
    return c.json({ requires_mfa: true, mfa_token });
  }

  await createSession(c, user.id);
  return c.json({ id: user.id, email, display_name: user.display_name });
});

app.post("/signin/verify-totp", async (c) => {
  const parsed = z.object({
    mfa_token: z.string().min(1),
    code: z.string().min(1),
  }).safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) return c.json({ error: { code: "invalid_request" } }, 400);
  const { mfa_token, code } = parsed.data;

  const rows = await query<{ user_id: number; expires_at: string }>(
    `SELECT user_id, expires_at FROM mfa_challenges WHERE id = $1`, [mfa_token]);
  const row = rows[0];
  if (!row || new Date(row.expires_at) < new Date()) {
    return c.json({ error: { code: "invalid_mfa_token" } }, 400);
  }

  const userRows = await query<{ id: number; email: string; display_name: string; totp_secret: string | null }>(
    `SELECT id, email, display_name, totp_secret FROM users WHERE id = $1`, [row.user_id]);
  const user = userRows[0];
  if (!user?.totp_secret) return c.json({ error: { code: "mfa_not_configured" } }, 400);

  // Accept a valid TOTP code OR an unused backup code.
  let authenticated = verifyTotp(code, user.totp_secret);
  if (!authenticated) {
    const codes = await query<{ id: number; code_hash: string }>(
      `SELECT id, code_hash FROM backup_codes WHERE user_id = $1 AND used_at IS NULL`,
      [user.id]
    );
    for (const bc of codes) {
      if (await verifyBackupCode(bc.code_hash, code)) {
        await query(`UPDATE backup_codes SET used_at = NOW() WHERE id = $1`, [bc.id]);
        authenticated = true;
        break;
      }
    }
  }
  if (!authenticated) return c.json({ error: { code: "invalid_mfa_code" } }, 401);

  await query(`DELETE FROM mfa_challenges WHERE id = $1`, [mfa_token]);
  await createSession(c, user.id);
  return c.json({ id: user.id, email: user.email, display_name: user.display_name });
});

app.post("/signout", async (c) => { await destroySession(c); return c.json({ ok: true }); });
app.get("/me", requireUser, (c) => c.json(c.get("user")));

// ---- TOTP enrollment ----

app.post("/mfa/enroll/start", requireUser, async (c) => {
  const user = c.get("user");
  if (user.totp_enabled) return c.json({ error: { code: "mfa_already_enabled" } }, 400);

  const secret = generateTotpSecret();
  const otpauth = buildOtpauthUrl(user.email, secret);
  const qr = await qrCodeDataUrl(otpauth);

  // Store the secret but DON'T flip totp_enabled yet — the user has to verify a first code.
  await query(`UPDATE users SET totp_secret = $1 WHERE id = $2`, [secret, user.id]);

  return c.json({ secret, otpauth_url: otpauth, qr_code: qr });
});

app.post("/mfa/enroll/verify", requireUser, async (c) => {
  const user = c.get("user");
  const parsed = z.object({ code: z.string().length(6) })
    .safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) return c.json({ error: { code: "invalid_request" } }, 400);

  const rows = await query<{ totp_secret: string | null }>(
    `SELECT totp_secret FROM users WHERE id = $1`, [user.id]);
  const secret = rows[0]?.totp_secret;
  if (!secret) return c.json({ error: { code: "mfa_not_started" } }, 400);
  if (!verifyTotp(parsed.data.code, secret)) {
    return c.json({ error: { code: "invalid_mfa_code" } }, 401);
  }

  // Generate backup codes BEFORE flipping totp_enabled, so the user has them.
  const codes = generateBackupCodes();
  const hashes = await Promise.all(codes.map(hashBackupCode));
  for (const h of hashes) {
    await query(`INSERT INTO backup_codes (user_id, code_hash) VALUES ($1, $2)`, [user.id, h]);
  }
  await query(`UPDATE users SET totp_enabled = TRUE WHERE id = $1`, [user.id]);

  return c.json({ ok: true, backup_codes: codes });
});

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
  if (rows.length > 0) {
    const token = newToken();
    const expiresAt = new Date(Date.now() + 60 * 60 * 1000);
    await query(
      `INSERT INTO email_tokens (user_id, purpose, token_hash, expires_at)
         VALUES ($1, 'password_reset', $2, $3)`,
      [rows[0].id, token.hash, expiresAt]
    );
    await sendPasswordResetEmail(email, token.plain).catch(() => {});
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
  await query(`DELETE FROM sessions WHERE user_id = $1`, [row.user_id]);
  return c.json({ ok: true });
});

// ---- GitHub OAuth ----

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
