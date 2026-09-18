# TaskForge Production-Readiness Checklist

## DR
- [ ] Paired-region SQL failover group configured
- [ ] Cosmos multi-region write configured
- [ ] Front Door / Traffic Manager fronting both regions
- [ ] DR runbook tested this quarter (`docs/DR-RUNBOOK.md`)

## Backup
- [ ] SQL PITR restore drilled to a NEW server this month
- [ ] Cosmos continuous backup enabled at account create
- [ ] Cosmos restore drilled this quarter
- [ ] Key Vault soft-delete retention ≥ 30 days
- [ ] Key Vault purge-protection enabled

## Cost
- [ ] Azure Cost Management budget with alerts at 80% + 100%
- [ ] Log Analytics daily ingestion cap set
- [ ] Cosmos autoscale-max reflects realistic peak
- [ ] APIM tier appropriate for baseline traffic

## Security (STRIDE-lite — see `docs/STRIDE-REVIEW.md`)
- [ ] RLS FILTER + BLOCK on every tenant-scoped SQL table
- [ ] Hierarchical partition key on every Cosmos tenant-scoped container
- [ ] APIM `<validate-jwt>` on every tenant-facing API
- [ ] Backend re-validates JWT (defense in depth)
- [ ] Two-identity separation (External ID vs Workforce Entra) enforced
- [ ] No client secrets in GitHub / repo / app config
- [ ] MI/federated cred used everywhere Azure-to-Azure

## Observability
- [ ] Three SLOs defined + alerted (availability, latency, error rate)
- [ ] Fast-burn + slow-burn burn-rate alerts wired
- [ ] Team workbook published
- [ ] On-call runbook links from every alert

## CI/CD
- [ ] OIDC federated credentials (no client secret in GitHub)
- [ ] Manual approval gate on prod
- [ ] Self-approval blocked
- [ ] Rollback workflow tested
