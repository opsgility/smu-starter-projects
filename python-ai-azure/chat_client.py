"""Azure OpenAI chat completion client."""
from openai import AzureOpenAI
import os

def get_client():
    return AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-10-21"
    )

def chat(messages, model="gpt-4o-mini", temperature=0.7, max_tokens=1000):
    client = get_client()
    response = client.chat.completions.create(
        model=model, messages=messages,
        temperature=temperature, max_tokens=max_tokens
    )
    return response.choices[0].message.content
