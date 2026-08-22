# APL-3016 Lesson 6 — Build a generative AI chat app in Python

Python scaffold for the first Lesson-6 hands-on of AI-3016 (APL-3016 prep). You will complete the TODOs in `src/chat-app.py` (sync) and `src/chat-async.py` (streaming, async) to turn a Margie's Travel sales-assistant idea into a working chat CLI backed by your Foundry `gpt-5.2` deployment. Everything is `DefaultAzureCredential` end-to-end — no API keys.

## Scenario

Margie's Travel is a boutique travel agency whose sales agents need an AI assistant they can trust. In Lesson 2 you provisioned a Foundry project and deployed `gpt-5.2`. In this lesson you write the first version of Margie's chat assistant: a Python CLI the sales team can prompt for destination ideas, itineraries, and follow-up questions. Later lessons ground it against Margie's brochures and evaluate it against a real question set — this lesson gets the plumbing right.

## Files

```
apl-3016-chat/
  README.md              # this file
  .env.example           # AZURE_OPENAI_ENDPOINT + MODEL_DEPLOYMENT placeholders
  .gitignore             # keep .env, __pycache__, .venv, editor cruft out of source
  requirements.txt       # reference manifest — every package ships in the python-ai container
  src/
    verify_env.py        # 30-line smoke test: reads .env, one auth+chat round-trip, exits 0/1
    chat-app.py          # sync scaffold with TODOs (Lesson 6 exercises 3+4)
    chat-async.py        # async streaming scaffold with TODOs (Lesson 6 exercise 5)
```

## How to run

1. In the container terminal: `az login --use-device-code`. Complete the device-code sign-in in your local browser using the credentials the lab supplies, then `az account show` to confirm the pre-provisioned subscription is selected.
2. Copy `.env.example` to `.env` and fill in the two values from the lab's environment tab. `AZURE_OPENAI_ENDPOINT` is your Foundry project endpoint (ends in `/api/projects/<project-name>`); `MODEL_DEPLOYMENT` is the deployment name you (or the ARM template) picked for `gpt-5.2` (`gpt-5-2-margie` by default).
3. `python src/verify_env.py`. A green "hello from Margie's Travel" reply means `.env` + auth + deployment all reach; anything else means fix the smallest broken piece before touching the chat app.
4. Complete the `# TODO` markers in `src/chat-app.py`, then run `python src/chat-app.py` and hold a real conversation with your deployment.
5. Complete the `# TODO` markers in `src/chat-async.py`, then run `python src/chat-async.py` to see streaming responses.

## Authentication

Every lab in this course authenticates through `DefaultAzureCredential` — no API keys. The pre-provisioned credential `azureaiuser` is granted the **Foundry User** role (assigned by role GUID `53ca6127-db72-4b80-b1b0-d745d6d5456d`, not by name, so the ongoing Azure AI User → Foundry User rename does not affect provisioning). Foundry User is enough to call the chat completions endpoint on your deployment. `verify_env.py`, `chat-app.py`, and `chat-async.py` all use `azure.identity.get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")` to mint bearer tokens on demand — the same pattern the Microsoft Learning `mslearn-ai-studio` labs teach.

## Notes

**Env-var naming — deviation from the SkillMeUp canonical.** This course pins `AZURE_OPENAI_ENDPOINT` and `MODEL_DEPLOYMENT` to match Microsoft Learning's `mslearn-ai-studio` repo verbatim, so candidates studying from both sources never translate variable names. The SkillMeUp house convention on newer starters is `AZURE_AI_PROJECT_ENDPOINT` + `AZURE_AI_CHAT_DEPLOYMENT` — every other current course uses those. If you copy this starter as a template for a future non-APL-3016 course, switch to the canonical `AZURE_AI_*` names.

**Foundry endpoint shape.** The `OpenAI` client's `base_url` is `f"{AZURE_OPENAI_ENDPOINT}/openai/v1"` — the `/openai/v1` suffix is required. Foundry accepts standard OpenAI SDK calls at that base URL against your project endpoint.

**Model pin.** `gpt-5.2` version `2025-12-11` — GA, Data Zone Standard SKU. Downstream lessons and the APL-3016 assessment assume this deployment; do not change the model version.

**`azure-ai-inference` is retired.** As of 2026-05-30 the standalone inference SDK is retired. This starter (and the whole course) uses the `openai` package with `azure-identity` for bearer minting. If a tutorial or blog post you find still imports `azure.ai.inference`, it is stale — ignore it.
