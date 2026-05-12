"""Cosmos vector store helper — lifted from Module 7, used in the capstone API."""
from __future__ import annotations

import os
from functools import lru_cache

from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

DATABASE_NAME = "northwind"
INCIDENT_VECTORS = "incident_vectors"


@lru_cache(maxsize=1)
def _client() -> CosmosClient:
    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ.get("COSMOS_KEY")
    if key:
        return CosmosClient(endpoint, credential=key)
    return CosmosClient(endpoint, credential=DefaultAzureCredential())


def container():
    return _client().get_database_client(DATABASE_NAME).get_container_client(INCIDENT_VECTORS)


def search(query_embedding: list[float], tenant: str, top_k: int = 5) -> list[dict]:
    query = (
        "SELECT TOP @k c.id, c.text, c.metadata, "
        "VectorDistance(c.embedding, @q) AS score "
        "FROM c WHERE c.tenantId = @tenant "
        "ORDER BY VectorDistance(c.embedding, @q)"
    )
    params = [
        {"name": "@k", "value": top_k},
        {"name": "@q", "value": query_embedding},
        {"name": "@tenant", "value": tenant},
    ]
    return list(container().query_items(
        query=query, parameters=params, partition_key=tenant,
    ))
