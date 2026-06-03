# Sentinel Intelligence Bureau — OSINT Concierge Handbook

The **Sentinel Intelligence Bureau (SIB) OSINT Concierge** is the bureau's
analyst-facing chat assistant for triaging open-source signals. This handbook
answers the most common analyst questions about how to use it.

All material in this document is unclassified. The Concierge is approved
for routine OSINT triage tasks only — it is not authorized to ingest,
process, or output classified information.

## Access and accounts

Analysts use their existing SIB single-sign-on account; the Concierge
inherits group membership and audit logging from SSO. The Concierge is
approved only on bureau-issued endpoints inside the SIB enclave.

For access issues, open a ticket in the bureau help desk; tag it
`osint-concierge`. The OSINT Modernization team triages these tickets
each business day.

## Tasking

**Appropriate tasks:**

- Summarize recent public reporting on a regional topic.
- Look up a published threat-feed indicator and explain its attributes.
- Help draft an unclassified analyst summary from a Concierge-retrieved
  passage.
- Quick analyst math (rate changes, percent shifts, headcount ratios).

**Not appropriate:**

- Tasking that requires classified inputs or outputs.
- Tasking that asks the Concierge to make an attribution decision
  unilaterally (see `attribution-policy.md`).
- Tasking that asks the Concierge to take action on a system outside its
  sandbox (no IT operations, no collection tasking).

## Live help

OSINT Modernization runs analyst office hours every Tuesday at 1400 EST
on the bureau-internal video bridge — no agenda needed.
