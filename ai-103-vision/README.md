# ai-103-vision — Summitline Outfitters Computer Vision (AI-103 Lesson 11)

FastAPI starter project for **AI-103 · Lesson 11 · Computer Vision (Hands-On)**.

You are the newly-hired lead AI engineer at **Summitline Outfitters**, a specialty
outdoor-gear retailer. Across four exercises you will wire four vision
capabilities onto one FastAPI service, all against the pre-deployed
Foundry AIServices account:

1. **Exercise 1 — Generate and inpaint images** with `gpt-image-1`
   (`/generate`, `/edit`).
2. **Exercise 2 — Multimodal chat** captions and visual Q&A with `gpt-4.1`
   via the Responses API (`/caption`, `/ask`).
3. **Exercise 3 — Structured visual analysis** with Azure AI
   Content Understanding (`/visual-analyze`).
4. **Exercise 4 — Indirect prompt-injection detection** for image uploads
   (`/inject-detect`).

Authentication is **keyless** for all Azure OpenAI / Foundry calls via
`DefaultAzureCredential`. The Content Understanding REST surface uses the
AIServices account key (pulled from the ARM template outputs).

## Project layout

```
ai-103-vision/
  app/
    __init__.py
    main.py              # FastAPI routes /generate, /edit, /caption, /ask, /visual-analyze, /inject-detect
    generate.py          # Exercise 1 — images.generate
    edit.py              # Exercise 1 — images.edit (inpainting)
    caption.py           # Exercise 2 — Responses API caption() + answer()
    cu_visual.py         # Exercise 3 — Content Understanding analyzer
    inject_detect.py     # Exercise 4 — SYSTEM prompt + JSON-mode detector
  sample_images/
    README.md            # guidance: students generate images in Exercise 1
  requirements.txt
  .env.example
  .gitignore
  README.md
```

## Setup (one time per lab session)

Open a terminal in the `ai-103-vision` folder.

1. Install dependencies (the lab VM's Python already has most of these — the
   `pip install` below is idempotent):

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

3. Populate `.env` from the ARM-template deployment outputs. The first
   exercise walks you through this step-by-step with `az deployment group show`
   and `sed`. You will set:

   | Variable | Source |
   |---|---|
   | `AZURE_AI_PROJECT_ENDPOINT` | `outputs.projectEndpoint.value` |
   | `IMAGE_DEPLOYMENT` | `outputs.gptImage1DeploymentName.value` (default `gpt-image-1`) |
   | `CHAT_DEPLOYMENT` | `outputs.gpt41DeploymentName.value` (default `gpt-4.1`) |
   | `FOUNDRY_ACCOUNT` | `outputs.foundryAccountName.value` |
   | `CU_ENDPOINT` | `outputs.contentUnderstandingEndpoint.value` |
   | `CU_KEY` | `outputs.aiServicesKey.value` |
   | `CU_API_VERSION` | `2024-12-01-preview` |

4. Sign in to Azure (the lab's Azure AI User credential is on the Lab
   Environment tab):

   ```bash
   az login
   ```

## Run the service

```bash
uvicorn app.main:app --reload --port 8000
```

Then in a second terminal, `curl` the endpoints as described in each
exercise (`/generate`, `/edit`, `/caption`, `/ask`, `/visual-analyze`,
`/inject-detect`).

## Scenario

Every example, prompt, and sample file references **Summitline Outfitters**,
the fictional specialty outdoor-gear retailer used across AI-103. The
generated images, the Content Understanding analyzer schema
(`store_name`, `hours`, `phone`, `is_open`), and the injection-detection
test strings are all Summitline-themed — keep the naming consistent when
you extend the app.
