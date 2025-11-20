import pandas as pd
from unittest.mock import patch, MagicMock

from src.etl.loader import Loader


@patch("src.services.bigquery_service.BigQueryService.load_dataframe")
def test_loader_calls_bigquery_service(mock_load):
    mock_load.return_value = {"status": "success"}

    loader = Loader(project_id="test-project")
    df = pd.DataFrame({"id": [1]})

    result = loader.load(
        df=df,
        dataset_id="dataset",
        table_id="table",
        create_dataset=False,
        create_table=False,
    )

    mock_load.assert_called_once()
    assert result["status"] == "success"
