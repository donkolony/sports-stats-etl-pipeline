import argparse
from datetime import UTC, datetime

from src.ingestion.api_client import fetch_api_data
from src.ingestion.config import AVAILABLE_ENTITIES, COMPETITION_MAP
from src.ingestion.duckdb_client import load_raw_data
from src.ingestion.local_storage import save_raw_data


def run_ingestion(competition_code: str, entity: str) -> None:
    """
    Orchestrates the ingestion process for a single entity. Fetches the raw data from
    the API (api_client) and saves it to the local data lake (local_storage)

    Args:
        The league code (e.g., "PL", "BL1")
        entity (str): a single entity (e.g., "matches")
    """

    if competition_code not in COMPETITION_MAP:
        raise ValueError(
            f"Invalid competition: {competition_code}. Valid options are: {list(COMPETITION_MAP.keys())}"
        )

    if entity not in AVAILABLE_ENTITIES:
        raise ValueError(
            f"Invalid entity: {entity}. Valid options are: {AVAILABLE_ENTITIES}"
        )

    api_endpoint: str = f"competitions/{competition_code}/{entity}"
    execution_date: datetime = datetime.now(UTC)
    league = COMPETITION_MAP.get(competition_code)

    print(
        f"Starting ingestion for `{entity}` in the {league} at {execution_date.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Extract
    raw_data = fetch_api_data(endpoint=api_endpoint)

    # Save
    saved_file_path = save_raw_data(
        data=raw_data,
        competition_code=competition_code,
        entity=entity,
        execution_date=execution_date,
    )

    # Load
    load_raw_data(
        entity=entity, execution_date=execution_date, file_path=saved_file_path
    )

    print(f"Successfully ingested and saved data for `{entity}` in the {league}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL Data Pipeline Ingestion Runner!")

    parser.add_argument(
        "-c",
        "--competition",  # optional flag
        type=str,
        default="PL",  # Defaults to Premier League if not provided
        choices=COMPETITION_MAP,
        help=f"The competition code (e.g. {list(COMPETITION_MAP.keys())})",
    )

    # Positional argument
    parser.add_argument(
        "entity",
        type=str,
        choices=list(AVAILABLE_ENTITIES),
        help=f"The name of the entity/endpoint to fetch data for (e.g. {AVAILABLE_ENTITIES})",
    )

    # Parse argument from the command line
    args = parser.parse_args()

    run_ingestion(competition_code=args.competition, entity=args.entity)
