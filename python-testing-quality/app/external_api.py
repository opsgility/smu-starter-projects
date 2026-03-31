import httpx
import time

API_BASE = "https://api.exchangerate-api.com/v4/latest"

def get_exchange_rate(base_currency, target_currency):
    """Fetch current exchange rate from external API."""
    response = httpx.get(f"{API_BASE}/{base_currency}")
    response.raise_for_status()
    data = response.json()
    return data["rates"].get(target_currency)

def convert_price(amount, from_currency, to_currency):
    """Convert a price between currencies."""
    rate = get_exchange_rate(from_currency, to_currency)
    if rate is None:
        raise ValueError(f"Unknown currency: {to_currency}")
    return round(amount * rate, 2)

def get_exchange_rate_with_retry(base, target, max_retries=3):
    """Fetch exchange rate with retry logic."""
    for attempt in range(max_retries):
        try:
            return get_exchange_rate(base, target)
        except httpx.HTTPError:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
