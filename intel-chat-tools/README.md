# AI-3016 · Chat & Tool Calling (Starter) — Sentinel Intelligence Bureau

The **Sentinel Intelligence Bureau (SIB)** is rolling out an *OSINT Concierge*:
a small FastAPI service that helps open-source intelligence analysts triage
public signals. The concierge can pull recent open-source news on a topic, do
quick analyst math (rate/percent/time-delta calculations), and look up
public threat-feed indicators by ID.

This starter project is the scaffold for the Chat & Tool Calling lab in the
**Azure AI Foundry Intensive for DIA Developers (AI-3016)** course. You are a
Senior AI Engineer on SIB's **OSINT Modernization** team.

You will:

1. Implement `POST /chat` (Exercise 1) — the tool-call loop over the OpenAI
   **Responses API** via `AIProjectClient.get_openai_client()`.
2. Implement `POST /chat/stream` (Exercise 2) — streams token deltas as
   Server-Sent Events.
3. Smoke-test both with `test_client.py` (Exercise 3).

## Layout

```
intel-chat-tools/
├── app/
│   ├── __init__.py
│   ├── main.py       # FastAPI app with TODOs 1-5
│   └── tools.py      # Tool schemas + Python impls (DO NOT modify)
├── test_client.py    # Smoke test for /chat and /chat/stream
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### `app/tools.py`

Exports two things the endpoints consume — you do **not** modify it:

- `TOOL_SCHEMAS` — Responses-API flat-shape definitions for three tools:
  `get_open_source_news`, `calculate`, `lookup_threat_feed`.
- `DISPATCH` — `{name: callable}` map wired to the Python implementations.

The canonical sample indicator used throughout the exercises is
`OSINT-IND-2024-1042` (an open-source disinformation campaign tracker entry).

### `app/main.py`

- `POST /chat` — TODOs 1-4 inside the tool-call loop (Exercise 1).
- `POST /chat/stream` — TODO 5 with the SSE generator (Exercise 2).
- `GET /healthz` — lightweight liveness probe, already implemented.

## Setup

The lab's ARM template auto-deploys the Foundry account, the project
`sib-osint-concierge`, and a `gpt-5-mini` model deployment into the
pre-created resource group. Exercise 1 walks through pulling
`projectEndpoint` and `modelDeploymentName` out of the ARM outputs.

Local workflow inside the VS Code Server terminal (the workspace is
already the starter root; no `cd` needed):

```bash
cp .env.example .env
# Edit .env with the project endpoint + deployment name from ARM outputs.
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then in a **second** terminal:

```bash
python test_client.py
```

## Required environment variables

| Variable                     | Description                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------- |
| `AZURE_AI_PROJECT_ENDPOINT`  | Foundry **project** URL — `https://<svc>.services.ai.azure.com/api/projects/<project-name>`.      |
| `MODEL_DEPLOYMENT`           | Deployment name (case-sensitive). The lab's ARM template defaults to `gpt-5-mini`.                |

## Authentication

`AIProjectClient` uses `DefaultAzureCredential`, which picks up your
`az login` session in the VS Code terminal. No API keys. If the first
request fails with `DefaultAzureCredential failed to retrieve a token`,
run `az login --use-device-code` and restart uvicorn.

## Sentinel Intelligence Bureau — scenario notes

All sample data is **non-classified, fictional, and synthesized for
training**. None of the indicators, news items, or threat-feed entries
represent real-world intelligence. The OSINT Concierge demonstrates the same
Responses-API patterns SIB engineers would apply against real open-source
data sources (RSS feeds, public threat-intelligence platforms, etc.).

## Common gotchas (see exercise troubleshooting for more)

- **Flat tool schemas** — Responses API wants
  `{"type": "function", "name": ..., "description": ..., "parameters": ...}`.
  There is NO inner `function:` wrapper.
- **`output` is a string** — wrap your tool's dict return with
  `json.dumps(result)` inside `function_call_output`.
- **`arguments` is a JSON string** — `json.loads(call.arguments)` before
  calling the Python function.
- **Pass `tools=TOOL_SCHEMAS` on every call**, including follow-ups —
  they are not cached server-side.
- **Use `previous_response_id=response.id`** so the server threads
  state and you don't resend the original user message.
