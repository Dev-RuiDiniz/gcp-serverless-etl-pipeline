import pandas as pd
from unittest.mock import patch, MagicMock
from src.services.bigquery_service import BigQueryService


@patch("google.cloud.bigquery.Client")
def test_bq_load_dataframe(mock_client):
    instance = mock_client.return_value

    mock_job = MagicMock()
    mock_job.job_id = "12345"
    instance.load_table_from_dataframe.return_value = mock_job
    instance.get_table.return_value = MagicMock(num_rows=1)

    service = BigQueryService(project_id="project")
    df = pd.DataFrame({"id": [1]})

    result = service.load_dataframe(df, "dataset", "table")

    assert result["status"] == "success"
    assert instance.load_table_from_dataframe.called
