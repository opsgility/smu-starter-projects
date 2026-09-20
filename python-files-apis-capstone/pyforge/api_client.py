"""API client for fetching data with pagination."""
import requests


class ApiClient:
    """Fetches data from a REST API with pagination support."""

    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"

    def fetch_all(self, endpoint, params=None):
        """Fetch all pages of data from an endpoint."""
        # TODO: Implement paginated fetching
        # 1. Make GET request to base_url + endpoint
        # 2. Parse JSON response
        # 3. If there's a "next" page, keep fetching
        # 4. Return all results as a list
        raise NotImplementedError("Implement fetch_all")
