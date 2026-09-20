"""Read the Ridgevault internal API secret from Key Vault via DefaultAzureCredential.

Zero Trust win: the secret never lives in code, never lives in an env var of its
own, and never lives on disk. Access is scoped to a managed identity or a lab
user with the 'Key Vault Secrets User' RBAC role on the vault.
"""
from __future__ import annotations

import os
import sys

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv


SECRET_NAME = "ridgevault-portfolio-api-key"


def main() -> int:
    load_dotenv()
    # Exercise 2 has you create your OWN Key Vault inside ai500-l15-security-rg
    # and store the secret there. Prefer that vault when set; fall back to the
    # ARM-deployed vault otherwise.
    vault_uri = os.environ.get("STUDENT_KEY_VAULT_URI") or os.environ.get("KEY_VAULT_URI")
    if not vault_uri or vault_uri.startswith("<"):
        print("KEY_VAULT_URI (or STUDENT_KEY_VAULT_URI) not set in .env")
        return 1

    print(f"Reading {SECRET_NAME!r} from {vault_uri}")
    client = SecretClient(vault_url=vault_uri, credential=DefaultAzureCredential())
    try:
        secret = client.get_secret(SECRET_NAME)
    except Exception as exc:  # noqa: BLE001
        print(f"  READ FAILED: {exc}")
        print("\n  Common causes:")
        print("    1. Your lab user does NOT have 'Key Vault Secrets User' on this vault.")
        print("       Fix: `az role assignment create --assignee $(az ad signed-in-user show --query id -o tsv) \\")
        print("             --role 'Key Vault Secrets Officer' --scope <student-kv-resource-id>`")
        print("    2. The secret was never stored — run Exercise 2 Task 3 first.")
        return 1

    # Never print the value in production — this print is a teaching aid ONLY.
    masked = secret.value[:4] + "…" + secret.value[-2:] if secret.value and len(secret.value) > 8 else "***"
    print(f"  OK: secret exists, value masked = {masked}")
    print(f"  vault      = {vault_uri}")
    print(f"  name       = {secret.name}")
    print(f"  version    = {secret.properties.version}")
    print(f"  created    = {secret.properties.created_on}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
