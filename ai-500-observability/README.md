# AI-500 Lesson 13 — Tracing, cost optimization, and drift monitoring

Instrument Ridgevault Financial's sequential portfolio-review multi-agent flow with OpenTelemetry, ship traces to Application Insights + Foundry Tracing, attribute token cost per agent turn, apply two cost optimizations to the risk_assessor (prompt compression + response caching), and set a drift alarm on the compliance_officer output distribution.

## Scenario

Ridgevault Financial's five-agent wealth-management platform is running in production. Advisors love the answers, but Finance is asking who's burning tokens, SRE wants an end-to-end trace when an answer feels off, and Compliance wants to know the moment the compliance_officer starts drifting away from its historical response shape. In this lesson you take the existing sequential portfolio-review flow (Portfolio Analyst -> Risk Assessor -> Compliance Officer), wrap it in OpenTelemetry, wire the tracer into both App Insights and Foundry Tracing, attribute prompt+completion tokens per agent turn, apply prompt compression + LRU response caching to the noisy risk_assessor, and alarm on a rolling drop in compliance_officer output length as a proxy for behavior drift.

## Files

```
ai-500-observability/
  README.md
  .env.example                        # Foundry endpoint + model + App Insights connection string + workspace id
  .gitignore
  requirements.txt                    # Reference manifest — every package is already in the lab container.
  src/
    verify_env.py                     # Smoke test — reads .env, one auth+model round-trip, exit 0/1.
    portfolio_flow.py                 # Instrumented sequential 3-agent flow — the code the lab observes.
    tracing/
      otel_setup.py                   # Idempotent OTel setup — App Insights exporter + Foundry Tracing enable.
    cost/
      token_attribution.py            # Extract prompt/completion token counts per turn + tag on the span.
    optimizations/
      prompt_compress.py              # Cheap prompt compression pass for the risk_assessor system prompt.
      response_cache.py               # LRU cache keyed on (agent, prompt_hash) -> completion string.
    drift/
      output_length_alarm.py          # Rolling-window mean/std alarm on compliance_officer output length.
  data/
    test-portfolios.jsonl             # 12 seed portfolios (client id + positions) the flow runs against.
```

## How to run

1. Sign in with a device code so the container (which has no browser) can complete Entra auth:

   ```
   az login --use-device-code
   ```

2. Copy the env template and fill in the four values printed on the lab's Environment tab:

   ```
   cp .env.example .env
   ```

3. Confirm your identity + deployment reach Foundry:

   ```
   python src/verify_env.py
   ```

   Expect `OK: gpt-5 replied: Hello ...`. If it complains about angle-bracket placeholders, edit `.env`; if it 401s, verify `azureaiuser` has the **Foundry User** role on the project (the lab environment grants this automatically at start).

4. Run the instrumented flow once end-to-end to seed traces:

   ```
   python src/portfolio_flow.py
   ```

   Then look at both App Insights (Application Map + End-to-end transaction search) and the Foundry portal's Tracing tab for the same run.

## Authentication

Everything authenticates keyless with `DefaultAzureCredential` -> the `azureaiuser` lab account. The lab environment grants `azureaiuser` the **Foundry User** role on the project + **Cognitive Services OpenAI User** on the Foundry account. No API keys are read anywhere in the starter. `APPLICATIONINSIGHTS_CONNECTION_STRING` is a resource-scoped ingestion string (not a subscription key) — safe to pass through env.

## Notes

- Model name is read from `FOUNDRY_MODEL` — do not hardcode `gpt-5` anywhere. Model versions rotate; a hardcode becomes a course-wide sweep.
- `data/test-portfolios.jsonl` is referenced by name from the agent tool code — do not rename without updating `portfolio_flow.py`.
- `tracing/otel_setup.py` is idempotent (guarded by a module-level flag). Import it once from `portfolio_flow.py` before the first agent call. Calling `configure_observability()` twice is a no-op.
- Cost attribution reads `response.usage.prompt_tokens` / `completion_tokens` from the Foundry chat-completions response and adds them as `gen_ai.usage.input_tokens` / `output_tokens` span attributes — this is the OTel GenAI semantic convention App Insights + Foundry Tracing both recognize.
- The drift alarm is intentionally simple (rolling mean +/- 2 sigma on output character length). It exists to teach the alarm-scaffolding pattern; a production system would layer PSI on top of embeddings.
