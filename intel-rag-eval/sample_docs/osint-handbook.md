# Sentinel Intelligence Bureau — OSINT Concierge Handbook

The **Sentinel Intelligence Bureau (SIB) OSINT Concierge** is the bureau's
analyst-facing chat assistant for triaging open-source signals. This
handbook answers the most common analyst questions about how to use it.

All material in this document is unclassified. The Concierge is approved
for routine OSINT triage tasks only — it is not authorized to ingest,
process, or output classified information.

## Access and accounts

**Do I need an account to use the Concierge?** Yes. Every analyst uses
their existing SIB single-sign-on account; the Concierge inherits group
membership and audit logging from SSO.

**Can the Concierge be used from a personal device?** No. The Concierge
is approved only on bureau-issued endpoints inside the SIB enclave.

**Who do I contact for access issues?** The OSINT Modernization team
maintains the Concierge. Open a ticket in the bureau help desk; tag it
`osint-concierge`.

## Tasking

**What kinds of questions are appropriate?**

- Summarize recent public reporting on a regional topic.
- Look up a published threat-feed indicator and explain its attributes.
- Help draft an unclassified analyst summary from a Concierge-retrieved
  passage.
- Quick analyst math (rate changes, percent shifts, headcount ratios).

**What is NOT appropriate?**

- Tasking that requires classified inputs or outputs.
- Tasking that asks the Concierge to make an attribution decision
  unilaterally (see `attribution-policy.md`).
- Tasking that asks the Concierge to take action on a system outside
  its sandbox (no IT operations, no collection tasking).

## Live help

OSINT Modernization runs analyst office hours every Tuesday at 1400 EST.
Drop in on the bureau-internal video bridge — no agenda needed.

## Bug reports

The Concierge logs every interaction. To report a bad answer, click the
**Flag response** button next to the assistant message and include the
nearest cited source filename. The OSINT Modernization team reviews
flagged responses each business day.
