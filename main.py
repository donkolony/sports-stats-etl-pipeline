from datetime import UTC, datetime

from src.ingestion.api_client import fetch_api_data
from src.ingestion.local_storage import save_raw_data


def main() -> None:

    print("Hello from sport-stats-etl-pipeline!")

    competition = "PL"
    entity = "matches"

    api_endpoint = f"competitions/{competition}/{entity}"

    today: datetime = datetime.now(UTC)

    print(f"Fetching {entity} for {competition}")

    # Extract
    raw_data: dict = fetch_api_data(endpoint=api_endpoint)

    # Load
    save_raw_data(
        data=raw_data, competition=competition, entity=entity, execution_date=today
    )

    print("Successfully loaded!")


if __name__ == "__main__":
    main()
