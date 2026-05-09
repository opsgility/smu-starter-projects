#!/usr/bin/env node
import express, { type Request, type Response } from "express";
import { exportJWK, generateKeyPair } from "jose";

const PORT = 4000;
const ISSUER = `http://localhost:${PORT}`;
const KEY_ID = "auth-server-es256-1";

async function buildKeys() {
  const { privateKey, publicKey } = await generateKeyPair("ES256");
  const publicJwk = await exportJWK(publicKey);
  publicJwk.kid = KEY_ID;
  publicJwk.alg = "ES256";
  publicJwk.use = "sig";
  return { privateKey, publicKey, publicJwk };
}

async function main(): Promise<void> {
  const keys = await buildKeys();
  // Silence "unused" until students implement /token signing.
  void keys.privateKey;

  const app = express();
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  // Public JWKS — the resource server fetches this to verify token signatures.
  app.get("/.well-known/jwks.json", (_req: Request, res: Response) => {
    res.json({ keys: [keys.publicJwk] });
  });

  // OAuth 2.1 authorization-server metadata (RFC 8414).
  app.get(
    "/.well-known/oauth-authorization-server",
    (_req: Request, res: Response) => {
      res.json({
        issuer: ISSUER,
        authorization_endpoint: `${ISSUER}/authorize`,
        token_endpoint: `${ISSUER}/token`,
        jwks_uri: `${ISSUER}/.well-known/jwks.json`,
        response_types_supported: ["code"],
        grant_types_supported: ["authorization_code", "refresh_token"],
        code_challenge_methods_supported: ["S256"],
        token_endpoint_auth_methods_supported: ["none"],
      });
    },
  );

  // === Authorization endpoint (PKCE-required) ===
  //
  // TODO (Task 1): Implement the auth-code flow. The browser arrives with:
  //   - response_type=code
  //   - client_id
  //   - redirect_uri
  //   - code_challenge + code_challenge_method=S256   (PKCE — required)
  //   - scope (space-separated)
  //   - resource (RFC 8707 — pin the issued token to the MCP resource server)
  //   - state
  //
  // Steps:
  //   1) Validate code_challenge_method === "S256" (reject "plain").
  //   2) Generate a one-time authorization code; store it in an in-memory map
  //      alongside { code_challenge, redirect_uri, scope, resource, sub }.
  //   3) Redirect to redirect_uri with `?code=<code>&state=<state>`.
  //
  // For learning purposes, hard-code `sub: "demo-user"` — a real auth server
  // would render a login + consent page here.
  app.get("/authorize", (_req: Request, res: Response) => {
    res
      .status(501)
      .json({ error: "authorize_endpoint_not_implemented" });
  });

  // === Token endpoint ===
  //
  // TODO (Task 1): Implement the auth-code -> JWT exchange.
  //
  // Expected POST body (application/x-www-form-urlencoded):
  //   - grant_type=authorization_code
  //   - code
  //   - redirect_uri
  //   - client_id
  //   - code_verifier   (PKCE — verify SHA256(verifier) base64url == stored challenge)
  //   - resource        (RFC 8707 — must match the resource saved at /authorize)
  //
  // Steps:
  //   1) Look up the code; reject if missing/expired/already-used.
  //   2) Verify PKCE: base64url(sha256(code_verifier)) === stored code_challenge.
  //   3) Build claims:
  //        iss: ISSUER
  //        sub: stored.sub
  //        aud: stored.resource          // RFC 8707 binding — critical
  //        scope: stored.scope
  //        resource: stored.resource     // RFC 8707 echo
  //        exp: now + 15 min
  //        iat: now
  //   4) Sign with the ES256 private key; set protected header
  //        { alg: "ES256", kid: KEY_ID, typ: "JWT" }
  //   5) Return { access_token, token_type: "Bearer", expires_in: 900,
  //               scope, resource } as JSON.
  //
  // === RFC 8707 wiring ===
  // The `resource` parameter (e.g., http://localhost:3000/mcp) MUST flow:
  //   /authorize?resource=...  -->  stored alongside the code
  //                            -->  /token rejects if mismatched
  //                            -->  signed JWT carries it as `aud` (and `resource`)
  // This binding is what stops a token issued for one MCP server from being
  // replayed against a different one.
  app.post("/token", (_req: Request, res: Response) => {
    res
      .status(501)
      .json({ error: "token_endpoint_not_implemented" });
  });

  app.listen(PORT, "127.0.0.1", () => {
    console.error(
      `oauth-authserver listening on ${ISSUER} (jwks at ${ISSUER}/.well-known/jwks.json)`,
    );
  });
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
