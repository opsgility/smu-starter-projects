# Track B — Knowledge (Notion/Confluence-style wiki)

Put your Track B code here. Suggested layout:

- `src/track-b/wiki-client.ts` — REST client for the wiki API
- `src/track-b/tools.ts` — `search_docs`, `read_doc`
- `src/track-b/resources.ts` — `wiki://{slug}` resource template
- `src/track-b/prompts.ts` — `write_doc` prompt template
- `src/track-b/elicit.ts` — confirmation flow via elicitation

Track B requires Streamable HTTP + OAuth 2.1. Swap the `StdioServerTransport`
in `src/server.ts` for `StreamableHTTPServerTransport` and use
`src/lib/auth.ts` for bearer-token validation.

Delete `src/track-a/` and `src/track-c/` when you commit.
