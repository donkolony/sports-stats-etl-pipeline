import json

from src.ingestion.api_client import fetch_api_data


def main() -> None:
    print("Hello from sport-stats-etl-pipeline!")


if __name__ == "__main__":
    main()
    match_endpoint = "competitions/PL/matches"
    raw_data = fetch_api_data(endpoint=match_endpoint)

    file = "data/raw/data.json"
    with open(file=file, mode="w") as f:
        json.dump(obj=raw_data, fp=f, indent=4)
