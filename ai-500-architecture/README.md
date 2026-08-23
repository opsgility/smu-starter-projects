# AI-500 Lesson 3 — Design and scaffold a multi-agent portfolio-review architecture

Skeleton for the Lesson 3 hands-on lab of AI-500 (Designing and Implementing Multi-Agent AI Solutions). You start with five empty agent stubs, an architecture-doc scaffold, and a wired-up smoke test. Across the exercises you sketch Ridgevault Financial's five-agent operating model as a Mermaid diagram, scaffold the Foundry project connection, then wire the Portfolio Analyst end-to-end with a stub tool and confirm it responds to a real Ridgevault portfolio question.

## Scenario

Ridgevault Financial is a mid-sized US wealth-management firm. In Lesson 1 you designed the multi-agent operating model on the whiteboard — five specialist agents (Portfolio Analyst, Compliance Officer, Risk Assessor, Client Relations, Investment Researcher) coordinated by a lightweight Ridge Orchestrator. In this lesson you turn that whiteboard into code: draw the architecture as a diagram your teammates can review, scaffold the Microsoft Agent Framework project and empty agent stubs, then bring one specialist online end-to-end so the rest of the course can build on a working baseline.

## Files

```
ai-500-architecture/
  README.md
  .env.example              # Foundry endpoint + model deployment for keyless auth
  .gitignore
  requirements.txt          # Reference manifest — every package is already in the lab container.
  src/
    verify_env.py           # 30-line smoke test — reads .env, one auth+model round-trip.
    agents/
      portfolio_analyst.py     # TODO — wired end-to-end in exercises 4 + 5.
      compliance_officer.py    # Empty stub — filled in later AI-500 lessons.
      risk_assessor.py         # Empty stub.
      client_relations.py      # Empty stub.
      investment_researcher.py # Empty stub.
  docs/
    architecture.md         # TODO — Mermaid diagram of the 5-agent + orchestrator mesh (exercise 2).
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

   Expect `OK: gpt-5 replied: Hello …`. If it complains about placeholders, edit `.env`; if it 401s, verify `azureaiuser` has the **Foundry User** role on the project (the lab environment grants this automatically at start).

4. Sketch the architecture diagram per exercise 2 by editing `docs/architecture.md`. The lab's Preview button renders Mermaid inline.

5. Complete the TODOs in `src/agents/portfolio_analyst.py` per exercises 4 + 5, then run:

   ```
   python -m src.agents.portfolio_analyst
   ```

## Authentication

Every reach for the model goes through `DefaultAzureCredential` — no API keys ever touch the code. The lab environment binds credential `azureaiuser` to the **Foundry User** role at subscription scope; that scope is what lets your `AIProjectClient` mint a bearer that Foundry accepts on the project endpoint.

## Notes

- **Do not run `pip install`.** The `python-ai` container variant already ships `agent-framework`, `azure-ai-projects`, `azure-ai-agents`, `azure-identity`, `openai`, and `python-dotenv`. `requirements.txt` is a reference manifest so local dev works if you clone the starter outside the lab environment.
- **Never hardcode the model name.** Always read from `os.environ["FOUNDRY_MODEL"]`. Model versions change — the env-var indirection is what keeps the code future-proof.
- **`verify_env.py` refuses to run if `.env` still contains `<angle-bracket>` placeholders.** That's on purpose — an "OK" from `verify_env` means you have a real deployment.
- **Only Portfolio Analyst gets wired in this lesson.** The other four agents are intentionally empty stubs — later AI-500 lessons fill them in one by one and eventually orchestrate them together.
