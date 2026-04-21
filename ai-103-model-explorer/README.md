# AI-103 Lesson 2 — Model Explorer (Summitline Outfitters)

Starter project for **AI-103 · Lesson 2 · Model Selection & Foundry Tools (Hands-On)**.

## Scenario
You are on the platform team at **Summitline Outfitters**, a fictional outdoor-gear retailer. Before the team commits to a production model for the Summitline AI concierge, you need to benchmark three candidate Foundry deployments on the same prompt and probe which ones reliably support tool calling.

The three Foundry model deployments, the Foundry account (hub), and the Foundry project are pre-provisioned by an ARM template that runs automatically when the lab environment starts. Your job is to finish the two probe scripts.

> **Note on Phi-4.** The teaching material references Phi-4 as the representative small language model. In `eastus2` Phi-4 is only available as a serverless endpoint, so the lab substitutes `gpt-4.1-nano` — a small, low-latency OpenAI model that fills the SLM slot for every exercise.

## Files

| File | Purpose |
| --- | --- |
| `compare_models.py` | Exercise 1 — benchmarks latency and token usage for each deployment on a fixed prompt, prints a Rich table. Contains 3 TODOs inside the `for name in deployments():` loop. |
| `toolcall_probe.py` | Exercise 2 — sends a weather-lookup prompt with a tool schema to each deployment and reports `yes` / `no` on tool-call emission. Contains 3 TODOs inside the `for name in deployments:` loop. |
| `requirements.txt` | Pinned runtime dependencies (pre-installed in the VS Code Server container). |
| `.env.example` | Template for the two environment variables the scripts read. Copy to `.env` and fill from the ARM template outputs (step 6 of Exercise 1). |

## Prerequisites
- Azure CLI signed in as the lab's `AzureAIUser` (`az login --use-device-code`)
- A pre-created resource group in `eastus2` (policy 989 prevents creating your own)
- The ARM template `AI-103 L2 - Foundry Hub + 3 Model Deployments` has finished with `provisioningState: Succeeded`

## Environment variables
Copy `.env.example` to `.env` and set:

- `AZURE_AI_PROJECT_ENDPOINT` — Foundry project data-plane URL (`projectEndpoint` ARM output)
- `MODEL_DEPLOYMENTS` — comma-separated deployment names (`modelDeploymentNames` ARM output)

Exercise 1 walks you through populating these automatically from the ARM template outputs.

## Run Exercise 1 (after you finish the TODOs)

```bash
python compare_models.py "Summarize Azure AI Foundry in one sentence."
```

You should see one row per deployment with latency, input/output tokens, and the first 80 characters of the response.

## Run Exercise 2 (after you finish the TODOs)

```bash
python toolcall_probe.py
```

You should see one row per deployment with `yes` / `no` and, when a tool call is emitted, a compact JSON summary of the call.

## SDK reference
- Client: `AIProjectClient(endpoint=..., credential=DefaultAzureCredential()).get_openai_client()`
- Call shape: `client.responses.create(model=name, input=prompt, tools=TOOLS)` — **Responses API**, not `chat.completions`.
- Token usage: `response.usage.input_tokens`, `response.usage.output_tokens`
- Output text: `response.output_text`
- Tool-call detection: `next((item for item in response.output if getattr(item, "type", None) == "function_call"), None)`
