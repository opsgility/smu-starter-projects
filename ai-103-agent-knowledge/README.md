# AI-103 Lesson 9 — Agent Knowledge Tools Starter

Scaffold for an agent that has access to:
- **File search** — vector store of uploaded PDFs / markdown
- **Azure AI Search** — hybrid search over the lab's `ai103-knowledge` index
- **Content Understanding** — invoice extraction tool (custom function tool)

## Files

- `app/agent.py` — agent with all three knowledge tools attached
- `app/cu_tool.py` — Content Understanding analyzer wrapper exposed as a function tool
- `sample_data/product-catalog.pdf` — *(student adds; placeholder note in folder)*
- `sample_data/invoice.pdf`         — *(student adds)*

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
python -m app.agent
```
