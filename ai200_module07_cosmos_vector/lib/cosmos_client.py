"""Cosmos client + helpers — Module 7. The student fills in vector_store.py."""
from __future__ import annotations

import os
from functools import lru_cache

from azure.cosmos import CosmosClient, ContainerProxy
from azure.identity import DefaultAzureCredential

DATABASE_NAME = "northwind"
INCIDENTS_CONTAINER = "incidents"
INCIDENT_VECTORS_CONTAINER = "incident_vectors"


@lru_cache(maxsize=1)
def get_client() -> CosmosClient:
    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ.get("COSMOS_KEY")
    if key:
        return CosmosClient(endpoint, credential=key)
    return CosmosClient(endpoint, credential=DefaultAzureCredential())


def get_container(name: str) -> ContainerProxy:
    return get_client().get_database_client(DATABASE_NAME).get_container_client(name)
