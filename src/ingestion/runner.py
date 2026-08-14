import argparse
from datetime import UTC, datetime

from src.ingestion.api_client import fetch_api_data
from src.ingestion.duckdb_client import load_raw_data
from src.ingestion.local_storage import save_raw_data


def run_ingestion(competition: str, entity: str) -> None:
    """
    Orchestrates the ingestion process for a single entity. Fetches the raw data from
    the API (api_client) and saves it to the local data lake (local_storage)

    Args:
        The league code (e.g., "PL", "BL1")
        entity (str): a single entity (e.g., "matches")
    """

    api_endpoint: str = f"competitions/{competition}/{entity}"

    execution_date: datetime = datetime.now(UTC)

    print(
        f"Starting ingestion for `{entity}` at {execution_date.strftime('%Y-%m-%d %H:%M:S')}..."
    )

    # Extract
    raw_data = fetch_api_data(endpoint=api_endpoint)

    # Save
    saved_file_path = save_raw_data(
        data=raw_data,
        competition=competition,
        entity=entity,
        execution_date=execution_date,
    )

    # Load
    load_raw_data(
        entity=entity, execution_date=execution_date, file_path=saved_file_path
    )

    print(f"Successfully ingested and saved data for `{entity}`")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL Data Pipeline Ingestion Runner!")

    parser.add_argument(
        "--competition",  # optional flag
        type=str,
        default="PL",  # Defaults to Premier League if not provided
        help="The competition code (e.g. PL, BL)",
    )

    # Positional argument
    parser.add_argument(
        "entity",
        type=str,
        help="The name of the entity/endpoint to fetch data for (e.g. matches, teams, and standings)",
    )

    # Parse argument from the command line
    args = parser.parse_args()

    run_ingestion(competition=args.competition, entity=args.entity)
