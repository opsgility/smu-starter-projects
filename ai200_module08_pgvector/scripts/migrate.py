"""Apply all SQL files in db/migrations/ in lexical order."""
from __future__ import annotations

from pathlib import Path

from lib.pg import get_conn


def main() -> int:
    files = sorted(Path("db/migrations").glob("*.sql"))
    with get_conn() as conn, conn.cursor() as cur:
        for f in files:
            print(f"applying {f.name} ...")
            cur.execute(f.read_text())
        conn.commit()
    print(f"done — applied {len(files)} migration(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
