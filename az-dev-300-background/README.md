# az-dev-300-background

TaskForge async spine: SB command handler + Durable Functions orchestrator.

## Env
- `SB_ConnectionString` (MI-based `<sb-namespace>.servicebus.windows.net` when using `AzureWebJobsServiceBus__fullyQualifiedNamespace`)
- `COSMOS_ENDPOINT`

## Local
`func start` (requires Azure Functions Core Tools). For SB with MI, the tools use `az login` under the hood.
