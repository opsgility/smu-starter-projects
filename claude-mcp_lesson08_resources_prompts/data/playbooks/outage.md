# Outage Response Playbook

This is the canonical runbook for responding to a Northwind production outage. If you are reading this because you've been paged, **start here**.

## Step 1 — Confirm the outage is real

- Check Grafana dashboard "Customer Health Top-Level".
- Cross-reference at least one synthetic check failure AND one customer report (or a 5xx-rate spike >1% sustained for >2 minutes).
- If you cannot confirm, downgrade severity and continue investigating.

## Step 2 — Declare and stand up the incident

- Page the secondary on-call.
- Open `#inc-YYYYMMDD-<short-name>` in Slack.
- Drop a `@here` in `#engineering-leadership` with the severity, customer impact summary, and the channel link.
- Designate a commander, scribe, and comms lead. The commander does not write code.

## Step 3 — Mitigate

Try, in order:

1. **Feature flag rollback** — does a flag turn this off? If so, flip it.
2. **Service rollback** — was a deploy in flight? If so, revert via `nw deploy rollback <service>`.
3. **Failover** — failover to the secondary region using `nw failover --region eus2 --to wus2`.
4. **Capacity bump** — if the issue is overload, scale the affected service up by 2x and add an alert to revisit cost the next day.

## Step 4 — Stabilize and communicate

- Post a customer-facing status update on the status page.
- Continue 15-minute updates in `#inc-...`.
- Stand up a post-incident triage meeting for the next morning.

## Step 5 — After the incident

- Schedule the blameless postmortem within 48 hours.
- File action items in the tracker with owners and 2-week due dates.
- Close the incident channel only after the postmortem.
