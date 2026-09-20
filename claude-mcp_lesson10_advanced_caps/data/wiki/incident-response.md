# Incident Response

Northwind runs 24x7 logistics — so our incident response process is the highest-leverage system we operate.

## Severity definitions

- **Critical** — customer-impacting outage; revenue or safety at risk. Page primary + secondary on-call immediately.
- **High** — degraded service for a meaningful subset of customers. Page primary on-call.
- **Medium** — partial degradation, internal-only or limited customer impact. Slack the team channel.
- **Low** — informational; track in the issue tracker.

## The first ten minutes

1. **Acknowledge the page** within 5 minutes — silence is the worst signal.
2. **Open an incident channel** named `#inc-YYYYMMDD-short-summary`.
3. **Declare a commander** — usually whoever picked up the page. The commander does not type code.
4. **Mitigate first, root-cause later.** Roll back, failover, or feature-flag off as fast as possible.
5. **Communicate every 15 minutes** even if the update is "still investigating".

## After the incident

- Schedule the postmortem within 48 hours.
- The postmortem is blameless and focused on systemic gaps, not individual mistakes.
- Action items must have owners and due dates within two weeks.
