# Lesson 14 — Add OAuth 2.1 with PKCE to Your Server

Track 2 continues. This starter is the completed Lesson 12 Streamable HTTP server (Express + `StreamableHTTPServerTransport` + session management + origin allowlist + `127.0.0.1` binding) plus a stub OAuth 2.1 authorization server you will configure to issue properly-claimed JWTs.

You will run **two** processes side by side:

| Process | Port | Source | What it does |
|---|---|---|---|
| Resource server | 3000 | `src/server.ts` | The MCP server. Validates bearer tokens before serving `/mcp`. |
| Authorization server | 4000 | `auth-server/server.ts` | Issues short-lived JWTs. Exposes `/.well-known/jwks.json`. |

## Setup

```bash
npm install
cp .env.example .env

# Build both projects (root tsconfig already includes auth-server/**)
npm run build

# Terminal 1 — auth server on :4000
npm run dev:auth

# Terminal 2 — resource server on :3000
npm run dev:resource
```

## Environment

`.env.example`:

```
JWKS_URL=http://localhost:4000/.well-known/jwks.json
EXPECTED_AUDIENCE=http://localhost:3000/mcp
EXPECTED_ISSUER=http://localhost:4000
RESOURCE_SERVER_URL=http://localhost:3000/mcp
```

## Tasks

1. Configure the local stub authorization server (`auth-server/server.ts`) to issue JWTs with proper `iss`, `aud`, `exp`, and `resource` (RFC 8707) claims. Wire `/authorize` (PKCE-required) and `/token` (auth-code -> JWT exchange).
2. Implement bearer-token middleware in `src/middleware/bearerToken.ts` using `jose`: validate signature against the JWKS, validate `iss`, validate `aud` (must equal `EXPECTED_AUDIENCE`), validate `exp`. Mount it in front of the `/mcp` route.
3. Implement `/.well-known/oauth-protected-resource` on the resource server. Return JSON with `resource`, `authorization_servers`, and `bearer_methods_supported`.
4. Register the authenticated server in Claude Code:

   ```bash
   claude mcp add --transport http secure http://127.0.0.1:3000/mcp
   ```

   Complete the in-browser OAuth flow.

5. Test a forged token: hand-craft a JWT with the wrong `aud` and verify the server returns 401.
6. Test an expired token: use a token whose `exp` is in the past and verify proper rejection.

## Verification

- The OAuth flow succeeds end-to-end inside Claude Code.
- Forged and expired tokens are rejected with informative errors.
- The `.well-known/oauth-protected-resource` document is correctly served.

## Files

- `src/server.ts` — Streamable HTTP MCP server (complete from Lesson 12).
- `src/middleware/bearerToken.ts` — Bearer-token validation middleware (TODO stub).
- `auth-server/server.ts` — Stub authorization server on port 4000 (ES256 keypair, JWKS, metadata, `/authorize`, `/token`).

## Notes

- Never `console.log` on an MCP server — use `console.error` only.
- The `resource` (RFC 8707) parameter MUST flow `/authorize` -> stored code -> `/token` -> JWT `aud`. That binding is what stops a token issued for one MCP server from being replayed against a different one.
- Use `jose` for JWT verification — never hand-roll it.
