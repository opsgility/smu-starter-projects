# AI-500 Lesson 11 — Automated evaluations, LLM-as-judge, and human review

Starter for the Lesson 11 hands-on lab of AI-500 (Designing and Implementing Multi-Agent AI Solutions). You run Foundry's built-in evaluators against a sample Ridgevault Financial portfolio-review test set, add a custom LLM-as-judge for regulatory tone, generate synthetic test cases with the Foundry Simulator, push results to the Foundry portal for human review, and wire the whole thing into a CI-style regression gate.

## Scenario

Ridgevault Financial's multi-agent operating model is now live in staging. The Portfolio Analyst agent is drafting quarterly portfolio reviews that go to clients under a regulated-communications banner — every reply must be relevant to the client's actual holdings, grounded in the retrieved statements, coherent as prose, AND written in the firm's regulatory-safe tone (no forward-looking guarantees, no unqualified performance claims, disclosures intact). Ridgevault's compliance lead cannot sign off on general availability until you can show three things: automated quality scores on the outputs, a repeatable synthetic test bed that grows over time, and a human-in-the-loop review round for the edge cases the automated scores flag.

## Files

```
ai-500-evaluations/
  README.md
  .env.example              # Foundry endpoint + model deployment for keyless auth
  .gitignore
  requirements.txt          # Reference manifest — every package is already in the lab container.
  src/
    verify_env.py           # 30-line smoke test — reads .env, one auth+model round-trip.
    eval/
      run_builtin_evaluators.py    # Exercise 2 — Relevance + Groundedness + Coherence over the test set.
      regulatory_tone_judge.py     # Exercise 3 — custom LLM-as-judge (TODO: rubric wiring).
      simulator.py                 # Exercise 4 — synthetic test generation with the Foundry Simulator.
      regression_ci.py             # Exercise 6 — CI-style regression gate against ci-baseline.json.
  data/
    test-set-portfolio-reviews.jsonl   # 12 seed test cases (query + context + ground-truth response).
    rubrics/
      regulatory-tone.md    # Ridgevault regulatory-tone rubric (5-point scale, 4 dimensions).
```

## How to run

1. Sign in with a device code so the container (which has no browser) can complete Entra auth:

   ```
   az login --use-device-code
   ```

2. Copy the env template and fill in the two values printed on the lab's Environment tab:

   ```
   cp .env.example .env
   ```

3. Confirm your identity + deployment reach Foundry:

   ```
   python src/verify_env.py
   ```

   Expect `OK: gpt-5 replied: Hello ...`. If it complains about placeholders, edit `.env`; if it 401s, verify `azureaiuser` has the **Foundry User** role on the project (the lab environment grants this automatically at start).

4. Work exercises in order. Each exercise names the script it runs:

   - Exercise 2 — `python -m src.eval.run_builtin_evaluators`
   - Exercise 3 — `python -m src.eval.regulatory_tone_judge`
   - Exercise 4 — `python -m src.eval.simulator`
   - Exercise 5 — push results in the Foundry portal (no script — you use the portal Evaluations tab and Human Review tab).
   - Exercise 6 — `python -m src.eval.regression_ci`

## Authentication

Every reach for the model AND the evaluators goes through `DefaultAzureCredential` — no API keys ever touch the code. The lab environment binds credential `azureaiuser` to the **Foundry User** role at subscription scope, plus the data-plane roles the evaluators need (`Cognitive Services OpenAI User`, `Cognitive Services User`). That scope is what lets both `AIProjectClient` and the `azure-ai-evaluation` SDK mint bearers Foundry accepts on the project endpoint.

## Notes

- **Do not run `pip install`.** The `python-ai` container variant already ships `azure-ai-projects`, `azure-ai-evaluation`, `azure-identity`, `openai`, and `python-dotenv`. `requirements.txt` is a reference manifest so local dev works if you clone the starter outside the lab environment.
- **Never hardcode the model name.** Always read from `os.environ["FOUNDRY_MODEL"]` — every script here already does. Model versions change; the env-var indirection keeps the code future-proof.
- **`verify_env.py` refuses to run if `.env` still contains `<angle-bracket>` placeholders.** That is intentional — an "OK" from `verify_env` means you have a real deployment.
- **The seed test set has 12 rows** — small enough to run every evaluator over in a minute, large enough that the LLM-as-judge produces a meaningful score distribution. Exercise 4 grows this via the Simulator.
- **The regulatory-tone rubric lives in `data/rubrics/regulatory-tone.md`** and is loaded by name in `regulatory_tone_judge.py`. Do NOT paste the rubric text into the script — the rubric file is a first-class artifact the compliance team edits directly.
