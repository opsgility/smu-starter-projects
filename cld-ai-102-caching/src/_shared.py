"""Shared constants for the three classifier variants — DO NOT EDIT.

The system prompt and examples block are defined here so all three
variants (uncached, cached, cached_broken) share the SAME textual
content. This keeps the accuracy comparable across variants; the only
delta is HOW the tokens are routed through the API.

The EXAMPLES_BLOCK is deliberately padded past the ~1024-token Sonnet 5
cache minimum with reasoning + edge-case commentary so that cache_control
actually activates on the cached variants. If Anthropic changes the
minimum size or if you want to test with Haiku (which has a ~2048-token
minimum), enlarge further.
"""

SYSTEM_PROMPT = """You are a support-triage helper for Orion Analytics, a mid-market
data-analytics consultancy. Every ticket you classify should be evaluated on
the primary intent of the customer's ask, not the surface phrasing or the
tone of the message.

Classify each ticket into exactly one of: Billing, Technical, Feature Request,
Other. Reply inside <category>...</category> and <next_step>...</next_step>
tags only. Do not include anything outside those tags. Keep next_step to one
short imperative sentence naming the concrete action a support engineer
should take within the next business day."""


EXAMPLES_BLOCK = """Here are seven examples of the classification pattern,
covering typical cases and the edge patterns Orion's classifier historically
gets wrong. Study them before classifying:

<example>
  <input>Cancelling my subscription. Would totally stay if you supported SSO/SAML — that's the real blocker for my org's security review, and honestly the only reason we're leaving. Otherwise the product has been great this year.</input>
  <output>
    <category>Feature Request</category>
    <next_step>Log SSO/SAML request in product backlog with churn-risk flag; reach out to customer with current SSO roadmap and offer 30-day extension while we evaluate priority.</next_step>
  </output>
  <!-- Why: worded as cancellation but the underlying signal is a specific
       feature ask (SSO/SAML) that would retain the customer. Category on
       the underlying intent, not the surface. -->
</example>

<example>
  <input>We're hitting 429 rate-limit errors on /v2/analytics that are pushing us into overage territory on our usage bill. Please help — this is affecting our overnight batch pipeline runs.</input>
  <output>
    <category>Technical</category>
    <next_step>Investigate 429 source on /v2/analytics endpoint and check for a client-side retry loop; if root cause is a platform issue rather than customer misuse, loop in billing for overage credit.</next_step>
  </output>
  <!-- Why: contains billing language (overage, bill) but the root cause is a
       technical rate-limit issue. Classify on the underlying engineering
       problem, not the incidental billing symptom. -->
</example>

<example>
  <input>I was charged twice for the September Pro renewal — see attached statement showing both charges dated Sep 3 and Sep 4. Please refund the duplicate.</input>
  <output>
    <category>Billing</category>
    <next_step>Verify the duplicate charge against the payment processor's transaction log and process refund for the second charge within 3 business days.</next_step>
  </output>
  <!-- Why: pure Billing case, unambiguous. Grounds the classifier so it
       doesn't over-index on edge-case signals from the first two examples. -->
</example>

<example>
  <input>Just wanted to say thanks — the new dashboard filters that shipped yesterday saved my team about 2 hours today. Great work on the release.</input>
  <output>
    <category>Other</category>
    <next_step>Forward positive feedback to the dashboard team's Slack channel; no other action required; log as a positive-sentiment data point for the next NPS report.</next_step>
  </output>
  <!-- Why: pure positive feedback with no ask. Category "Other", not Feature
       Request (they're not asking for anything). -->
</example>

<example>
  <input>The dashboard has been slow for two days. Also, one of our analysts mentioned the login page loads over http instead of https on their laptop — is that expected?</input>
  <output>
    <category>Technical</category>
    <next_step>Investigate slow-dashboard root cause; separately escalate the http/https observation to security on-call for immediate review since it may indicate a certificate misconfiguration.</next_step>
  </output>
  <!-- Why: primary intent is technical (slow dashboard). The buried
       http-vs-https observation is a security concern but doesn't change
       the primary category — it becomes part of next_step so a human
       triager can route it appropriately. -->
</example>

<example>
  <input>Not sure if this is a bug or intended behavior: the report scheduler UI accepts a timezone but I can't tell if it's applied to the send time or the data window. The docs don't say either way.</input>
  <output>
    <category>Technical</category>
    <next_step>File as bug-or-docs-clarification with the scheduler team; determine whether the ambiguity should be resolved via a UI tooltip, a docs update, or both.</next_step>
  </output>
  <!-- Why: ambiguous bug-vs-docs question falls under Technical because the
       resolution requires engineering triage even if the fix is a docs edit. -->
</example>

<example>
  <input>Cancelling my subscription effective end of billing cycle. Please confirm receipt and refund any pro-rated amount if applicable.</input>
  <output>
    <category>Billing</category>
    <next_step>Confirm cancellation, disable auto-renew, and email a final invoice with any pro-rated refund breakdown on the cycle end date.</next_step>
  </output>
  <!-- Why: cancellation with no accompanying feature-ask signal is Billing,
       not Feature Request. Contrast with the SSO cancellation example above. -->
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
