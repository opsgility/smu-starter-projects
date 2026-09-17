# az-dev-120-adls

Anchorline ADLS Gen2 CLI. Uses `DataLakeServiceClient` for directory operations + POSIX ACLs.

```bash
dotnet run -- <account> tenants scaffold
dotnet run -- <account> tenants show-acl tenants/acme
dotnet run -- <account> tenants set-acl tenants/acme "user::rwx,group::r-x,other::---"
dotnet run -- <account> tenants rename tenants/acme tenants/acme-inc
dotnet run -- <account> tenants list-recursive tenants
```
