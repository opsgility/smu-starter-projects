"""Azure OpenAI embeddings and vector search utilities."""
from openai import AzureOpenAI
import os

def get_embedding(text, model="text-embedding-3-small"):
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-10-21"
    )
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
