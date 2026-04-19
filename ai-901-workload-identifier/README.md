# ai-901-workload-identifier — scenario → workload classifier CLI

Starter for AI-901 Obj 1 Part III (AI Workloads Overview). Feed a short business scenario into the CLI; it uses your Foundry-deployed chat model to classify the scenario into one of the five AI-901 workload families:

1. Generative / Agentic AI
2. Text Analysis
3. Speech
4. Computer Vision
5. Information Extraction

## What's here
- `src/identify.py` — reads a scenario (stdin or `--scenario`), calls the Foundry-deployed model with a zero-shot classification prompt, prints the predicted workload + recommended Azure service.
- `sample_data/scenarios.txt` — 10 real-world scenarios. The exercise has you run a batch, score the results, and then improve the prompt.

## Env vars
Copy `.env.example` → `.env` and fill in `FOUNDRY_PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME`.

## Run
```
python src/identify.py --scenario "A call center wants to auto-transcribe every call and flag angry customers."
python src/identify.py --file sample_data/scenarios.txt
```
