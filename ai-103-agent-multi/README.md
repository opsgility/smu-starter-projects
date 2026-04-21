# AI-103 Lesson 10 — Summitline Multi-Agent Concierge

Starter project for AI-103 Lesson 10: **Multi-Agent & Approval Flows**
(lab 2262).

Summitline Outfitters is breaking its monolithic concierge agent apart. Across
three exercises you will stand up a **supervisor / worker** agent system with
a FastAPI human-in-the-loop (HITL) approval queue and full OpenTelemetry
tracing into Application Insights:

| Exercise | Focus | Files you edit |
| --- | --- | --- |
| **3391** Build Refund & Lookup Workers | One agent + one `FunctionTool` per worker. | `app/worker.py` |
| **3392** Orchestrate with ConnectedAgentTool + HITL | Supervisor delegates via `ConnectedAgentTool`; FastAPI gates refunds > $100. | `app/orchestrator.py`, `app/main.py`, `app/worker.py` |
| **3393** Instrument with OpenTelemetry | `configure_azure_monitor` + custom span attributes; confirm traces in App Insights. | `app/tracing.py`, `app/main.py` |

## Layout

```
ai-103-agent-multi/
  app/
    __init__.py
    worker.py         # _refund, _lookup_order, request_refund (HITL gated),
                      # PENDING + FUTURES, converse helper, worker factories.
    orchestrator.py   # build() — creates workers + ConnectedAgentTool fan-out.
    tracing.py        # init() — azure-monitor-opentelemetry wiring.
    main.py           # FastAPI with lifespan cleanup + /request, /approvals.
  requirements.txt
  .env.example
  .gitignore
  README.md
```

## Prerequisites

- The lab platform deploys the AI-103 L10 ARM template automatically: a
  Foundry account, a child project, a `gpt-4.1` deployment, a Log Analytics
  workspace, and a workspace-based Application Insights component in an
  `eastus2` resource group.
- You are signed in as the `azureaiuser` credential from the Lab Environment
  tab (has the `Azure AI User` role on the Foundry project).
- The starter's `requirements.txt` is pre-installed in the VS Code Server
  container — no `pip install` is needed.

## Populate `.env`

See Exercise 3391 Steps 3–6 for the full `az deployment group show` commands.
The short version is:

```bash
export RG=$(az group list --query "[0].name" -o tsv)
export DEP=$(az deployment group list -g $RG --query "[0].name" -o tsv)

cat > .env <<EOF
PROJECT_ENDPOINT=$(az deployment group show -g $RG -n $DEP --query 'properties.outputs.projectEndpoint.value' -o tsv)
MODEL_DEPLOYMENT_NAME=$(az deployment group show -g $RG -n $DEP --query 'properties.outputs.gpt41DeploymentName.value' -o tsv)
APPLICATIONINSIGHTS_CONNECTION_STRING=$(az deployment group show -g $RG -n $DEP --query 'properties.outputs.appInsightsConnectionString.value' -o tsv)
EOF
```

## Run the API

After finishing Exercise 3392:

```bash
uvicorn app.main:app --port 8000
```

Do **not** pass `--reload` while approvals are pending — the in-memory
`PENDING` / `FUTURES` queues are wiped on every reload.

### Auto-approved refund (under $100)

```bash
curl -s -X POST http://localhost:8000/request \
  -F 'message=Refund order 42, $45, wrong color' \
  -F 'customer_id=C-1001'
```

### HITL refund (over $100)

```bash
curl -s -X POST http://localhost:8000/request \
  -F 'message=Refund order 88, $150, damaged tent' \
  -F 'customer_id=C-1002'    # hangs until you approve
```

List and approve pending refunds:

```bash
curl -s http://localhost:8000/approvals
curl -s -X POST http://localhost:8000/approvals/<id> -F 'decision=approved'
```

## Observability

After Exercise 3393 finishes wiring `configure_azure_monitor`, each
`/request` call becomes one end-to-end transaction in Application Insights
with child dependency spans for every connected-agent sub-run and tool call.
First traces may take 60–120 seconds to appear.

Useful Kusto:

```kusto
union requests, dependencies, traces
| where cloud_RoleName == "summitline-concierge" or operation_Name contains "handle_request"
| project timestamp, itemType, name, duration, customDimensions
| order by timestamp desc
| take 50
```

## Design notes

- **Policy in code, not in prompts.** The `$100` refund threshold lives in
  `request_refund` in `app/worker.py`. Prompt injection cannot talk Python
  out of an `if` branch.
- **Least-authority workers.** `lookup_worker` is read-only and literally
  has no tool that can mutate state. `refund_worker` is write-only.
- **Layered defense for routing.** The orchestrator's instructions AND the
  `ConnectedAgentTool` descriptions both say "verify with `lookup_worker`
  before calling `refund_worker`".
- **Single trace per user request.** `tracing.init()` runs **before**
  `app = FastAPI()` so auto-instrumentation hooks FastAPI middleware.
