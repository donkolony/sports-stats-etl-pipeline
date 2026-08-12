from datetime import datetime

from src.ingestion.api_client import fetch_api_data
from src.ingestion.local_storage import save_raw_data


def main() -> None:
    print("Hello from sport-stats-etl-pipeline!")


if __name__ == "__main__":
    main()
    match_endpoint: str = "competitions/PL/teams"  # TODO make endpoints dynamic
    today: datetime = datetime.now()

    raw_data: dict = fetch_api_data(endpoint=match_endpoint)

    save_raw_data(data=raw_data, entity=match_endpoint, execution_date=today)
