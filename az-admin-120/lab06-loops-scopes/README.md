# SMU-BICEP-FUND Lab 06 — Copy loops, conditional resources, and subscription-scope policy

Starter scaffold for Lab 06 of the *Bicep Fundamentals for Azure Infrastructure* course.

## Scenario

Cascade Renewable Energy's platform team wants a single Bicep file that spins
up "N test VMs" for the operations engineers to shell into during runbook
rehearsals — with just one of them reachable from the internet for the
on-call engineer to hop through. They also want a subscription-wide guardrail
that forbids any *new* public IP from being created outside the sanctioned
Bicep pipeline.

You take a hard-wired one-VM starter, refactor it into a copy loop with a
conditional public IP, add an RBAC role assignment at RG scope, and then move
to a second Bicep file at subscription scope to assign an Azure Policy that
denies public IPs — and confirm the policy actually blocks a rogue portal-style
`az network public-ip create`.

## Files

```
lab06-loops-scopes/
  README.md          # this file
  main.bicep         # starter — one VM, one NIC, one PIP. Refactor to loops in Ex 1-3.
  policy.bicep       # starter — empty. Author subscription-scope policy assignment in Ex 4.
  bicepconfig.json   # minimal linter config with warning-level rules
```

`main.bicep` starts as a working one-VM RG-scope deployment so Exercise 1 has
a concrete "before" state that compiles and deploys. Exercises 1 through 3
refactor it in place. Exercises 4 and 5 add and deploy `policy.bicep` at
subscription scope.

## How to run

1. Sign into Azure in the VS Code terminal:
   ```bash
   az login --use-device-code
   ```
   Follow the device-code flow in a private/incognito browser window using
   the lab credentials shown on the Environment tab.

2. Confirm the pre-created resource group is present:
   ```bash
   RG=$(az group list --query "[?starts_with(name, 'cascade-')].name | [0]" -o tsv)
   LOC=$(az group show -n "$RG" --query location -o tsv)
   echo "RG=$RG  LOC=$LOC"
   ```

3. Preview and deploy the starter template as-is (a single VM), then follow
   the exercises in order to refactor it into loops.

## Authentication

Runs as `labuser` (RG-scope Owner on the pre-created `cascade-*` resource
group) with a minimal subscription-scope role. Subscription-scope policy
assignments (Exercise 5) are permitted for this lab through the platform's
sub-scope RBAC — you do NOT need to elevate the credential yourself. If
`az deployment sub create` returns `AuthorizationFailed`, wait 30-60 seconds
for RBAC propagation and retry; do not try to grant yourself extra roles.

## Notes

- Bicep CLI is preinstalled in the `vscode-dotnet` container. `bicep --version`
  works out of the box; no `az bicep install` step required.
- Loops are declared with `[for i in range(0, count): { ... }]`. The `range()`
  function is inclusive of the start and produces `count` integers.
- Conditional loops combine both: `[for i in range(0, count): if(i == 0) { ... }]`.
- Sub-scope deployments require an explicit `--location` because there is no
  resource group to store the deployment record — the location tells ARM
  where to store the deployment history.
- Role assignments need a deterministic GUID for the `name` — use
  `guid(resourceGroup().id, principalId, roleDefinitionId)` so re-deploys
  target the same assignment record instead of creating duplicates.
- The "Not allowed resource types" policy definition ID is a fixed built-in
  GUID: `6c112d4e-5bc7-47ae-a041-ea2d9dccd749`. It is available in every
  Azure subscription — you do NOT create the definition, you only assign it.
