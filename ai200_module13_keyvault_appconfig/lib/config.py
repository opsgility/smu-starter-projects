"""App Configuration helper with feature-flag support.

The student completes the TODOs in Step 6.
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from azure.appconfiguration.provider import (
    AzureAppConfigurationProvider,
    SettingSelector,
    load,
)
from azure.identity import DefaultAzureCredential


@lru_cache(maxsize=1)
def get_config() -> AzureAppConfigurationProvider:
    """Load and return the App Configuration provider, resolving KV references.

    TODO(step6a): replace this body. Call azure.appconfiguration.provider.load(
        endpoint=os.environ['APP_CONFIG_ENDPOINT'],
        credential=DefaultAzureCredential(),
        selects=[SettingSelector(key_filter='northwind:*')],
        feature_flag_enabled=True,
    ) and return the result.

    The provider will automatically resolve any KV references to Key Vault
    using the same credential.
    """
    raise NotImplementedError("Step 6a: implement get_config")


def setting(key: str, default: Any = None) -> Any:
    """Read a normal config setting."""
    return get_config().get(key, default)


def feature_enabled(name: str) -> bool:
    """Read a feature flag.

    TODO(step6b): replace this body. Use:
        flag = get_config().get_feature_flag(name)
        return bool(flag and flag.enabled)
    """
    raise NotImplementedError("Step 6b: implement feature_enabled")
