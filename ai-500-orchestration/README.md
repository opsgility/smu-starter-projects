# AI-500 Lesson 9 — Orchestrate a portfolio review with Agent Framework and LangGraph

Skeleton for the Lesson 9 hands-on lab of AI-500 (Designing and Implementing Multi-Agent AI Solutions). You take the four Ridgevault Financial specialist agents (portfolio analyst, risk assessor, compliance officer, brief writer) and wire them into a portfolio-review workflow **two ways** so you feel the trade-off firsthand:

1. **Microsoft Agent Framework `SequentialBuilder`** — a straight-line pipeline where every specialist runs in order on a shared conversation thread.
2. **LangGraph `StateGraph`** — a typed graph with per-node state, a conditional edge, and a **human-in-the-loop (HITL) approval gate** at the compliance-officer node.

Then in the capstone challenge you fault-inject one specialist and add graceful degradation with an on-graph error edge.

## Scenario

Ridgevault Financial's client-experience team asks for a nightly "morning brief" on every priority portfolio. The brief needs the analyst's read of overnight moves, the risk desk's stress-test summary, and a compliance sign-off before it lands in the advisor's inbox. In earlier lessons you designed the multi-agent operating model and built the individual specialist agents plus their MCP tools. In this lesson you turn those specialists into a real workflow — first as a fast sequential pipeline, then as a stateful graph with a compliance-officer approval gate the graph pauses on until a human clicks approve.

## Files

```
ai-500-orchestration/
  README.md
  .env.example                   # Foundry endpoint + model deployment for keyless auth
  .gitignore
  requirements.txt               # Reference manifest — every package is already in the lab container.
  src/
    verify_env.py                # Smoke test — reads .env, one auth+model round-trip, asserts langgraph importable.
    agents/
      portfolio_analyst.py       # Reads the portfolio, calls out overnight moves + concentration risk.
      risk_assessor.py           # Runs stress-test summary against the analyst's read.
      compliance_officer.py      # Checks the brief for restricted-list violations and disclosure gaps.
      brief_writer.py            # Renders the final advisor-facing morning brief.
    orchestrators/
      sequential_builder.py      # TODO — wire the 4 specialists into a SequentialBuilder pipeline (exercise 2 + 3).
      langgraph_state.py         # TODO — rebuild the same flow as a LangGraph StateGraph (exercise 4 + 5 + 6).
  data/
    test-portfolio.json          # Ridgevault test portfolio — 6 holdings, 1 restricted-list ticker.
```

## How to run

1. Sign in with a device code so the container (which has no browser) can complete Entra auth:

   ```
   az login --use-device-code
   ```

   Follow the URL `https://microsoft.com/devicelogin` and enter the code the CLI prints.

2. Copy the env template and fill in the two values printed on the lab's Environment tab:

   ```
   cp .env.example .env
   ```

3. Confirm your identity + deployment reach Foundry and that LangGraph imports cleanly:

   ```
   python src/verify_env.py
   ```

   Expect `OK: gpt-5 replied: Hello ...  langgraph <version> importable`. If it complains about placeholders, edit `.env`; if it 401s, verify `azureaiuser` has the **Foundry User** role on the project (the lab environment grants this automatically at start).

4. Complete the TODOs in `src/orchestrators/sequential_builder.py` per exercise 2, then run it against the test portfolio:

   ```
   python -m src.orchestrators.sequential_builder data/test-portfolio.json
   ```

5. Complete the TODOs in `src/orchestrators/langgraph_state.py` per exercises 4-5-6, then run:

   ```
   python -m src.orchestrators.langgraph_state data/test-portfolio.json
   ```

## Authentication

Every reach for the model goes through `DefaultAzureCredential` — no API keys ever touch the code. The lab environment binds credential `azureaiuser` to the **Foundry User** role at subscription scope; that scope is what lets your `AIProjectClient` mint a bearer token that Foundry accepts on the project endpoint.

## Notes

- **Do not run `pip install`.** The `python-ai` container variant already ships `agent-framework`, `azure-ai-projects`, `azure-ai-agents`, `azure-identity`, `openai`, `python-dotenv`, `langgraph`, `langchain-core`, and `langchain-openai`. `requirements.txt` is a reference manifest so local dev works if you clone this starter outside the lab environment.
- **Never hardcode the model name.** Always read from `os.environ["FOUNDRY_MODEL"]`. Model versions change — the env-var indirection is what keeps the code future-proof.
- **The four specialist agents are intentionally minimal** — one prompt each, no external tools. This lesson is about the *orchestration shape*, not the specialist depth. Depth is added in the capstone.
- **The LangGraph HITL gate** uses `interrupt()` inside the compliance node. When the graph hits it, execution pauses; you resume it with `graph.invoke(Command(resume="approve"))` or `resume="reject"`. In exercise 5 you drive that interactively from stdin so it feels like a real approval step.
- **Do not rename `data/test-portfolio.json`** — the orchestrators load it by exact path.
