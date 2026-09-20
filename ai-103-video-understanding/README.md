# AI-103 - Video Understanding with Content Understanding (Summitline Outfitters)

Starter project for **AI-103 Lab 2588 - Video Understanding with Content Understanding
- Lab Exercises**. You will build the Summitline Outfitters video-analytics pipeline
that lets a Foundry agent answer questions like "show me videos where the tent is
set up in windy conditions" with timestamped citations.

## Scenario

Summitline Outfitters is a specialty outdoor-gear retailer. The product team
records short product-demo videos (packs, tents, softshells) and needs a way to
let customer-support agents search them by scene content, not just filename. In
this lab you stand up the full pipeline:

1. Upload sample product-demo videos to an AAD-only Azure Blob container.
2. Author a Content Understanding **pro-mode video analyzer** with a Summitline
   `fieldSchema` (`products_demonstrated`, `key_features_shown`, `scene_summary`,
   `presenter_quality`, `duration_seconds`).
3. Invoke the analyzer, poll `operation-location`, and inspect segmented results.
4. Index each analyzer segment into Azure AI Search with a `text-embedding-3-large`
   vector so semantic similarity search works.
5. Wrap that search behind a Foundry Agents `FunctionTool` that returns
   timestamped citations.
6. Run the end-to-end "windy tent" query through the agent and see the citation
   string materialize.

## Files

```
ai-103-video-understanding/
  README.md
  .env.example                 # Filled in from ARM outputs in Exercise 1 Step 4.
  .gitignore
  requirements.txt             # Manifest only. Every package already preinstalled
                               # in the python-ai container - do NOT `pip install`.
  src/
    verify_env.py              # Exercise 1 - reads .env, tests DefaultAzureCredential + one round-trip.
    analyzer_schema.json       # Exercise 3 starter - students edit the fieldSchema.
    upload_videos.py           # Exercise 2 - upload sample MP4s via user-delegation SAS.
    invoke_analyzer.py         # Exercise 4 - PUT analyzer + POST :analyze + poll operation-location.
    index_segments.py          # Exercise 5 - create vector index + upload segment documents.
    agent_tool.py              # Exercise 6 - wrap search behind a FunctionTool.
    end_to_end_query.py        # Exercise 7 - drive the agent with the "windy tent" query.
  sample-videos/
    README.md                  # Where to source the demo MP4s (public Azure sample URLs).
```

## How to run

The lab's ARM template (Template 89) pre-deploys the Foundry account + gpt-5.1
+ text-embedding-3-large + AI Search + storage account with a `videos` container.
Wait until the Lab Environment tab shows "Ready" (about 10 minutes) before starting.

1. **Sign in to Azure in the VS Code terminal.**

   ```bash
   az login --use-device-code
   ```

   The container is headless - always use `--use-device-code`. Follow the
   `https://microsoft.com/devicelogin` link and select the `azureaiuser` account
   shown on the Lab Environment tab.

2. **Capture the ARM outputs and write `.env`** (Exercise 1 Step 4).

3. **Run the environment check.**

   ```bash
   python src/verify_env.py
   ```

   Prints `OK` when every env var + auth path works.

4. **Work through the exercises in order.** Every subsequent script depends on
   the previous exercise's state (uploaded blobs, created analyzer, populated
   index).

## Packages

Every package in `requirements.txt` is **already preinstalled** in the
`python-ai` VS Code Server container the lab runs in. You do **not** run
`pip install` at lab time. The `requirements.txt` in this folder is kept as a
manifest for reference and for local development outside the lab.

## Authentication

Every SDK client in this starter uses `DefaultAzureCredential` - keyless, backed
by the cached `az login --use-device-code` token. No API keys are stored in
`.env`, no shared-key SAS is minted anywhere. The `azureaiuser` credential (id 59)
holds these Azure roles at subscription scope:

- `Foundry User` - lets the student call the Foundry account + project.
- `Cognitive Services OpenAI User` - inference (chat + embeddings) via Foundry.
- `Cognitive Services User` - Content Understanding data-plane calls.
- `Contributor` - control-plane operations the exercises use.
- `Storage Blob Data Contributor` - blob upload / SAS-mint via user-delegation.
- `Search Service Contributor` - create the AI Search index.
- `Search Index Data Contributor` - upload documents to the index.

## Notes

- **Content Understanding API version**: always `2025-11-01` (GA). The starter
  never touches `2026-06-01-preview` - preview features aren't needed here.
- **Model versions**: `gpt-5.1` version `2025-11-13` (GA to 2027-05-15) and
  `text-embedding-3-large` version `1`. Both pulled from `MODEL_DEPLOYMENT` /
  `EMBEDDING_DEPLOYMENT` env vars - never hardcoded in code.
- **Region**: `eastus2` (pool 6). Content Understanding, gpt-5.1 GlobalStandard,
  text-embedding-3-large, and AI Search Basic are all supported there.
- **RBAC propagation**: fresh role assignments can take 2-5 minutes to
  propagate. If you hit `AuthorizationFailed` on your first blob or search
  call, wait 3 minutes and retry before assuming a real bug.
- **Sample videos**: `sample-videos/README.md` names public Azure sample MP4s
  the upload script can grab. The starter does not bake video binaries into
  the repo (they'd bloat every lab clone).
