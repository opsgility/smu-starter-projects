# AI-3026 Lesson 12 (capstone) — Multi-agent solution with sequential + A2A

Python capstone starter for the Halcyon Assist claims-triage pipeline. Orchestrates three specialist agents — two local (coverage_agent, adjuster_brief_agent) and one remote via the **Agent-to-Agent (A2A) protocol** (damage_assessment_server). Combines patterns from MS Learn exercises 08 (SequentialBuilder) and 09 (A2A federation).

## Scenario

The Halcyon claims-triage pipeline runs on every new claim: (1) verify coverage against the policy, (2) assess damage severity and photos, (3) draft the adjuster's first-touch brief. Each stage is a specialist agent — different system prompts, different tools, different runtime SLAs — and Halcyon's damage-assessment team runs their own service (`damage_assessment_server`) that the pipeline consumes over A2A. This capstone builds the whole thing end-to-end.

## Files

```
ai3026-multi-agent-capstone/
  README.md
  .env.example
  .gitignore
  requirements.txt          # Reference — all installed in the lab container.
  src/
    verify_env.py           # Smoke test — FoundryChatClient round-trip.
    orchestrator.py         # SequentialBuilder wiring the 3 specialists.
    specialists/
      coverage_agent.py             # Local Agent Framework agent.
      adjuster_brief_agent.py       # Local Agent Framework agent.
      damage_assessment_server.py   # A2A server (A2AStarletteApplication) — runs as its OWN process.
  data/
    test-claim.json         # One complete Halcyon claim payload.
```

## How to run

1. `az login --use-device-code`
2. Copy `.env.example` → `.env`.
3. `python src/verify_env.py`
4. **Terminal 1** — start the remote A2A server: `python src/specialists/damage_assessment_server.py`
5. **Terminal 2** — run the orchestrator: `python src/orchestrator.py`

## Authentication

`DefaultAzureCredential` for everything Foundry-side. The A2A protocol on localhost is unauthenticated in this starter — production would front the A2A endpoint with mTLS.

## Notes

- **Env-var naming deviates from SkillMeUp canonical** — same `FOUNDRY_PROJECT_ENDPOINT` + `FOUNDRY_MODEL` pattern as the other AI-3026 starters.
- **Model pin:** `gpt-5` version `2025-08-07`.
- **`requirements.txt` reference-only.** `agent-framework`, `agent-framework-foundry`, and `starlette` are preinstalled in `python-ai`.
- **`starlette` is why we rebuilt the `python-ai` container on 2026-08-23** — it wasn't there before this course.
- **Fault-injection exercise** — the capstone finishes with killing the A2A server mid-flight to see how the orchestrator handles the remote-agent failure. Kill it with Ctrl+C in Terminal 1 during Exercise 6.
