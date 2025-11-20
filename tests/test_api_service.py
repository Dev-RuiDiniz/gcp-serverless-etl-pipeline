import pytest
from unittest.mock import patch, MagicMock
from src.services.api_service import APIService


@patch("requests.get")
def test_api_service_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"ok": True}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    api = APIService(base_url="https://example.com")
    result = api.get()

    assert result == {"ok": True}
    mock_get.assert_called_once()


@patch("requests.get")
def test_api_service_retry(mock_get):
    mock_get.side_effect = Exception("Network error")

    api = APIService(base_url="https://example.com", max_retries=2)

    with pytest.raises(Exception):
        api.get()

    assert mock_get.call_count == 2
