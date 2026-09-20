# AI-3026 Lesson 10 — Build an Agent Framework chat agent

Python starter for the Halcyon Assist expense reimbursement agent, built with the **Microsoft Agent Framework** (GA 1.0 as of 2026-04). This is your first lesson on the second SDK track — L2-L8 used the Foundry Agent Service SDK (`azure-ai-projects`); L10-L12 use `agent-framework-foundry`.

## Scenario

Halcyon's adjusters submit expense reports for mileage, meals, and lodging while working claims in the field. The intake app already ingests the raw expense lines; L10 builds an **expense categorization agent** that classifies each line, applies Halcyon's reimbursement rules (per diem caps, mileage rate, receipt-required threshold), and drafts an approval or clarification message. It's a great fit for the Agent Framework because you'll extend it into multi-agent workflows in L12.

## Files

```
ai3026-agent-framework/
  README.md
  .env.example
  .gitignore
  requirements.txt          # Reference — all installed in the lab container.
  src/
    verify_env.py           # Smoke test — FoundryChatClient round-trip.
    expense_reimbursement_agent.py  # Skeleton with TODO markers.
  data/
    expenses.json           # 5 test expense records.
```

## How to run

1. `az login --use-device-code`
2. Copy `.env.example` → `.env`.
3. `python src/verify_env.py`
4. Complete the TODO markers in `src/expense_reimbursement_agent.py` and run: `python src/expense_reimbursement_agent.py`.

## Authentication

`DefaultAzureCredential` end-to-end. The Microsoft Agent Framework accepts either `DefaultAzureCredential` or `AzureCliCredential` — they're interchangeable here.

## Notes

- **Env-var naming deviates from SkillMeUp canonical.** `FOUNDRY_PROJECT_ENDPOINT` + `FOUNDRY_MODEL` per MS Learn's `mslearn-ai-agents` convention.
- **Model pin:** `gpt-5` version `2025-08-07`.
- **`requirements.txt` reference-only.** `agent-framework` + `agent-framework-foundry` are preinstalled in the `python-ai` container.
- **This is where the SDK track switches.** L9 (teaching) explains when to reach for the Agent Framework vs the Foundry Agent Service SDK — read that first if you haven't.
- **Not the same framework as AI-3016.** AI-3016 uses the OpenAI SDK's Responses API. AI-3026 uses `azure-ai-projects` (L2-L8) and `agent-framework-foundry` (L10-L12).
