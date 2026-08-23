# AI-3026 Lesson 4 — Give your agent a custom function tool

Python starter for the Halcyon Assist adjuster claim-drafter agent. You add a `lookup_policy_summary` function tool so the agent can pull real policy details when it drafts responses to open claims.

## Scenario

Halcyon's adjusters need the intake-triage agent (built in L2) to draft a first-response paragraph on every new claim. That draft has to cite the actual deductible, coverage limits, and rider set from the policyholder's contract — which lives in `data/halcyon-policies.json` in this starter (simulating the real Halcyon Policy Admin System). You register a Python function as a `FunctionTool` on a Foundry agent and watch it call the function on demand.

## Files

```
ai3026-custom-tools/
  README.md
  .env.example              # FOUNDRY_PROJECT_ENDPOINT + FOUNDRY_MODEL
  .gitignore
  requirements.txt          # Reference — every package preinstalled in the lab container.
  src/
    verify_env.py           # Smoke test — one AIProjectClient round-trip, exits 0/1.
    agent_with_tool.py      # Skeleton with TODO markers for the lesson's build steps.
  data/
    halcyon-policies.json   # 6 fake Halcyon policies the FunctionTool reads from.
```

## How to run

1. `az login --use-device-code`
2. Copy `.env.example` → `.env` and fill in from the lab's Cloud Details tab.
3. `python src/verify_env.py` — confirms your bearer token reaches the Foundry project.
4. Complete the TODO markers in `src/agent_with_tool.py` and run it: `python src/agent_with_tool.py`.

## Authentication

`DefaultAzureCredential` end-to-end. The lab provisions the `azureaiuser` credential with the **Foundry User** role — enough to build agents, register tools, and invoke them.

## Notes

- **Env-var naming deviates from SkillMeUp canonical.** `FOUNDRY_PROJECT_ENDPOINT` + `FOUNDRY_MODEL` follows the newest MS Learn convention (mslearn-ai-agents repo, verified Aug 2026). AI-3016 uses `AZURE_OPENAI_ENDPOINT` + `MODEL_DEPLOYMENT`; the SkillMeUp canonical is `AZURE_AI_*`. Deliberate divergence for exam-prep parity with MS Learn.
- **Model pin:** `gpt-5` version `2025-08-07`.
- **`requirements.txt` is manifest-only.** All packages already installed in the `python-ai` lab container.
- **Halcyon policies are fictional.** No real customer data.
