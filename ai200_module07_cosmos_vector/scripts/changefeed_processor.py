"""Run the change feed processor once. Reads continuation from .checkpoint."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from lib.change_feed import run_once

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
CHECKPOINT = Path(".checkpoint")


def main() -> int:
    cont = CHECKPOINT.read_text().strip() if CHECKPOINT.exists() else None
    next_cont = run_once(continuation=cont)
    if next_cont:
        CHECKPOINT.write_text(next_cont)
    print(f"checkpoint -> {CHECKPOINT}: {next_cont[:32] if next_cont else '(none)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
