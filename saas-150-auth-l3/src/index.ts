// Lumen Trail auth API — SAAS-150 Lesson 3 starter.
//
// End-state of Lesson 2: password sign-up/sign-in PLUS GitHub OAuth.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { getCookie, setCookie, deleteCookie } from "hono/cookie";
import { generateState } from "arctic";
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
import { github } from "./oauth.js";

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
    return c.json({ error: { code: "invalid_request", details: parsed.error.flatten() } }, 400);
  }
  const { email, display_name, password } = parsed.data;
  const existing = await query<{ id: number }>(`SELECT id FROM users WHERE email = $1`, [email]);
  if (existing.length > 0) {
    return c.json({ error: { code: "email_in_use" } }, 409);
  }
  const password_hash = await hashPassword(password);
  const [user] = await query<{ id: number }>(
    `INSERT INTO users (email, display_name, password_hash) VALUES ($1, $2, $3) RETURNING id`,
    [email, display_name, password_hash]
  );
  await createSession(c, user.id);
  return c.json({ id: user.id, email, display_name }, 201);
});

app.post("/signin", async (c) => {
  const parsed = signinSchema.safeParse(await c.req.json().catch(() => ({})));
  if (!parsed.success) return c.json({ error: { code: "invalid_request" } }, 400);
  const { email, password } = parsed.data;
  const rows = await query<{ id: number; password_hash: string | null; display_name: string }>(
    `SELECT id, password_hash, display_name FROM users WHERE email = $1`, [email]);
  const user = rows[0];
  const dummy = "$argon2id$v=19$m=65536,t=3,p=4$abcdefghijklmnopqrstuv$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
  const ok = await verifyPassword(user?.password_hash ?? dummy, password);
  if (!user || !user.password_hash || !ok) {
    return c.json({ error: { code: "invalid_credentials" } }, 401);
  }
  await createSession(c, user.id);
  return c.json({ id: user.id, email, display_name: user.display_name });
});

app.post("/signout", async (c) => {
  await destroySession(c);
  return c.json({ ok: true });
});

app.get("/me", requireUser, (c) => c.json(c.get("user")));

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

  // Fetch the GitHub user profile.
  const ghResp = await fetch("https://api.github.com/user", {
    headers: {
      Authorization: `Bearer ${tokens.accessToken()}`,
      "User-Agent": "lumentrail-saas-150",
    },
  });
  if (!ghResp.ok) return c.json({ error: { code: "oauth_profile_failed" } }, 400);
  const profile = (await ghResp.json()) as { id: number; login: string; name?: string; email?: string };

  // GitHub may not return an email on /user unless the user has made it public.
  // Fall back to the /user/emails endpoint for the primary verified address.
  let email: string | undefined = profile.email ?? undefined;
  if (!email) {
    const emails = await fetch("https://api.github.com/user/emails", {
      headers: { Authorization: `Bearer ${tokens.accessToken()}`, "User-Agent": "lumentrail-saas-150" },
    }).then((r) => (r.ok ? r.json() : [])) as Array<{ email: string; primary: boolean; verified: boolean }>;
    email = emails.find((e) => e.primary && e.verified)?.email;
  }
  if (!email) return c.json({ error: { code: "oauth_no_email" } }, 400);

  // Link by github_user_id first, then fall back to email.
  const existing = await query<{ id: number }>(
    `SELECT id FROM users WHERE github_user_id = $1 OR email = $2 LIMIT 1`,
    [profile.id, email.toLowerCase()]
  );
  let userId: number;
  if (existing.length > 0) {
    userId = existing[0].id;
    await query(
      `UPDATE users SET github_user_id = $1 WHERE id = $2 AND github_user_id IS NULL`,
      [profile.id, userId]
    );
  } else {
    const [row] = await query<{ id: number }>(
      `INSERT INTO users (email, display_name, github_user_id) VALUES ($1, $2, $3) RETURNING id`,
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
});
