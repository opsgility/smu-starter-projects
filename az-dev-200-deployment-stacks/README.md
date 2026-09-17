# az-dev-200-deployment-stacks

Anchorline workload managed as a deployment stack with deny-settings and drift detection.

## Convert workload to stack

```bash
chmod +x create-stack.sh
RG=<sandbox-rg> ./create-stack.sh
```

## Try deleting a resource

```bash
az storage account delete -g $RG -n <storage-name> --yes
# Expected: DenyAssignmentAuthorizationFailed — deny-settings blocked it.
```

## Simulate drift

Change something in the portal (e.g. add a tag to the Storage Account), then:

```bash
./detect-drift.sh   # what-if shows the drift as a Modify
./create-stack.sh   # re-apply remediates
```

## Unmanage vs delete

`--action-on-unmanage deleteAll` deletes managed resources when the stack is deleted. Use `detachAll` to keep them.
