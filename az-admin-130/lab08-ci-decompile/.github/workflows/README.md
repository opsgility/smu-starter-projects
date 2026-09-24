# .github/workflows/

Add `arm-tests.yml` here during Exercise 2. The workflow triggers on pull
requests touching `legacy-arm-templates/` or `tests/`, installs arm-ttk +
Pester, runs the Pester tests with `-CI`, logs into Azure via OIDC, and runs
`az deployment group validate` and `az deployment group what-if` (with a
Delete-gate) on each template.

See Lab 08 Exercise 2 for the workflow YAML and OIDC setup notes.
