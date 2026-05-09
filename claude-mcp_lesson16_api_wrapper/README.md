# Lesson 16 — Build an API-Wrapper MCP Server

Track 2 continues here. This starter is the **completed Lesson 14 OAuth-protected Streamable HTTP server** plus a real local environment to integrate against:

- **Auth server** — issues short-lived JWTs (RS256) with proper `iss`, `aud`, `exp`, `sub`, `scope`, and `resource` claims, served on port 4000.
- **Mock REST API** — Northwind shipments service on port 5000. Trusts the inbound bearer token (decodes the subject; the resource server is the one that actually verified the JWT).
- **SQLite database** — local `data/shipments.db` with `shipments_history` rows for three demo users.
- **Resource server (this MCP server)** — the Streamable HTTP server with bearer-token middleware, AsyncLocalStorage for caller context, and TODO scaffolds for four new tools.

Five base tools (`greet`, `add_numbers`, `fetch_url`, `format_json`, `calculate`) are already wired and OAuth-protected.

## What you will build

1. **Wire JWT context through tool handlers** — the bearer-token middleware already drops `{ sub, tenantId, scopes, bearerToken }` into AsyncLocalStorage. Every new tool must call `getCallerContext()` to read it.
2. **`search_shipments(query, status?, limit?, cursor?)`** — wrap the REST API; filter by `owner_sub = ctx.sub`; forward the bearer token; return paginated structured results.
3. **`get_shipment_history(id)`** — read SQLite with `WHERE shipment_id = ? AND owner_sub = ?` parameterized query.
4. **LRU+TTL cache (5 min)** — keys MUST start with `${ctx.sub}:` so users never share entries. Expose hit-rate via `cache_stats`.
5. **`record_delivery(id, signature)`** — `idempotentHint: true`. Requires scope `shipments:write`; return a clean structured error if the JWT is missing it.
6. **End-to-end test** — issue a token for `user-a`, ask Claude Code to "find delayed shipments and show their history," verify pagination works and that user-a never sees user-b's data.

## Running the three processes

You need three terminals. Each process is independent.

### 1. Install dependencies (root, auth-server, mock-api)

```bash
npm install
(cd auth-server && npm install)
(cd mock-api && npm install)
```

### 2. Seed the SQLite DB

```bash
npm run build
npm run seed
```

This reads `data/seed.sql` and writes `data/shipments.db` with 200 history rows.

### 3. Start the auth server (terminal 1)

```bash
npm run dev:auth
```

Listens on `http://127.0.0.1:4000`. Issue a token any time with:

```bash
curl -X POST 'http://127.0.0.1:4000/token?user=user-a'
```

Demo users:

| user | sub | scopes |
|---|---|---|
| `user-a` | `user-a-uuid` | `mcp:tools shipments:read shipments:write` |
| `user-b` | `user-b-uuid` | `mcp:tools shipments:read shipments:write` |
| `user-c` | `user-c-uuid` | `mcp:tools shipments:read` (no write — useful for scope-enforcement testing) |

### 4. Start the mock REST API (terminal 2)

```bash
npm run dev:mock
```

Listens on `http://127.0.0.1:5000`. Requires `Authorization: Bearer <jwt>`; decodes the subject from the token to scope responses.

### 5. Start the MCP resource server (terminal 3)

```bash
npm run dev:resource
```

Listens on `http://127.0.0.1:3000/mcp`. Validates inbound JWTs against the auth server's JWKS, populates the per-request `callerContext` (AsyncLocalStorage) with `{ sub, tenantId, scopes, bearerToken }`, then routes the request into the Streamable HTTP transport.

### 6. Connect Claude Code

```bash
claude mcp add --transport http secure-shipments http://127.0.0.1:3000/mcp
```

Claude Code will run the OAuth flow against the auth server, receive a token, and start calling tools.

## Configuration

Copy `.env.example` to `.env` and adjust if needed:

| Var | Default | Purpose |
|---|---|---|
| `PORT` | `3000` | Resource server port |
| `OAUTH_ISSUER` | `http://127.0.0.1:4000` | Auth server URL (becomes JWT `iss`) |
| `OAUTH_AUDIENCE` | `http://127.0.0.1:3000/mcp` | This server's URL (becomes JWT `aud`) |
| `OAUTH_JWKS_URI` | `http://127.0.0.1:4000/.well-known/jwks.json` | JWKS for signature verification |
| `MOCK_API_BASE` | `http://localhost:5000` | Upstream REST API base |
| `SQLITE_PATH` | `./data/shipments.db` | Local SQLite database |

## Verification

- SQL injection attempt in the `query` arg is safely parameterized (the SQLite call uses `?` placeholders).
- A token issued for user-b cannot read user-a's shipment history (`isError: true`).
- `cache_stats.per_user_keys` only counts entries belonging to the current caller — no bleed across subjects.
- Calling `record_delivery` with a `user-c` token (which lacks `shipments:write`) returns a structured "missing scope" error, not a crash.
- `nextCursor` round-trips through Claude Code on `search_shipments`.

## Notes

- Never `console.log` on an MCP server — `console.error` only.
- The mock API does NOT verify the JWT signature. The resource server is the trust boundary; the mock just looks at the subject claim. In production this would be a real downstream service applying its own validation (or the resource server would do an OAuth 2.0 Token Exchange to mint a downstream-audience token).
