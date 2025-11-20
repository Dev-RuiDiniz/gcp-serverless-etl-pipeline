import pytest
from unittest.mock import patch
from src.etl.extractor import Extractor
from src.core.exceptions import ExtractError


@patch("src.services.api_service.APIService.get")
def test_extractor_success(mock_get):
    mock_get.return_value = [{"id": 1, "nome": "A"}]

    extractor = Extractor(base_url="https://fake.com")
    data = extractor.fetch_data()

    assert isinstance(data, list)
    assert data[0]["id"] == 1


@patch("src.services.api_service.APIService.get")
def test_extractor_error(mock_get):
    mock_get.side_effect = ExtractError("erro")

    extractor = Extractor(base_url="https://fake.com")

    with pytest.raises(ExtractError):
        extractor.fetch_data()
