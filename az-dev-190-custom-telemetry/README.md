# az-dev-190-custom-telemetry

Anchorline Orders API emits business-domain telemetry: `orders.received.total` (counter), `orders.processing.duration.ms` (histogram), `orders.validation.failures.total` (counter), `orders.inflight` (observable gauge), plus an `Orders.Validate` custom activity with tags for `orderId`, `customerId`, `totalAmount`.

## Run
```
dotnet run
```

## Push traffic
```
curl -X POST http://localhost:5000/orders -H 'Content-Type: application/json' \
  -d '{"orderId":"ord-100","customerId":"cust-42","totalAmount":249.5,"channel":"web","region":"US"}'
```

Every metric appears in App Insights `customMetrics`; every activity in `dependencies` (or `requests` for the top-level).
