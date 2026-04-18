"""AI Search index schema + upload."""
import os

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    VectorSearch,
    VectorSearchProfile,
)
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
INDEX = os.environ["AZURE_SEARCH_INDEX"]
CRED = DefaultAzureCredential()


def ensure_index() -> None:
    # TODO 1: Build SearchIndex with fields:
    #         id, source (filterable), doc_type (filterable), markdown (searchable),
    #         fields_json (Edm.String), embedding (Collection(Single), dims=1536, profile="default")
    # TODO 2: VectorSearch with HnswAlgorithmConfiguration("default-hnsw") + VectorSearchProfile("default", "default-hnsw")
    # TODO 3: SemanticSearch with config "default" → prioritize markdown content + doc_type
    # TODO 4: SearchIndexClient(ENDPOINT, CRED).create_or_update_index(index)
    raise NotImplementedError


def upload(documents: list[dict]) -> None:
    SearchClient(ENDPOINT, INDEX, CRED).upload_documents(documents=documents)
