"""Shared constants for the three classifier variants — DO NOT EDIT.

The system prompt and examples block are defined here so all three
variants (uncached, cached, cached_broken) share the SAME textual
content. This keeps the accuracy comparable across variants; the only
delta is HOW the tokens are routed through the API.
"""

SYSTEM_PROMPT = """You are a support-triage helper for Orion Analytics.
Classify each ticket into one of: Billing, Technical, Feature Request, Other.
Reply inside <category>...</category> and <next_step>...</next_step> tags only.
Do not include anything outside those tags."""


EXAMPLES_BLOCK = """Here are examples of the classification pattern:

<example>
  <input>Cancelling my subscription. Would totally stay if you supported SSO/SAML — that's the real blocker for my org's security review.</input>
  <output>
    <category>Feature Request</category>
    <next_step>Log SSO/SAML request in product backlog and flag as churn-risk in CRM.</next_step>
  </output>
</example>

<example>
  <input>We're hitting 429 rate-limit errors on /v2/analytics that are pushing us into overage territory on our usage bill.</input>
  <output>
    <category>Technical</category>
    <next_step>Investigate 429 source on /v2/analytics; loop in billing for overage credit if root cause is our end.</next_step>
  </output>
</example>

<example>
  <input>I was charged twice for the September Pro renewal. Please refund the duplicate.</input>
  <output>
    <category>Billing</category>
    <next_step>Verify duplicate charge and process refund within 3 business days.</next_step>
  </output>
</example>

<example>
  <input>Just wanted to say thanks — the new dashboard filters shipped yesterday saved my team 2 hours today.</input>
  <output>
    <category>Other</category>
    <next_step>Forward positive feedback to the dashboard team channel; no other action.</next_step>
  </output>
</example>

<example>
  <input>The dashboard has been slow for two days. Also, one of our analysts mentioned the login page loads over http instead of https on their laptop.</input>
  <output>
    <category>Technical</category>
    <next_step>Investigate slow-dashboard root cause; escalate the http/https issue to security on-call.</next_step>
  </output>
</example>

<example>
  <input>Not sure if this is a bug or intended behavior: the report scheduler UI accepts a timezone but I can't tell if it's applied to the send time or the data window.</input>
  <output>
    <category>Technical</category>
    <next_step>File as bug-or-docs-clarification with the scheduler team.</next_step>
  </output>
</example>

<example>
  <input>Cancelling my subscription effective end of billing cycle. Please confirm.</input>
  <output>
    <category>Billing</category>
    <next_step>Confirm cancellation, disable auto-renew, and email a final invoice on cycle end.</next_step>
  </output>
</example>"""


# Sonnet 5 pricing as of 2026-09-27 (in USD per 1M tokens)
SONNET5_INPUT_PER_MTOK = 3.00
SONNET5_OUTPUT_PER_MTOK = 15.00
SONNET5_CACHE_WRITE_MULT = 1.25   # cache write is ~1.25x normal input rate
SONNET5_CACHE_READ_MULT = 0.10    # cache read is ~0.10x normal input rate


def compute_cost_usd(input_tokens: int, output_tokens: int,
                     cache_read: int = 0, cache_creation: int = 0) -> float:
    """Return the USD cost for one Sonnet 5 call given all four token counts."""
    return (
        input_tokens * SONNET5_INPUT_PER_MTOK / 1_000_000
        + cache_creation * SONNET5_INPUT_PER_MTOK * SONNET5_CACHE_WRITE_MULT / 1_000_000
        + cache_read * SONNET5_INPUT_PER_MTOK * SONNET5_CACHE_READ_MULT / 1_000_000
        + output_tokens * SONNET5_OUTPUT_PER_MTOK / 1_000_000
    )
