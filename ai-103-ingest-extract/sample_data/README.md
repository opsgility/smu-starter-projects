# Sample data for ai-103-ingest-extract

Drop a mix of PDFs into this folder, then upload to the storage container with:

```bash
az storage blob upload-batch \
  --account-name <your-storage-account> \
  --destination ai103-source \
  --source .
```

Suggested mix:
- 2-3 invoices (`invoice-*.pdf`)
- 1-2 contracts (`contract-*.pdf`)
- 1 statement of work (`sow-*.pdf`)
