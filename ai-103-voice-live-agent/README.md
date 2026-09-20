# AI-103 · Voice Live Agents with Azure Speech and Foundry — Hands-on Lab

**Scenario.** You are the AI engineer at **Summitline Outfitters**, an outdoor-gear retailer. Store associates on the floor need hands-free product answers while they help customers — arms full of tents, no time to type. You are building a Voice Live agent backed by a Microsoft Foundry hosted agent that reads a small RAG index of Summitline product docs (Ridgeline 2 tent, Alpinist 60L backpack, Cirrus sleeping bag, Summit Shell jacket, Trailmark boots) and answers spoken questions with spoken responses.

**Why file-based audio (important).** This is a browser-hosted VS Code container. It has no microphone, no speaker, and no ALSA/PortAudio device. Every Voice Live sample on Microsoft Learn assumes a laptop with `pyaudio` — those samples will not work here. Instead, this lab drives Voice Live with pre-recorded WAV files (audio in) and writes the streaming assistant audio to a WAV file you can download from the file tree and play locally (audio out). Same SDK, same event loop, same architecture as a production voice agent — just deterministic and testable.

## What's provisioned for you at lab start

- Microsoft Foundry (AIServices) resource, `eastus2`
- Foundry project inside the account
- `gpt-5-mini` deployment (for the hosted agent — Voice Live's real-time model is fully managed and does NOT need a Foundry deployment of its own)
- `text-embedding-3-large` deployment (for the RAG index)
- Azure AI Search service, Basic tier (supports vector search)
- Azure Storage account (holds product-doc source; also convenient scratch for output WAVs)

You do NOT deploy any of this — the ARM template runs at lab start. Give it ~10 minutes.

## Exercise-by-exercise TODO map

| # | Exercise | Files you touch |
|---|---|---|
| 1 | Sign in and verify environment | `src/verify_env.py`, `.env` (auto-populated) |
| 2 | Deploy the Foundry hosted agent + RAG index | `src/index_product_docs.py`, `src/deploy_agent.py` |
| 3 | Wire the agent behind a Voice Live session | `src/voice_live_client.py` |
| 4 | Test with a WAV-in / WAV-out harness | `src/voice_live_client.py`, `audio/tent_setup_windy.wav` |
| 5 | Add barge-in interruption handling | `src/barge_in_test.py`, `audio/barge_in_followup.wav` |
| 6 | Add a `check_inventory(sku)` function tool | `src/check_inventory_tool.py`, `audio/inventory_check.wav` |

## Environment variables

Populated by `src/verify_env.py` from the lab's Azure environment (subscription, resource group, resource names).

| Var | Example | Used by |
|---|---|---|
| `AZURE_AI_PROJECT_ENDPOINT` | `https://smu-foundry-abc.services.ai.azure.com/api/projects/smu-project` | Ex 2 (agent client) |
| `AZURE_AI_PROJECT_NAME` | `smu-project` | Ex 3, 4, 5, 6 (Voice Live agent config) |
| `AZURE_SPEECH_ENDPOINT` | `https://smu-foundry-abc.services.ai.azure.com` | Ex 3, 4, 5, 6 (Voice Live SDK `endpoint=`) |
| `AZURE_SEARCH_ENDPOINT` | `https://smu-search-abc.search.windows.net` | Ex 2 (index + agent tool) |
| `AZURE_SEARCH_INDEX_NAME` | `summitline-products` | Ex 2 (RAG index) |
| `MODEL_DEPLOYMENT` | `gpt-5-mini` | Ex 2 (Foundry agent model) |
| `EMBEDDING_DEPLOYMENT` | `text-embedding-3-large` | Ex 2 (index vectorizer) |
| `VOICE_LIVE_VOICE` | `en-US-Aria:DragonHDLatestNeural` | Ex 3, 4, 5, 6 (agent voice) |

Note: `AZURE_SPEECH_ENDPOINT` and `AZURE_AI_PROJECT_ENDPOINT` share the same Foundry hostname. Voice Live is exposed on `services.ai.azure.com/voice-live/realtime` on the SAME resource — you do NOT provision a separate Speech account.

## What's already in the container (`python-ai`)

Do NOT `pip install` anything. The image ships with everything this lab needs, including:

- `azure-ai-voicelive[aiohttp]==1.3.0b1` — the Voice Live SDK (async-only)
- `azure-ai-projects`, `azure-ai-agents` — Foundry hosted-agent SDKs
- `azure-search-documents` — AI Search index management
- `azure-identity` — `DefaultAzureCredential`
- Azure CLI 2.x — `az login --use-device-code`

## Audio assets

`data/transcripts.json` lists the three WAV files you'll need and the exact text each one says. `src/generate_audio.py` synthesizes all three from those transcripts at lab start using the Foundry account's TTS voice — smaller repo, deterministic, and you see the TTS surface once before diving into the real-time surface.

Run it once early in Exercise 1; it will populate `audio/*.wav`.
