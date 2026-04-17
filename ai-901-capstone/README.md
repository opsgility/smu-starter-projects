# AI-901 Capstone — Multimodal Foundry Assistant

Build a single FastAPI service that exposes a multimodal assistant for Northwind Horizon. The app pulls together everything from the course:

- `/chat` — Foundry chat (Lesson 5)
- `/analyze-text` — Azure AI Language sentiment + entities (Lesson 7)
- `/analyze-image` — Multimodal vision (Lesson 9)
- `/extract-document` — Content Understanding document extraction (Lesson 10)
- `/speak` — Text-to-speech (Lesson 8)

Run with `uvicorn app.main:app --reload --port 8000` and exercise it from the provided `test_client.py`.

## Layout

```
app/
  __init__.py
  main.py          # FastAPI app + route wiring
  chat.py
  text.py
  vision.py
  documents.py
  speech.py
test_client.py     # calls every endpoint end-to-end
sample_data/       # test image, test PDF, test text
```
