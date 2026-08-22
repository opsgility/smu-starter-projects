# APL-3016 Lesson 2 — Create a Foundry project and deploy your first model

Minimal starter for the first hands-on lab of AI-3016 (APL-3016 prep). You will not write Python in this lesson — the whole exercise is portal + VS Code extension. The Foundry Toolkit extension you install here becomes your primary window into the Foundry project the platform pre-provisioned for you.

## Scenario

Margie's Travel is a boutique travel agency whose sales agents need an AI assistant they can trust. You have joined Margie's team as the AI engineer. Before you can build anything, you need a Foundry project and a chat model deployed inside it. This lesson gets you there.

## Files

```
apl-3016-foundry-toolkit/
  README.md            # this file
  .env.example         # placeholders for the endpoint + deployment name you'll capture from the portal
  .gitignore           # keep .env, __pycache__, .venv, editor cruft out of source
```

No `requirements.txt`, no `src/`, no source code — the container already ships everything you need, and this lesson does not exercise the SDK.

## How to run

1. Open a terminal in the lab environment: `az login --use-device-code`. Complete the device code sign-in in your local browser using the credentials the lab supplies. Then `az account show` to confirm the pre-provisioned subscription is selected.
2. Open the Extensions panel in VS Code and install **Azure AI Foundry** (the Foundry Toolkit — publisher `ms-toolsai`).
3. Sign the extension in to the same account, expand your Foundry project, and follow the lesson's exercise to deploy `gpt-5.2` (version `2025-12-11`).
4. Copy the endpoint URL and the deployment name from the portal into a local `.env` (copy `.env.example` to `.env` first). You will use these values in every downstream lesson.

## Authentication

Every lab in this course authenticates through `DefaultAzureCredential` — no API keys. The pre-provisioned credential `azureaiuser` is granted the **Foundry User** role at Foundry-project scope (assigned by role GUID `53ca6127-db72-4b80-b1b0-d745d6d5456d`, not by name, so the ongoing Azure AI User → Foundry User rename does not affect provisioning). Foundry User is enough to deploy models, call the Responses API, and use the built-in tools. The fine-tune-deploy step in Lesson 10 needs Foundry Owner — that lesson uses a pre-created resource group so the platform grants Owner at RG scope without ever putting Owner on the credential itself.

## Notes

**Env-var naming — deviation from the SkillMeUp canonical.** This course pins `AZURE_OPENAI_ENDPOINT` and `MODEL_DEPLOYMENT` to match Microsoft Learning's `mslearn-ai-studio` repo verbatim, so candidates studying from both sources never have to translate variable names between the two. The SkillMeUp house convention on newer starters is `AZURE_AI_PROJECT_ENDPOINT` + `AZURE_AI_CHAT_DEPLOYMENT` — every other current course uses those. If you copy this starter as a template for a future course that isn't APL-3016 exam-prep, switch to the canonical `AZURE_AI_*` names.

**Model pin.** `gpt-5.2` version `2025-12-11` — Data Zone Standard SKU, GA, no access request. Confirm the version in the model card before deploying; picking a different `gpt-5.x` breaks the exam-day screenshots you will encounter in downstream lessons.

**Foundry Toolkit is one path.** The toolkit gives you the fastest visual view of your project. You can also do everything through the Foundry portal at `ai.azure.com`; both surfaces call the same underlying REST API. Downstream lessons drop the toolkit and go straight to Python.
