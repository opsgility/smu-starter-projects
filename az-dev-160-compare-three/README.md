# az-dev-160-compare-three

Send 100 "OrderCreated" messages through Service Bus, Event Grid, Event Hubs. Compare code shape and latency.

## Env

- `SB_NAMESPACE`, `SB_QUEUE`
- `EG_TOPIC_ENDPOINT`, `EG_TOPIC_KEY` (or MI-based)
- `EH_NAMESPACE`, `EH_NAME`

## Modes

```
dotnet run --project . -- sb
dotnet run --project . -- eg
dotnet run --project . -- eh
```
