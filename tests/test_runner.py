from src.ingestion.runner import run_ingestion


def test_run_ingestion_calls_fetch_save_and_load_in_order(mocker):
    """Orchestrates fetch -> save -> load with the correct args for a single entity"""

    sample_competition_code = "PL"
    sample_entity = "matches"
    expected_endpoint = f"competitions/{sample_competition_code}/{sample_entity}"

    fake_api_data = {"data": "fake_data"}
    fake_file_path = "fake/path/to/raw_data.json"

    mock_fetch = mocker.patch(
        "src.ingestion.runner.fetch_api_data", return_value=fake_api_data
    )
    mock_save = mocker.patch(
        "src.ingestion.runner.save_raw_data", return_value=fake_file_path
    )
    mock_load = mocker.patch("src.ingestion.runner.load_raw_data")

    run_ingestion(competition_code=sample_competition_code, entity=sample_entity)

    mock_fetch.assert_called_once_with(endpoint=expected_endpoint)
    mock_save.assert_called_once_with(
        data=fake_api_data,
        competition_code=sample_competition_code,
        entity=sample_entity,
        execution_date=mocker.ANY,
    )
    mock_load.assert_called_once_with(
        entity=sample_entity, execution_date=mocker.ANY, file_path=fake_file_path
    )
