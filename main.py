from datetime import UTC, datetime

from src.ingestion.api_client import fetch_api_data
from src.ingestion.duckdb_client import load_raw_data
from src.ingestion.local_storage import save_raw_data


def main() -> None:
    print("Hello from sport-stats-etl-pipeline!")


if __name__ == "__main__":
    main()
    match_endpoint: str = "competitions/PL/teams"  # TODO make endpoints dynamic
    today: datetime = datetime.now(UTC)

    # print(match_endpoint)
    # print(match_table)

    raw_data: dict = fetch_api_data(endpoint=match_endpoint)

    save_raw_data(data=raw_data, entity=match_endpoint, execution_date=today)

    load_raw_data(entity=match_endpoint, execution_date=today)
