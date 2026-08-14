import json
from datetime import datetime
from pathlib import Path


def save_raw_data(
    data: dict, competition: str, entity: str, execution_date: datetime
) -> str:
    """
    Saves the raw data dictionary as a JSON file in a date-partitioned data lake.

    Args:
        data (dict): The raw API response payload to persist
        competition (str): The league code (e.g., "PL", "BL1")
        entity (str): The data domain being saved (e.g. "matches", "standings", "teams")
        execution_date (datetime): The Airflow logical date, used to determine the partition path

    Returns:
        str: Hands off state (file path) 
    """

    year: str = execution_date.strftime("%Y")
    month: str = execution_date.strftime("%m")
    day: str = execution_date.strftime("%d")

    dir_path = (
        Path("storage")
        / "raw"
        / "competitions"
        / competition
        / entity
        / year
        / month
        / day
    )

    # Defensively create the directory structure
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / "raw_data.json"

    with open(file=file_path, mode="w") as f:
        json.dump(obj=data, fp=f, indent=4)

    return str(dir_path)
