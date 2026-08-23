# AI-3026 Lesson 8 — Add Foundry IQ RAG to an agent

Python starter for the Halcyon Assist policy-retrieval agent. You upload 4 Halcyon policy documents to a Foundry IQ vector index, attach the index to an agent, and watch the agent answer coverage questions with real citations instead of plausible-sounding hallucinations.

## Scenario

Halcyon's adjusters constantly get "what does this policy actually cover?" questions from claimants — deductibles, exclusions, riders, waiting periods. Reading the whole policy PDF at claim time is slow; asking the LLM without grounding produces confident-but-wrong answers. In L8 you index Halcyon's 4 core policy documents into **Foundry IQ** (Foundry's native vector store), attach the index to an agent, and see the difference between grounded and ungrounded responses side-by-side.

## Files

```
ai3026-foundry-iq/
  README.md
  .env.example
  .gitignore
  requirements.txt          # Reference — all installed in the lab container.
  src/
    verify_env.py           # Smoke test.
    index_policies.py       # Bulk-upload policies/*.md into a Foundry IQ index.
    policy_agent.py         # Foundry agent with the IQ index attached.
  policies/
    halcyon-umbrella-gold.md      # ~500 words — Halcyon Umbrella Gold policy
    halcyon-auto-silver.md        # ~500 words — Halcyon Auto Silver policy
    halcyon-property-basic.md     # ~500 words — Halcyon Property Basic policy
    halcyon-umbrella-platinum.md  # ~500 words — Halcyon Umbrella Platinum policy
```

## How to run

1. `az login --use-device-code`
2. Copy `.env.example` → `.env`.
3. `python src/verify_env.py`
4. `python src/index_policies.py` — uploads the 4 policies + waits for indexing to complete.
5. `python src/policy_agent.py` — queries the agent with grounded vs ungrounded modes.

## Authentication

`DefaultAzureCredential` end-to-end. The `azureaiuser` credential's Foundry User role covers both index writes and agent runs.

## Notes

- **Env-var naming deviates from SkillMeUp canonical.** `FOUNDRY_PROJECT_ENDPOINT` + `FOUNDRY_MODEL` + `FOUNDRY_IQ_INDEX` per MS Learn's newest convention.
- **Model pin:** `gpt-5` version `2025-08-07`.
- **Policies are fictional.** No real customer data.
- **First indexing run is slow** — Foundry IQ needs 30-60s per document to embed + index. Subsequent queries are near-instant.
- **Grounded vs ungrounded** — L8's Exercise 5 asks the same question with and without the IQ tool attached; the ungrounded run typically invents plausible-sounding but wrong numbers.
