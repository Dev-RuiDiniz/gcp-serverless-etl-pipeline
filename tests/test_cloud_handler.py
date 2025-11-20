from unittest.mock import patch, MagicMock
from src.cloud_function_handler import main


class MockRequest:
    def __init__(self, json_data=None):
        self._json = json_data

    def get_json(self):
        return self._json


@patch("src.etl.loader.Loader.load")
@patch("src.etl.transformer.Transformer.run")
@patch("src.etl.extractor.Extractor.fetch_data")
def test_cloud_fn_success(mock_extract, mock_transform, mock_load):
    mock_extract.return_value = [{"id": 1}]
    mock_transform.return_value = [{"id": 1}]
    mock_load.return_value = {"status": "success"}

    req = MockRequest()
    response, status = main(req)

    assert status == 200
    assert response.json["status"] == "success"
