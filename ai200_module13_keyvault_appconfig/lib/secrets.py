"""Key Vault secret helper.

Student fills in the TODO in Step 4.
"""
from __future__ import annotations

import os
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


@lru_cache(maxsize=1)
def get_secret_client() -> SecretClient:
    """Return a SecretClient bound to the lab's Key Vault.

    TODO(step4a): replace this body. Use:
      - vault_url = os.environ['KEY_VAULT_URL']  # e.g. https://kvai200xxxx.vault.azure.net
      - credential = DefaultAzureCredential()
      - return SecretClient(vault_url=vault_url, credential=credential)
    """
    raise NotImplementedError("Step 4a: implement get_secret_client")


@lru_cache(maxsize=64)
def get_secret(name: str) -> str:
    """Read a secret value by name, cached for the lifetime of the process.

    TODO(step4b): replace this body. Call get_secret_client().get_secret(name)
    and return .value.
    """
    raise NotImplementedError("Step 4b: implement get_secret")
