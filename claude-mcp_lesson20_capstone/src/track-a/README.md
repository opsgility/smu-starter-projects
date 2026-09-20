# Track A — DevOps (Kubernetes, read-only)

Put your Track A code here. Suggested layout:

- `src/track-a/k8s.ts` — `@kubernetes/client-node` wrapper
- `src/track-a/tools.ts` — `list_pods`, `describe_deployment`, `get_logs`
- `src/track-a/resources.ts` — manifest YAMLs as resources
- `src/track-a/roots.ts` — Roots enforcement helper

Wire registrations from `src/server.ts`. Track A keeps the
`StdioServerTransport` already in `server.ts`.

Delete `src/track-b/` and `src/track-c/` when you commit.
