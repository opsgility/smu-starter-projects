# ai-3016-model-inference

Starter project for AI-3016 Lesson 6 — **Call the deployed model from Python**.

Sample code for calling Aurora Insights' `aurora-gpt-51-prod` deployment (gpt-5.1 v2025-11-13, GA per MS Learn) via the **Azure AI Inference SDK**, with Managed Identity authentication and support for both synchronous and streaming responses.

## What you'll build

- `src/chat.py` — a simple end-to-end example: single completion + a streaming completion.
- Environment configuration via `.env` (Foundry auto-injects endpoint + credential at lab runtime).

## Prerequisites

- The lab environment provides Python 3.11+ pre-installed in the VS Code container.
- Aurora's deployed `aurora-gpt-51-prod` model from Lesson 5.
- Endpoint URL and credentials will be injected as environment variables at lab start (see `.env.example`).

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python src/chat.py
```

Expected output: a completion answering "What are three benefits of cloud computing?" followed by the same question answered via streaming.

## Files

- `src/chat.py` — the sample.
- `.env.example` — the environment variables the sample reads.
- `requirements.txt` — pinned package versions.
