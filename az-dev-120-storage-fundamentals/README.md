# az-dev-120-storage-fundamentals

Console tool that probes an RA-GZRS storage account from BOTH the primary and secondary endpoints. Reports whether each is reachable and how long it took.

## Run

```bash
export ANCHORLINE_StorageAccount=<account>
export ANCHORLINE_Container=storefront-images
az login
dotnet run
```

Use to verify:
- The primary is up (normal state).
- The secondary READ endpoint returns the same list (RA-GZRS live).
- After a portal-triggered failover, primary fails and secondary responds.
