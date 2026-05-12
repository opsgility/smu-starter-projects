"""Cosmos DB NoSQL connection helper.

Used by all scripts in this module. The student completes the TODOs in
Step 4 of the lab; everything else is pre-written.
"""
from __future__ import annotations

import os
from functools import lru_cache

from azure.cosmos import CosmosClient, ContainerProxy, DatabaseProxy
from azure.identity import DefaultAzureCredential


DATABASE_NAME = "northwind"
CONTAINER_NAME = "shipments"


@lru_cache(maxsize=1)
def get_client() -> CosmosClient:
    """Return a CosmosClient authenticated either via AAD (preferred) or key.

    TODO(step4): replace this NotImplementedError with the real
    implementation. The function must:
      1. Read COSMOS_ENDPOINT from os.environ
      2. If COSMOS_KEY is set in os.environ, return CosmosClient(endpoint, credential=key)
      3. Otherwise return CosmosClient(endpoint, credential=DefaultAzureCredential())
    """
    raise NotImplementedError("Step 4: implement get_client() — see TODO above")


def get_database() -> DatabaseProxy:
    return get_client().get_database_client(DATABASE_NAME)


def get_container() -> ContainerProxy:
    return get_database().get_container_client(CONTAINER_NAME)
