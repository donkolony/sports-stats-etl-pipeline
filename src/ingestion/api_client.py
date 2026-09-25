import logging

import requests

from src.ingestion.config import API_KEY, BASE_URL, HEADER_KEY

logger = logging.getLogger(__name__)

# Football-Data API auth headers
headers: dict = {HEADER_KEY: API_KEY}


def fetch_api_data(endpoint: str) -> dict:

    url: str = f"{BASE_URL}{endpoint}"

    logger.info(f"Fetching data from API endpoint: {endpoint}")

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()

        logger.info(f"Successfully fetched data from {endpoint}")

    except requests.exceptions.RequestException as e:
        # Log error before the pipeline crashes
        logger.error(f"Failed to fetch data from {endpoint}. Error: {e}")
        raise RuntimeError(f"API failed to fetch data. Details {e}") from e

    return response.json()
