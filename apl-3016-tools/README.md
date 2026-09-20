# AI-3016 Lesson 8 — Build a chat app with web and file tools

Skeleton for the Lesson 8 hands-on lab of AI-3016 (APL-3016 prep). You extend the Lesson 6 chat pattern to use the Foundry Responses API with two built-in tools: `web_search` (Bing-grounding) and `file_search` (against a Foundry vector store you upload Margie's Travel brochures into). This is the modern APL-3016 grounding path — no Azure AI Search resource, no custom retrieval code, just tools on the model.

## Scenario

Margie's Travel sales agents are asking their AI assistant questions that mix live external context ("what's the weather in Copenhagen next week") with grounded internal-policy content ("what does our Baltic cruise brochure say about excursions"). In this lesson you wire both into a single `responses.create` call so the model can pick the right tool for the right slice of a question — and cite the brochure directly when it does.

## Files

```
apl-3016-tools/
  README.md
  .env.example              # AZURE_OPENAI_ENDPOINT + MODEL_DEPLOYMENT
  .gitignore                # Adds vector_store_id.txt to the ignore list
  requirements.txt          # Reference manifest — every package is already in the lab container.
  src/
    verify_env.py           # 30-line smoke test — same as apl-3016-chat.
    tools-app.py            # Responses API + tools skeleton. TODOs you fill in exercises 3 + 4.
  brochures/                # Margie's Travel brochure content. You upload these to a Foundry vector store in exercise 4.
    margie-baltic-cruise.md
    margie-mediterranean.md
    margie-solo-travel.md
```

## How to run

1. Sign in with a device code so the container completes Entra auth:

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

4. Complete the TODOs in `src/tools-app.py` per exercises 3 (web_search) and 4 (file_search + vector store upload), then run:

   ```
   python src/tools-app.py "Suggest a 5-day trip to the Baltic in September, and quote our brochure's cancellation policy."
   ```

The script will print each tool call the model makes plus the final response text. Tool calls that hit `web_search` are Bing-grounded and Foundry bills them as First-Party Consumption; tool calls that hit `file_search` are answered from your uploaded brochures.

## Authentication

Every reach for the model goes through `DefaultAzureCredential` + `get_bearer_token_provider("https://cognitiveservices.azure.com/.default")` — no API keys. The lab environment binds credential `azureaiuser` to the **Foundry User** role (role ID `53ca6127-db72-4b80-b1b0-d745d6d5456d`) at subscription scope. The Responses API + tools call goes to the same `{endpoint}/openai/v1/responses` surface the L6 chat completions used, so the bearer + endpoint pattern is identical.

## Notes

- **Env-var naming deviates from the SkillMeUp canonical `AZURE_AI_*` prefix.** This starter uses `AZURE_OPENAI_ENDPOINT` + `MODEL_DEPLOYMENT` (the names Microsoft Learning's `mslearn-ai-studio` repo uses) so students who cross-reference the official APL-3016 exercises don't have to rename variables. Same decision documented in `apl-3016-chat/README.md`.
- **Do not run `pip install`.** The `python-ai` container variant already ships `openai`, `azure-identity`, and `python-dotenv`. `requirements.txt` is a reference manifest.
- **`web_search` billing:** it's a First-Party Consumption Service (Bing Grounding) — Foundry meters the calls separately from your model deployment. The lab environment's subscription pool has a small quota; do not stress-test with hundreds of calls.
- **Vector-store id is cached in `vector_store_id.txt`** (git-ignored). Delete that file to rebuild the store from scratch — useful if you edit brochure content and want the model to re-index.
- **Brochure content is deliberately Margie-specific fiction.** Do not treat the cancellation policies as real; they exist to give the model something concrete to cite so students can verify `file_search` is grounding correctly.
