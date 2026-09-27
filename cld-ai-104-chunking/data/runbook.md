# Orion Analytics On-Call Runbook

## Section 1 — Severity Classification

Severity-1 (Sev-1) outages are incidents that prevent core workflow for a substantial fraction of users, or any incident with a security breach dimension. SLA: 15-minute initial response, 4-hour resolution target. Escalation manager must be paged at the 2-hour mark if resolution is not on track. Post-incident review is required within 48 hours.

Severity-2 (Sev-2) issues affect a subset of users or a non-critical feature. SLA: 1-hour response, 24-hour resolution. Escalation to senior on-call is optional but recommended for anything blocking a paying Enterprise customer.

Severity-3 (Sev-3) covers minor bugs, cosmetic issues, and non-blocking feature requests. SLA: 4-hour response, 72-hour resolution. Usually handled during the next business day.

## Section 2 — Escalation Procedures

For Sev-1, the on-call engineer creates a war room in Slack (#incident-{id}) and pages the incident commander. Every 30 minutes an update goes to #status-internal. The incident commander decides when to notify affected customers (usually within the first hour). Do not communicate outward without incident commander approval — status page updates are the incident commander's job.

For Sev-2, the on-call engineer creates a ticket in the incident tracker but does not need a Slack war room. Customer communication is direct (via the account CSM) rather than a status page update.

## Section 3 — Refund Authority

Support engineers may issue goodwill credits of up to $200 per incident for platform-caused outages without additional approval. Credits between $200 and $1000 require a CSM sign-off. Credits above $1000 require a manager approval.

Full refunds (as opposed to credits) require reading the customer's contract first. Enterprise contracts have custom refund terms defined in the MSA. Consumer refunds follow the standard 30-day policy: full refund within 30 days of initial subscription, prorated afterwards, no refund on cancelled or suspended accounts.

## Section 4 — Data Residency

Customer PII must remain in-region. EU customers' data lives in eu-west-1; US customers in us-east-1; APAC customers in ap-southeast-2. Cross-region transfers require a signed DPA and legal review. Never move customer data across regions without written approval logged in the compliance tracker.

## Section 5 — Post-Incident Review

Every Sev-1 requires a written post-incident review (PIR) within 48 hours. PIR template: timeline, root cause, contributing factors, corrective actions, prevention plan. PIRs are shared with the affected customer's CSM before the customer is notified of the root cause.
