from src.ingestion.api_client import fetch_api_data


def test_fetch_api_data_returns_json_on_200(mocker):
    """Returns the parsed JSON body when the API responds with 200."""

    # 1. Arrange
    fake_api_data = {
        "filters": {"season": "2026"},
        "matches": [{"id": 1, "homeTeam": "Arsenal"}],
    }

    # Intercept 'requests.get' inside the api_client file
    mock_get = mocker.patch("src.ingestion.api_client.requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_api_data

    # 2. Act
    # Call actual function which will get intercepted
    result = fetch_api_data(endpoint="matches")

    # 3. Assert
    assert result == fake_api_data
    mock_get.assert_called_once()
