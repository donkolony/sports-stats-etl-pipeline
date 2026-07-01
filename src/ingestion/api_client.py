import requests

from src.ingestion.config import API_KEY, BASE_URL

# Football-Data API auth header
headers = {"X-Auth-Token": API_KEY}


def fetch_api_data(endpoint: str) -> dict:
    """
    Fetches JSON data from the Football-Data.org API using a dynamically provided endpoint

    Args:
        endpoint (str): The specific API path to append to the base URL

    Raises:
        RuntimeError: If the HTTP request fails (e.g., 404 Not Found, 429 Too Many Requests).
                      ensuring the pipeline crashes immediately rather than passing bad data.

    Returns:
        dict: The raw API response parsed into a Python dictionary
    """

    full_url = f"{BASE_URL}{endpoint}"

    try:
        res = requests.get(full_url, headers=headers)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Chain the exception to provide a custom, readable error message for Airflow
        # while preserving the original traceback context
        raise RuntimeError(f"API Request failed to fetch data. Details: {e}") from e

    return res.json()
