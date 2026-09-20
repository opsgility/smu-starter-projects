"""Cache-aside wrapper around an embedding lookup. The student completes
the TODOs in Step 6.
"""
from __future__ import annotations

import hashlib
import json
import time
from typing import Callable

from lib.redis_client import get_redis


def _key(prompt: str) -> str:
    h = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    return f"completion:{h}"


def cached_call(prompt: str, fn: Callable[[str], str], ttl_seconds: int = 3600) -> tuple[str, bool]:
    """Return (result, cache_hit).

    TODO(step6): replace this body. The function must:
      1. Compute key = _key(prompt)
      2. Try r.get(key); if present, return (value.decode(), True)
      3. Else call fn(prompt), then r.set(key, value, ex=ttl_seconds)
      4. Return (value, False)
    """
    raise NotImplementedError("Step 6: implement cached_call — see TODO above")
