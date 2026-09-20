#!/usr/bin/env node
/**
 * Lesson 16 stub OAuth 2.1 authorization server.
 *
 * Mirrors the Lesson 14 completed code: issues short-lived JWTs (15 minutes)
 * with proper iss / aud / exp / sub / scope / resource claims, and exposes a
 * JWKS endpoint for the resource server to validate against.
 *
 * Endpoints:
 *   GET  /.well-known/oauth-authorization-server   metadata document
 *   GET  /.well-known/jwks.json                    public keys
 *   POST /token                                    issue a JWT for one of
 *                                                  three demo users
 *
 * This is a STUB — there is no real PKCE flow, no consent UI, no client
 * registration. It exists only so the resource server has a real JWKS to
 * verify against and so students can issue tokens with different sub /
 * scope combinations to test multi-tenancy and scope enforcement.
 */
import express, { type Request, type Response } from "express";
import { SignJWT, exportJWK, generateKeyPair, type KeyLike } from "jose";

const PORT = Number(process.env.AUTH_PORT ?? 4000);
const ISSUER = process.env.OAUTH_ISSUER ?? `http://127.0.0.1:${PORT}`;
const RESOURCE = process.env.OAUTH_AUDIENCE ?? "http://127.0.0.1:3000/mcp";
const KEY_ID = "lesson16-key-1";
const ACCESS_TOKEN_TTL_SECONDS = 15 * 60;

// Three demo users so students can issue tokens for different subjects and
// verify per-user data scoping. Tokens are issued via POST /token?user=user-a
// (etc.) — no password, this is a learning sandbox.
const DEMO_USERS: Record<string, { sub: string; tenantId: string; scopes: string[] }> = {
  "user-a": {
    sub: "user-a-uuid",
    tenantId: "tenant-north",
    scopes: ["mcp:tools", "shipments:read", "shipments:write"],
  },
  "user-b": {
    sub: "user-b-uuid",
    tenantId: "tenant-north",
    scopes: ["mcp:tools", "shipments:read", "shipments:write"],
  },
  "user-c": {
    sub: "user-c-uuid",
    tenantId: "tenant-south",
    // user-c can read but cannot record deliveries — useful for testing scope
    // enforcement on the record_delivery tool.
    scopes: ["mcp:tools", "shipments:read"],
  },
};

interface SigningKey {
  privateKey: KeyLike;
  publicJwk: Record<string, unknown>;
}

async function buildSigningKey(): Promise<SigningKey> {
  const { privateKey, publicKey } = await generateKeyPair("RS256");
  const publicJwk = await exportJWK(publicKey);
  publicJwk.kid = KEY_ID;
  publicJwk.alg = "RS256";
  publicJwk.use = "sig";
  return { privateKey, publicJwk };
}

async function main() {
  const key = await buildSigningKey();
  const app = express();
  app.use(express.urlencoded({ extended: true }));
  app.use(express.json());

  app.get("/.well-known/oauth-authorization-server", (_req: Request, res: Response) => {
    res.json({
      issuer: ISSUER,
      token_endpoint: `${ISSUER}/token`,
      jwks_uri: `${ISSUER}/.well-known/jwks.json`,
      response_types_supported: ["code"],
      grant_types_supported: ["authorization_code", "refresh_token", "client_credentials"],
      code_challenge_methods_supported: ["S256"],
      token_endpoint_auth_methods_supported: ["none"],
      scopes_supported: ["mcp:tools", "shipments:read", "shipments:write"],
    });
  });

  app.get("/.well-known/jwks.json", (_req: Request, res: Response) => {
    res.json({ keys: [key.publicJwk] });
  });

  // POST /token?user=user-a&scope=...&audience=...
  // For demo purposes only — a real authorization server would do PKCE.
  app.post("/token", async (req: Request, res: Response) => {
    const userKey = String(req.query.user ?? req.body?.user ?? "user-a");
    const user = DEMO_USERS[userKey];
    if (!user) {
      res.status(400).json({ error: "unknown demo user", known: Object.keys(DEMO_USERS) });
      return;
    }

    const requestedScope = String(req.query.scope ?? req.body?.scope ?? "");
    const scopes = requestedScope
      ? requestedScope.split(/\s+/).filter((s) => user.scopes.includes(s))
      : user.scopes;

    const audience = String(req.query.audience ?? req.body?.audience ?? RESOURCE);

    const jwt = await new SignJWT({
      scope: scopes.join(" "),
      tenant_id: user.tenantId,
      // RFC 8707 — bind this token to ONE specific resource.
      resource: audience,
    })
      .setProtectedHeader({ alg: "RS256", kid: KEY_ID })
      .setIssuer(ISSUER)
      .setAudience(audience)
      .setSubject(user.sub)
      .setIssuedAt()
      .setExpirationTime(`${ACCESS_TOKEN_TTL_SECONDS}s`)
      .sign(key.privateKey);

    res.json({
      access_token: jwt,
      token_type: "Bearer",
      expires_in: ACCESS_TOKEN_TTL_SECONDS,
      scope: scopes.join(" "),
    });
  });

  app.listen(PORT, "127.0.0.1", () => {
    console.error(`auth-server listening on ${ISSUER}`);
    console.error(`Demo users: ${Object.keys(DEMO_USERS).join(", ")}`);
    console.error(`Issue a token: curl -X POST '${ISSUER}/token?user=user-a'`);
  });
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
