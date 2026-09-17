# az-dev-130-always-encrypted

Client-side Always Encrypted demo for AZ-DEV-130 M8L16.

## Env

- `ANCHORLINE_SQL_SERVER`
- `ANCHORLINE_SQL_DATABASE`

## Modes

```
dotnet run --project . -- seed            # insert 2 customers with encrypted PII
dotnet run --project . -- read-ae         # read with Column Encryption Setting=Enabled — plaintext
dotnet run --project . -- read-plain      # read without the AE keyword — ciphertext bytes
dotnet run --project . -- find-email <e>  # equality lookup on deterministic Email column
```
