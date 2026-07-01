from src.ingestion.api_client import fetch_api_data

if __name__ == "__main__":
    # Test the endpoints
    match_endpoint = "matches"

    print(f"Fetching data from endpoint: {match_endpoint}...")
    res = fetch_api_data(match_endpoint)

    print(res["matches"])
