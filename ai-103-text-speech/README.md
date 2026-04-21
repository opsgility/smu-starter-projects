# AI-103 · Lesson 12 — Summitline Outfitters Text & Speech

Hands-on starter for **AI-103 Lab 2271 · Lesson 12 — Text Analysis & Speech**.
You will complete three exercises that wire Azure AI Language, the Azure OpenAI
Responses API, Azure Translator, and the Azure Speech SDK into one FastAPI
service for Summitline Outfitters — an outdoor-gear retailer modernizing its
merchandising, translation, and in-store voice-kiosk pipelines.

## Scenario

Summitline Outfitters is expanding internationally and rolling out a voice
kiosk at its Denver flagship. The merchandising team needs:

1. Structured extraction from 8,000 free-form guide-written trip reports, plus
   sentiment / key phrases on product reviews (Exercise 1).
2. On-demand translation of product descriptions and kiosk messages into
   Spanish, French, and Japanese for Madrid, Montreal, and Tokyo
   (Exercise 2).
3. Voice-in / voice-out capability for the in-store kiosk, plus speech
   translation for the Madrid location's Spanish-speaking staff (Exercise 3).

## Project layout

```
.
|-- app/
|   |-- __init__.py
|   |-- main.py          # FastAPI app — six endpoints, no student edits
|   |-- text.py          # Exercise 1 — analyze() + extract() (TODOs 1-4)
|   |-- translate.py     # Exercise 2 — translate() (TODOs 1-2)
|   +-- speech.py        # Exercise 3 — synthesize / transcribe / translate_speech (TODOs 1-3)
|-- sample_audio/
|   +-- README.md        # ffmpeg recipes to generate a 16 kHz mono PCM WAV
|-- requirements.txt
|-- .env.example
|-- .gitignore
+-- README.md
```

## Endpoints

| Method | Path                | Exercise | Helper                      |
|--------|---------------------|----------|-----------------------------|
| POST   | /analyze            | 1        | `text.analyze`              |
| POST   | /extract            | 1        | `text.extract`              |
| POST   | /translate          | 2        | `translate.translate`       |
| POST   | /speak              | 3        | `speech.synthesize`         |
| POST   | /transcribe         | 3        | `speech.transcribe`         |
| POST   | /translate-speech   | 3        | `speech.translate_speech`   |

## Prerequisites

- The lab environment has finished deploying the ARM template (Foundry
  account + project + `gpt-4.1` model deployment, standalone Language,
  Translator, and Speech accounts — all in `eastus2`).
- VS Code Server is open at the `ai-103-text-speech` folder.
- You are signed in to Azure: `az account show` should print your subscription.

## Getting started

```bash
# 1. Install dependencies (pre-installed in the lab VM image).
pip install -r requirements.txt

# 2. Copy the env template and fill it in per Exercise 1 / 2 / 3.
cp .env.example .env

# 3. Run the API with auto-reload.
uvicorn app.main:app --reload --port 8000
```

Sample smoke test once `text.analyze` is implemented:

```bash
curl -s -X POST http://127.0.0.1:8000/analyze \
  -F "content=I love the new Summitline Aurora parka."
```

## Note on Cognitive Services key retrieval

If `az cognitiveservices account keys list` fails with HTTP 403, your lab
identity may lack the `Microsoft.CognitiveServices/accounts/listKeys/action`
permission — ask your lab admin. As a temporary workaround you can copy the
key from the Azure portal (resource -> Keys and Endpoint) and paste it into
`.env` directly.

## References

- Exercise 1: <https://learn.microsoft.com/azure/ai-services/openai/how-to/structured-outputs>
- Exercise 2: <https://learn.microsoft.com/azure/ai-services/translator/reference/v3-0-translate>
- Exercise 3: <https://learn.microsoft.com/azure/ai-services/speech-service/quickstarts/setup-platform?pivots=programming-language-python>
