# az-dev-120-doc-store

Anchorline document-store CLI. Uploads with metadata + tags, seeds bulk data, and queries via `FindBlobsByTagsAsync`.

```bash
dotnet run <account> docs upload 2026/invoice-1042.txt michael@anchorline.example sales invoice 2026
dotnet run <account> docs seed 100
dotnet run <account> docs find "\"documentType\" = 'invoice' AND \"year\" = '2026'"
dotnet run <account> docs list-metadata 2026/invoice-1042.txt
```
