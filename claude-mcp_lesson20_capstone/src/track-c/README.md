# Track C — Data (Read-only Postgres analytics)

Put your Track C code here. Suggested layout:

- `src/track-c/db.ts` — `pg` pool, `READ ONLY` transaction wrapper
- `src/track-c/tools.ts` — `run_query` (SELECT only, row caps)
- `src/track-c/resources.ts` — schema introspection (`schema://{table}`)
- `src/track-c/sampling.ts` — sampling/createMessage for result summarization

Track C requires Streamable HTTP + OAuth 2.1. Swap the `StdioServerTransport`
in `src/server.ts` for `StreamableHTTPServerTransport` and use
`src/lib/auth.ts` for bearer-token validation.

Delete `src/track-a/` and `src/track-b/` when you commit.
