# AI-103 Capstone — Northwind Horizon AI Platform Starter

A unified FastAPI platform that brings together everything from AI-103:

- `/chat`         — Foundry chat with tool calling
- `/rag`          — RAG over the capstone knowledge index
- `/agent`        — Multi-tool agent (Agent Service)
- `/vision-ask`   — Multimodal Q&A on an uploaded image
- `/extract-doc`  — Content Understanding extraction
- `/voice`        — Voice-in / voice-out (Speech)
- `/health`       — Liveness probe
- Tracing exported to Azure Monitor

## Files

- `app/main.py`    — FastAPI orchestrator wiring all endpoints
- `app/chat.py`    — chat client
- `app/rag.py`     — retrieval + answer
- `app/agent.py`   — agent setup
- `app/vision.py`  — multimodal vision
- `app/speech.py`  — TTS + STT
- `app/cu.py`      — Content Understanding wrapper
- `app/tracing.py` — OTel + Azure Monitor

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
uvicorn app.main:app --reload --port 8000
python test_client.py
```
