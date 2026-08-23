"""Print the Foundry account's system-assigned managed identity + every role
assignment it holds. Zero Trust check: the ONLY role assignment on the MI
should be 'Cognitive Services OpenAI User' scoped to the Foundry account.

Anything broader (Contributor, Owner, subscription-scope roles, additional
data-plane roles) is a finding — flag it in Exercise 4 Task 3.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

from dotenv import load_dotenv


def _run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def main() -> int:
    load_dotenv()
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "")
    if "services.ai.azure.com" not in endpoint:
        print("FOUNDRY_PROJECT_ENDPOINT not set in .env")
        return 1
    account_name = endpoint.split("//", 1)[1].split(".", 1)[0]

    print(f"Foundry account: {account_name}")
    print("Locating in current subscription…")

    try:
        acct_id = _run(
            ["az", "cognitiveservices", "account", "show", "--name", account_name,
             "--resource-group", _find_rg(account_name), "--query", "id", "-o", "tsv"]
        ).strip()
        mi_pid = _run(
            ["az", "cognitiveservices", "account", "show", "--name", account_name,
             "--resource-group", _find_rg(account_name), "--query", "identity.principalId", "-o", "tsv"]
        ).strip()
    except subprocess.CalledProcessError as exc:
        print(f"  az call failed: {exc.stderr}")
        return 1

    if not mi_pid:
        print("  Foundry has NO system-assigned managed identity — expected the ARM template to set one.")
        return 1

    print(f"  MI object id : {mi_pid}")
    print(f"  Foundry id   : {acct_id}")
    print("\nRole assignments held by the MI (subscription scope + below):")

    role_json = _run(["az", "role", "assignment", "list", "--assignee", mi_pid, "--all", "-o", "json"])
    roles = json.loads(role_json)
    if not roles:
        print("  (none)")
        return 1

    for r in roles:
        print(f"  - {r['roleDefinitionName']}  @  {r['scope']}")

    ok_names = {"Cognitive Services OpenAI User"}
    findings = [r for r in roles if r["roleDefinitionName"] not in ok_names]
    if findings:
        print("\n  ZERO TRUST FINDING: MI holds roles beyond least-privilege:")
        for r in findings:
            print(f"    {r['roleDefinitionName']} @ {r['scope']}")
        return 2

    print("\n  OK — MI holds only 'Cognitive Services OpenAI User'. Least-privilege posture confirmed.")
    return 0


def _find_rg(account_name: str) -> str:
    """Look up the resource group of the Foundry account by name — the RG name is not in .env."""
    out = _run(
        ["az", "cognitiveservices", "account", "list", "--query",
         f"[?name=='{account_name}'].resourceGroup", "-o", "tsv"]
    ).strip()
    if not out:
        raise SystemExit(f"Could not find resource group for account {account_name!r}")
    return out


if __name__ == "__main__":
    sys.exit(main())
