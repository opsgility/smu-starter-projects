# AI-3026 Lesson 2 — Build your first agent in portal + VS Code

Portal-first starter for the Halcyon Assist intake-triage agent. No Python source ships here — Lesson 2 has you build the agent entirely in the Microsoft Foundry portal, then attach the Foundry Toolkit VS Code extension to iterate locally.

## Scenario

Halcyon Insurance is a mid-sized property + auto carrier building an agent platform to modernize claims operations. The first agent in the Halcyon Assist stack is the **intake-triage agent** — it categorizes each new claim submission into `auto`, `property`, `liability`, or `other` so the right specialist can pick it up. You build it in the Foundry portal (no code) and hit it from the Foundry Toolkit VS Code extension.

## Files

```
ai3026-portal-and-vscode/
  README.md
  .env.example         # FOUNDRY_PROJECT_ENDPOINT + FOUNDRY_MODEL, filled in from lab-provided values
  .gitignore           # Python (in case you add exploratory Python during the lesson)
```

## How to run

1. `az login --use-device-code` — sign in with the lab-provided credentials.
2. Copy `.env.example` → `.env` and fill in the two values from the lab's Cloud Details tab (`FOUNDRY_PROJECT_ENDPOINT` is emitted by the ARM template's output).
3. Open the Foundry portal at the URL in `FOUNDRY_PROJECT_ENDPOINT` — your project is already provisioned with `gpt-5` deployed.
4. Build the agent in the portal per the exercise instructions.
5. Install the **Foundry Toolkit** VS Code extension from the Extensions view inside this container.
6. Sign the toolkit into your Foundry project and hit the agent from the toolkit playground.

## Authentication

Everything goes through `DefaultAzureCredential` — the lab provisions the `azureaiuser` credential with the **Foundry User** role at the subscription scope. No API keys.

## Notes

- **Env-var naming deviates from SkillMeUp canonical.** This course uses `FOUNDRY_PROJECT_ENDPOINT` + `FOUNDRY_MODEL` — the newest Microsoft Learn convention as of Aug 2026 (see the `mslearn-ai-agents` repo). AI-3016 uses `AZURE_OPENAI_ENDPOINT` + `MODEL_DEPLOYMENT`; SkillMeUp's canonical prefix is `AZURE_AI_*`. The naming difference is deliberate — exam candidates who study from MS Learn material will see `FOUNDRY_PROJECT_ENDPOINT` there.
- **Model pin:** `gpt-5` version `2025-08-07` (matches MS Learn `mslearn-ai-agents` repo verbatim). Different from AI-3016's `gpt-5.2` pin.
- **No Python source in this starter.** Lesson 4 introduces the `azure-ai-projects` SDK; that starter (`ai3026-custom-tools`) is where the code begins.
