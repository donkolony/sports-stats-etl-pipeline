
from src.ingestion.api_client import fetch_api_data


def test_fetch_api_data_sucess(mocker):
    # 1. Arrange
    mocker_response_data = {
        "filters": {"season": "2026"},
        "matches": [{"id": 1, "homeTeam": "Arsenal"}],
    }

    # Intercept 'requests.get' inside the api_client file
    mock_get = mocker.patch("src.ingestion.api_client.requests.get")

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mocker_response_data

    # 2. Act
    # Call actual function which will get intercepted
    result = fetch_api_data("matches")


    # 3. Assert
    assert result == mocker_response_data
    mock_get.assert_called_once()
    