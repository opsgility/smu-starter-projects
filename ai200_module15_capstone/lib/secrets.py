"""Key Vault helper — pre-written, used by the FastAPI app on boot."""
from __future__ import annotations

import os
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


@lru_cache(maxsize=1)
def get_secret_client() -> SecretClient:
    return SecretClient(vault_url=os.environ["KEY_VAULT_URL"], credential=DefaultAzureCredential())


@lru_cache(maxsize=64)
def get_secret(name: str) -> str:
    return get_secret_client().get_secret(name).value or ""
