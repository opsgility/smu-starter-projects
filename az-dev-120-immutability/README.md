# az-dev-120-immutability

Shell scripts for the immutability + WORM exercises.

- `scripts/seed.sh <account> <container> [count]` — seed audit blobs.
- `scripts/try-delete.sh <account> <container> <blob>` — attempt delete, report outcome.

The lab uses `az storage container immutability-policy` for policy management.
