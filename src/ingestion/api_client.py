import requests

from src.ingestion.config import API_KEY, BASE_URL, HEADER_KEY

# Football-Data API auth headers
headers: dict = {HEADER_KEY: API_KEY}


def fetch_api_data(endpoint: str) -> dict:

    full_url: str = f"{BASE_URL}{endpoint}"

    try:
        response = requests.get(url=full_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API failed to fetch data. Details {e}") from e

    return response.json()
