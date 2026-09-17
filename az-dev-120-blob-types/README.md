# az-dev-120-blob-types

CLI for the block/append blob type exercises.

## Usage

```bash
az login

# Upload with default single-connection settings
dotnet run -- <account> uploads /tmp/big.bin single-conn.bin --project . -- upload-single /tmp/big.bin single-conn.bin

# Upload with 8 parallel × 8 MiB blocks
dotnet run <account> uploads upload-parallel /tmp/big.bin parallel.bin

# Append N lines to an append blob (per-line calls)
dotnet run <account> audit-logs append-log audit-2026-09.log 200
```
