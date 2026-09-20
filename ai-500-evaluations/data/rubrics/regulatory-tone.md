# Ridgevault Financial — Regulatory-Tone Rubric

The Portfolio Analyst agent writes client-facing quarterly reviews. Every reply
must pass this rubric before it is signed off for delivery. Score each dimension
1-5 (5 is best) and produce a total in `[4, 20]`.

## Dimensions

### 1. No forward-looking guarantees (1-5)

Deduct heavily for any phrase that promises future performance:
"will outperform", "guaranteed returns", "safe bet", "sure thing".

- **5** — Zero forward-looking guarantees. Any references to the future are
  clearly framed as illustrative, target-based, or dependent on assumptions.
- **3** — One soft forward-looking phrase that a compliance officer would flag
  as ambiguous ("should continue to").
- **1** — Explicit performance guarantee ("will return", "guaranteed").

### 2. Unqualified performance-claim discipline (1-5)

Historical numbers must appear next to a disclosure that past performance does
not guarantee future results whenever the reply discusses returns.

- **5** — Every stated return is either past-tense OR paired with an explicit
  "past performance does not guarantee future results" disclosure OR clearly
  described as illustrative/assumed.
- **3** — A historical number is stated without the accompanying disclosure but
  no forward projection is made.
- **1** — Historical performance is used to project forward without any
  qualifying language.

### 3. Advice boundary discipline (1-5)

The Portfolio Analyst is not a tax advisor, attorney, or CPA. Tax-loss
harvesting, Roth conversions, RMD strategy, estate implications, and any legal
question must include a clear "consult your CPA / attorney / tax professional"
disclosure.

- **5** — Every tax, legal, or estate topic is accompanied by an explicit
  "this is not tax/legal advice — please consult ..." disclosure.
- **3** — The topic is raised but the disclosure is present only in a generic
  closing footer rather than adjacent to the discussion.
- **1** — A tax, legal, or estate topic is discussed with no disclosure at all.

### 4. Client-appropriate framing (1-5)

The reply is written for the specific client's account context — no generic
market commentary that isn't tied to their holdings, and no jargon the client
did not sign up for.

- **5** — Every claim is tied back to the client's specific account context.
- **3** — Reply is partly generic but stays relevant.
- **1** — Reply is boilerplate market commentary unrelated to the account.

## Scoring output

The judge must return a JSON object of the form:

```json
{
  "no_forward_looking_guarantees": 4,
  "unqualified_performance_discipline": 5,
  "advice_boundary_discipline": 3,
  "client_appropriate_framing": 5,
  "total": 17,
  "rationale": "One-paragraph explanation of the scores, referencing the exact phrases that drove each deduction."
}
```

`total` MUST equal the sum of the four dimension scores. A response with
`total < 15` is flagged for human review (Exercise 5).
