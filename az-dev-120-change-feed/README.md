# az-dev-120-change-feed

Anchorline change-feed CLI. Two commands:

- `churn <container>` — generates a small amount of change traffic (upload, overwrite, tier, delete).
- `replay [hours]` — reads the change feed for the past N hours via `ChangeFeedClient`.

```bash
dotnet run -- <account> churn changes
# Wait 5-15 min for the change feed to batch
dotnet run -- <account> replay 2
```
