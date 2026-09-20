"""Postgres connection helper.

The student fills in the TODOs in Step 4. The completed module:
- registers pgvector with psycopg
- returns a connection from get_conn() reading PG* env vars
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

import psycopg
from pgvector.psycopg import register_vector


def _conninfo() -> str:
    return (
        f"host={os.environ['PG_HOST']} "
        f"port={os.environ.get('PG_PORT', '5432')} "
        f"dbname={os.environ['PG_DB']} "
        f"user={os.environ['PG_USER']} "
        f"password={os.environ['PG_PASSWORD']} "
        "sslmode=require"
    )


@contextmanager
def get_conn() -> Iterator[psycopg.Connection]:
    """Yield a connection with pgvector registered.

    TODO(step4): replace the NotImplementedError. The function must:
      1. Open psycopg.connect(_conninfo())
      2. Call register_vector(conn) so the `vector` type round-trips as numpy/list
      3. yield conn
      4. On exit, close the connection
    """
    raise NotImplementedError("Step 4: implement get_conn — see TODO above")
