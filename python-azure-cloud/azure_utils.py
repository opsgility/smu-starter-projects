"""Utility functions for Azure SDK operations."""
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
import os

def get_credential():
    return DefaultAzureCredential()

def get_resource_client(subscription_id=None):
    sub_id = subscription_id or os.getenv("AZURE_SUBSCRIPTION_ID")
    if not sub_id:
        raise ValueError("AZURE_SUBSCRIPTION_ID not set")
    return ResourceManagementClient(get_credential(), sub_id)
