"""Sanity-check secrets + config + feature flags wiring."""
from __future__ import annotations

import sys

from lib.config import feature_enabled, setting
from lib.secrets import get_secret


def main() -> int:
    s = get_secret("downstream-api-key")
    print(f"[ok] secret length={len(s)}")
    assert s and len(s) >= 4

    cd = setting("northwind:carrier_default")
    cw = setting("northwind:claim_window_hours")
    print(f"[ok] carrier_default={cd}  claim_window_hours={cw}")
    assert cd and cw

    enabled = feature_enabled("fastpath")
    print(f"[ok] feature 'fastpath' enabled={enabled}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
