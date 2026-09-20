# AI-3016 Lesson 6 — Build a generative AI chat app in Python

Skeleton for the Lesson 6 hands-on lab of AI-3016 (APL-3016 prep). You start with a wired-up smoke test and two stub scripts (sync + async), fill in the OpenAI-client construction and the completion call, and end with a streaming chat REPL that talks to a Foundry-hosted `gpt-5.2` deployment as Margie's Travel's on-call assistant.

## Scenario

Margie's Travel is a boutique travel agency whose sales agents need an AI assistant they can trust. In Lesson 2 you already provisioned a Foundry project and deployed `gpt-5.2`. In this lesson you write the first version of the Python client that reaches that model with keyless auth, keeps a rolling conversation state, and streams replies token-by-token so Margie's staff get a snappy chat surface.

## Files

```
apl-3016-chat/
  README.md
  .env.example              # AZURE_OPENAI_ENDPOINT + MODEL_DEPLOYMENT
  .gitignore
  requirements.txt          # Reference manifest — every package is already in the lab container.
  src/
    verify_env.py           # 30-line smoke test — reads .env, one auth+chat round-trip.
    chat-app.py             # Sync REPL. TODOs you fill in exercises 3 + 4.
    chat-async.py           # Async + streaming REPL. TODOs you fill in exercise 5.
```

## How to run

1. Sign in with a device code so the container (which has no browser) can complete Entra auth:

   ```
   az login --use-device-code
   ```

2. Copy the env template and fill in the two values the lab environment prints for you:

   ```
   cp .env.example .env
   ```

3. Confirm your identity + deployment reach Foundry:

   ```
   python src/verify_env.py
   ```

   Expect `OK: gpt-5-2-margie replied: Hello …`. If it complains about placeholders, edit `.env`; if it 401s, verify `azureaiuser` has the **Foundry User** role on the project (the lab environment grants this automatically, but a subscription-selection mismatch will show as 401).

4. Complete the TODOs in `src/chat-app.py` per exercises 3 + 4, then run:

   ```
   python src/chat-app.py
   ```

5. Complete the TODOs in `src/chat-async.py` per exercise 5, then run:

   ```
   python src/chat-async.py
   ```

## Authentication

Every reach for the model goes through `DefaultAzureCredential` + `get_bearer_token_provider("https://cognitiveservices.azure.com/.default")` — no API keys ever touch the code. The lab environment binds credential `azureaiuser` to the **Foundry User** role (role ID `53ca6127-db72-4b80-b1b0-d745d6d5456d`) at subscription scope; that scope is what lets your `OpenAI` client mint a bearer that Foundry accepts on `{endpoint}/openai/v1`.

## Notes

- **Env-var naming deviates from the SkillMeUp canonical `AZURE_AI_*` prefix.** This starter uses `AZURE_OPENAI_ENDPOINT` + `MODEL_DEPLOYMENT` (the names Microsoft Learning's `mslearn-ai-studio` repo uses) so students who cross-reference the official APL-3016 exercises don't have to rename variables. See course 576's plan §6 Q4 for the decision.
- **Do not run `pip install`.** The `python-ai` container variant already ships `openai`, `azure-identity`, `python-dotenv`, and `aiohttp`. `requirements.txt` is a reference manifest so local dev works if you clone the starter outside the lab environment.
- **Never hardcode the model name.** Always read from `os.environ["MODEL_DEPLOYMENT"]`. Model versions change (see the L5 teaching lesson's `azure-ai-inference` retirement callout); the env-var indirection is what keeps the code future-proof.
- **`verify_env.py` refuses to run if `.env` still contains `<angle-bracket>` placeholders.** That's on purpose — a "OK" from `verify_env` means you have a real deployment.
