# az-dev-300-blazor-slots

Blazor Server + Azure SignalR back-plane + /health/ready warm-up path.

Deploy to App Service staging slot, verify `/health/ready` returns 200, then `az webapp deployment slot swap --slot staging`.
