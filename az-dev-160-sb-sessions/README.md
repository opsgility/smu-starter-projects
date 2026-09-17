# az-dev-160-sb-sessions

Session-based FIFO Service Bus queue for Anchorline orders.

## Env

- `SB_NAMESPACE`
- `SB_QUEUE` — default `orders-sessions` (must have sessions enabled)

## Modes

```
dotnet run --project . -- send-interleaved   # 5 orders × 3 customers, interleaved sessions
dotnet run --project . -- process            # session processor with 3 concurrent sessions
dotnet run --project . -- poison             # duplicate detection test
dotnet run --project . -- dlq                # read the DLQ
```
