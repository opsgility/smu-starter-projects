# AI-500 Lesson 17 — Multi-intervention guardrails and custom validators

Wire a four-layer guardrail stack around Ridgevault Financial's portfolio-review flow, then gate every future change on a red-team regression suite. You start with an unprotected `portfolio_flow_with_guardrails.py` (the same flow shape you sketched in Lesson 1 + built out in Lesson 5), plus four empty middleware stubs — one per interception point — and one JSONL red-team set. Across the exercises you fill each middleware in, wire them into the flow, then run the CI-style regression and inspect the per-category pass rate.

## Scenario

Ridgevault Financial's Advisor Agent sits between wealth-management clients and their portfolios. It already answers questions and calls the `portfolio_lookup` + `client_record` tools — but it has no defensive perimeter. A jailbreak that slips a naive input filter reaches a real tool call; an over-returning tool leaks a client SSN into the model's context; the model can (and has, in staging) drafted "guaranteed return" copy that Ridgevault's compliance officer, Ridge, categorically forbids. In this lesson you build all four guardrail layers — input, tool-arg, tool-result, output-response — and then prove they work by red-teaming the assembled flow against a labeled attack set that CI can enforce on every pull request.

## Files

```
ai-500-guardrails/
  README.md
  .env.example                                    # Foundry + Content Safety + Language endpoints
  .gitignore
  requirements.txt                                # Reference manifest — every package already in the lab container.
  src/
    verify_env.py                                 # Smoke test — reads .env, one auth round-trip against Foundry.
    guardrails/
      input_content_safety.py                     # TODO exercise 2 — ChatMiddleware, L1 (Content Safety + Prompt Shields).
      tool_arg_validator.py                       # TODO exercise 3 — FunctionMiddleware, L2 (account-number regex + rules).
      tool_result_pii_redact.py                   # TODO exercise 4 — FunctionMiddleware, L3 (Azure AI Language PII).
      response_grounding_check.py                 # TODO exercise 5 — ChatMiddleware, L4 (grounding + regulatory blocklist).
    portfolio_flow_with_guardrails.py             # The Ridgevault Advisor flow. Middleware wire-up TODO in exercises 2-5.
    tests/
      red_team_set.jsonl                          # Labeled attack + benign-control prompts consumed by exercise 6.
```

## How to run

1. Sign in with a device code so the container (which has no browser) can complete Entra auth:

   ```
   az login --use-device-code
   ```

   The device-code URL is `https://microsoft.com/devicelogin`.

2. Copy the env template and fill in the four endpoints printed on the lab's Environment tab (the ARM template attached to this lab emits `FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL`, `CONTENT_SAFETY_ENDPOINT`, and `LANGUAGE_ENDPOINT` as outputs):

   ```
   cp .env.example .env
   ```

3. Confirm your identity + deployment reach Foundry:

   ```
   python src/verify_env.py
   ```

   Expect `OK: gpt-5 replied: ...`. If it complains about placeholders, edit `.env`; if it 401s, verify `azureaiuser` has the **Foundry User** + **Cognitive Services User** roles (the lab environment grants these automatically at start).

4. Complete the TODOs in `src/guardrails/*.py` in the order the exercises walk you through, then run the assembled flow end-to-end:

   ```
   python -m src.portfolio_flow_with_guardrails
   ```

5. Run the CI-style regression:

   ```
   python -m src.portfolio_flow_with_guardrails --redteam src/tests/red_team_set.jsonl
   ```

   The last line prints the per-category pass rate. Ridge's promotion gate is 100% on `direct_injection`, `pii_exfil`, `regulatory`, and `tool_arg_injection`; ≥95% on `hallucination`; ≥95% pass on `benign_control` (false-positive rate below 5%).

## Authentication

Every reach for a model, Content Safety, or Language service goes through `DefaultAzureCredential` — no API keys ever touch the code. The lab environment binds credential `azureaiuser` to **Foundry User**, **Cognitive Services User**, **Cognitive Services OpenAI User**, and **Contributor** at subscription scope. Cognitive Services User is what lets the middleware call `text:analyze`, `text:shieldPrompt`, and `text:detectGroundedness` on the Content Safety account, and the PII entity-recognition endpoint on the Language account — all keyless, all via managed identity.

## Notes

- **Do not run `pip install`.** The `python-ai` container variant already ships `agent-framework`, `azure-ai-projects`, `azure-ai-contentsafety`, `azure-ai-textanalytics`, `azure-identity`, `openai`, `httpx`, and `python-dotenv`. `requirements.txt` is a reference manifest so local dev works if you clone the starter outside the lab environment.
- **Never hardcode the model name.** Always read from `os.environ["FOUNDRY_MODEL"]`. Model versions rotate quarterly — the env-var indirection keeps the code future-proof.
- **All four guardrails fail closed.** If a detector call raises (timeout, 5xx from Content Safety), the middleware propagates the exception instead of allowing the request through. That is a Ridge compliance non-negotiable — never `try/except` around a detector call and continue.
- **The red-team set is deliberately small so it runs in-lab.** Ridgevault's real production set is ~230 prompts across 8 categories. The starter's set gives you at least three prompts per category so per-category pass-rate math is meaningful without waiting 4+ minutes for every regression run.
- **You are wiring the SAME agent flow four times, once per layer.** By exercise 5 the middleware list on the `ChatAgent` reads `[input_cs, tool_arg, tool_result, response_ground]` in that exact order — the order matters because L1 short-circuits before L2 even sees the tool call.
