# az-dev-200-what-if

Anchorline pattern for what-if-gated Bicep deploys. Change `planSku` in `main.bicep` or override at the CLI to see the diff.

## Local what-if

```bash
az deployment group what-if -g $RG -f main.bicep -p planSku=S1
```

## `--confirm-with-what-if` gate

```bash
az deployment group create -g $RG -f main.bicep -p planSku=S1 --confirm-with-what-if
```

## PR-comment gate

`.github/workflows/pr-what-if.yml` runs what-if on every PR to `main` that touches `main.bicep` or a `.bicepparam` file, then posts the diff back as a PR comment.
