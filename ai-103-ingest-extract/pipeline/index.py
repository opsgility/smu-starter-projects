"""AI Search index definition for the Summitline knowledge base.

Exercise 3 (Lab 2273 / 3408) asks you to implement `ensure_index()` so it
creates (or idempotently updates) the `summitline-knowledge` index with:

  Fields
  ------
    id           : String, key
    source       : String, filterable, facetable, searchable
    doc_type     : String, filterable, facetable
    markdown     : String, searchable
    fields_json  : String
    embedding    : Collection(Single), searchable,
                   vector_search_dimensions=3072,
                   vector_search_profile_name="default"

  Vector search
  -------------
    algorithms : HnswAlgorithmConfiguration(name="default-hnsw")
    profiles   : VectorSearchProfile(name="default",
                                     algorithm_configuration_name="default-hnsw")

  Semantic configuration
  ----------------------
    name = "default"
    prioritized_fields:
      title_fields    -> source
      content_fields  -> markdown
      keywords_fields -> doc_type

3072 is the native output dimension of `text-embedding-3-large`. The index
field dim, the embedding model output, and the query vector length must all
agree or uploads succeed but queries return zero hits.
"""
from __future__ import annotations

import os

from azure.identity import DefaultAzureCredential
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
    """Create or update the `summitline-knowledge` index.

    `create_or_update_index` is idempotent for additive changes. Destructive
    changes (renaming a field, changing a type) fail with 400 and need a
    brand new index.
    """
    # TODO (Exercise 3 Step 1): Build the SearchField list. See the module
    # docstring for exact field names, types, and flags. Remember the vector
    # field's `vector_search_dimensions=3072` and `vector_search_profile_name="default"`.
    fields: list = []

    # TODO (Exercise 3 Step 1): Build the VectorSearch definition with one
    # HnswAlgorithmConfiguration called "default-hnsw" and one
    # VectorSearchProfile called "default" that references it.
    vector = None  # type: ignore[assignment]

    # TODO (Exercise 3 Step 1): Build the SemanticSearch definition with a
    # single SemanticConfiguration named "default" whose prioritized_fields
    # wire source -> title, markdown -> content, doc_type -> keywords.
    semantic = None  # type: ignore[assignment]

    # TODO (Exercise 3 Step 1): Assemble the SearchIndex and call
    # SearchIndexClient(ENDPOINT, CRED).create_or_update_index(index_def).
    raise NotImplementedError("Implement ensure_index in Exercise 3 Step 1.")


if __name__ == "__main__":
    ensure_index()
    print("index ready")
