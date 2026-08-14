import json
from datetime import datetime
from pathlib import Path


def save_raw_data(data: dict, entity: str, execution_date: datetime) -> None:
    """
    Saves the raw data dictionary from the api client as a JSON file in a date partitioned data lake.

    Args:
        data (dict): The raw API response payload to persist

        entity (str): The data domain being saved (e.g. "matches", "standings")

        execution_date (datetime): The Airflow logical date, used to determine the partition path
    """

    year: str = execution_date.strftime("%Y")
    month: str = execution_date.strftime("%m")
    day: str = execution_date.strftime("%d")

    dir_path = Path("storage") / "raw" / entity / year / month / day

    # Defensively create the directory structure
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path: str = dir_path / "data.json"  # TODO replace filename

    with open(file=file_path, mode="w") as f:
        json.dump(obj=data, fp=f, indent=4)
