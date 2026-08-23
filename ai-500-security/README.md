# AI-500 Lesson 15 — Zero Trust, Key Vault, and AI Red Teaming

Ridgevault Financial's portfolio-review platform runs across a Foundry account and downstream Container Apps. You harden it in this lab: attach a system-assigned managed identity to Foundry with a single least-privilege data-plane role, move a Ridgevault internal API secret out of code and into Azure Key Vault, then run an adversarial safety scan against the portfolio-review flow and write two mitigations for the top findings.

## Scenario

Ridgevault Financial rolled out a multi-agent portfolio-review service last quarter. An internal security review flagged three risks: (1) a Ridgevault internal API secret is embedded in agent code, (2) the Foundry account has no managed identity and no role-scoped access story, (3) the portfolio-review flow was never red-teamed. You have 90 minutes to close all three, in the same order security engineers would tackle them in production.

## Files

```
ai-500-security/
  README.md
  .env.example                                   # Foundry + Key Vault values from the ARM template outputs
  .gitignore
  requirements.txt                               # Reference only — every package is preinstalled in python-ai
  src/
    verify_env.py                                # Smoke test — reads .env, one auth round-trip to Foundry
    security/
      keyvault_secret_read.py                    # Reads the Ridgevault secret from Key Vault via DefaultAzureCredential
      mi_least_priv_scaffold.py                  # Prints Foundry system-assigned MI + its role assignments
    red_team/
      run_red_team.py                            # Runs adversarial safety scan against portfolio_review_flow
      portfolio_review_flow.py                   # The target flow being scanned (calls Foundry gpt-5)
    mitigations/
      injection_defense_middleware.py            # Prompt-injection guardrail (Task 6 exercises fill this in)
      pii_redact.py                              # PII redaction filter (Task 6 exercises fill this in)
  data/
    test-inputs.jsonl                            # Adversarial prompt corpus — prompt injection, PII exfil, jailbreak
```

## How to run

1. Sign in to Azure from the container terminal:
   ```bash
   az login --use-device-code
   ```
   Copy the code shown, open `https://microsoft.com/devicelogin` in your local browser, paste the code, and sign in with the lab-provided Azure credentials from the Environment tab.

2. Copy `.env.example` to `.env` and fill in the values from your lab's Environment tab (`FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL`, `KEY_VAULT_NAME`, `KEY_VAULT_URI`).

3. Run the smoke test:
   ```bash
   python src/verify_env.py
   ```
   Green output means Foundry auth is working and your gpt-5 deployment is reachable.

4. Work through Exercises 2–6 in order. Each exercise runs one of the scripts under `src/`.

## Authentication

Every script authenticates via `DefaultAzureCredential()` — no API keys. The lab-provided credential (`azureaiuser`) already holds the Foundry data-plane roles the scripts need (`Foundry User`, `Cognitive Services OpenAI User`, `Cognitive Services User`). Do NOT edit the scripts to use API keys — the Foundry account has `disableLocalAuth: true` and rejects key-based calls.

Exercise 2 (Key Vault secret store) has you create a *separate* Key Vault inside the pre-provisioned `ai500-l15-security-rg` resource group (where the platform gives you Owner scope), then assign yourself `Key Vault Secrets Officer` on it and write the secret. The ARM template's Key Vault is used for `keyvault_secret_read.py` as the read-only reference vault.

## Notes

- Model deployment name is `gpt-5` (Foundry Models `gpt-5` version `2025-08-07`, GlobalStandard SKU, eastus2). Verified GA on MS Learn.
- `azure-ai-evaluation` (base package) is preinstalled — the red-team scan uses `AdversarialSimulator` + `IndirectAttackEvaluator` + `ContentSafetyEvaluator` rather than the `[redteam]`/PyRIT extra (which isn't in the container variant). Same conceptual workflow; different SDK surface.
- Never grant `Owner`, `User Access Administrator`, or `Role Based Access Control Administrator` on any resource — the lab specifically teaches least-privilege and those roles defeat the point.
