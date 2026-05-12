"""Redis connection helper for Azure Managed Redis."""
from __future__ import annotations

import os
from functools import lru_cache

import redis


@lru_cache(maxsize=1)
def get_redis() -> redis.Redis:
    """Return a Redis client.

    TODO(step4): replace this body. The function must:
      1. Read REDIS_HOST and REDIS_PORT from os.environ (port defaults to 10000 for Managed Redis SSL)
      2. Read REDIS_PASSWORD from os.environ
      3. Return redis.Redis(host=..., port=..., password=..., ssl=True, decode_responses=False)
         (decode_responses=False is important — vector bytes must round-trip raw)
    """
    raise NotImplementedError("Step 4: implement get_redis — see TODO above")
