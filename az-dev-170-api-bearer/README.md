# az-dev-170-api-bearer

Orders API protected by JWT bearer with three policies:
- `OrdersRead`  – requires `scp:Orders.Read` OR `roles:Orders.Reader`
- `OrdersWrite` – requires `scp:Orders.Write` OR `roles:Orders.Writer`
- `OrdersAdmin` – requires `roles:Orders.Admin`
