import json
import os
from datetime import UTC, datetime

from src.ingestion.local_storage import save_raw_data


def test_save_raw_data_writes_json_file_to_disk(tmp_path, mocker):
    """Writes the payload to a JSON file at the path returned by save_raw_data"""

    sample_competition_code = "PL"
    sample_entity = "matches"

    fake_api_data = {
        "id": 2021,
        "name": "Premier League",
        "code": "PL",
    }

    execution_date = datetime.now(UTC)

    # Intercept the pathlib.Path() inside save_raw_data()
    mock_path = mocker.patch("src.ingestion.local_storage.Path", return_value=tmp_path)

    fake_file_path = save_raw_data(
        data=fake_api_data,
        competition_code=sample_competition_code,
        entity=sample_entity,
        execution_date=execution_date,
    )

    assert os.path.exists(fake_file_path) is True
    with open(file=fake_file_path, mode="r") as f:
        saved_data = json.load(f)

    assert saved_data == fake_api_data
