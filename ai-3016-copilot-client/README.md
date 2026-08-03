# ai-3016-copilot-client

Starter project for AI-3016 Lesson 9 — **Extend a copilot: Python nodes + programmatic client**.

Two related samples:

- `src/flow_client.py` — invoke Aurora's **deployed prompt flow** endpoint (not the raw model) with a user question and print the grounded answer + citations.
- `src/python_node_scaffold.py` — a self-contained example of the kind of Python function that plugs into a Prompt Flow node. Includes a small dev harness so you can iterate locally before copy-pasting into the Foundry flow editor.

## What you'll build

- A repeatable pattern for calling deployed flows from application code.
- A Python-node template you'll take back into the Foundry flow editor to extend Aurora's copilot.

## Prerequisites

- Aurora's `consulting-copilot-flow` deployed as an endpoint (lesson 8 + lesson 11).
- Environment variables injected by the lab at start (see `.env.example`).

## Install

```bash
pip install -r requirements.txt
```

## Run the flow client

```bash
python src/flow_client.py
```

## Run the local Python-node scaffold

```bash
python src/python_node_scaffold.py
```

## Files

- `src/flow_client.py` — the flow-endpoint client.
- `src/python_node_scaffold.py` — the Python-node template.
- `.env.example` — expected environment variables.
- `requirements.txt` — pinned dependencies.
