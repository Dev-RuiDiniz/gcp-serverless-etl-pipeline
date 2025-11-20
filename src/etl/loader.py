from typing import Optional, List
import pandas as pd
from google.cloud import bigquery

from src.services.bigquery_service import BigQueryService
from src.core.logger import logger
from src.core.exceptions import LoadError


class Loader:
    """
    Loader delegates to BigQueryService for dataset/table creation and dataframe loads.
    """

    def __init__(self, project_id: str, location: str = "US"):
        self.bq = BigQueryService(project_id=project_id, location=location)

    def load(self,
             df: pd.DataFrame,
             dataset_id: str,
             table_id: str,
             write_disposition: str = "WRITE_APPEND",
             create_dataset: bool = True,
             create_table: bool = False,
             table_schema: Optional[List[bigquery.SchemaField]] = None):
        try:
            result = self.bq.load_dataframe(
                df=df,
                dataset_id=dataset_id,
                table_id=table_id,
                write_disposition=write_disposition,
                create_dataset=create_dataset,
                create_table=create_table,
                table_schema=table_schema,
            )
            return result
        except Exception as e:
            logger.error({"event": "loader_error", "error": str(e)})
            raise LoadError(f"Erro no loader: {e}")

from src.models.schema_definition import IBGE_STATE_SCHEMA

result = loader.load(
    df=df,
    dataset_id=Config.DATASET,
    table_id=Config.TABLE,
    write_disposition="WRITE_APPEND",
    create_dataset=True,
    create_table=True,
    table_schema=IBGE_STATE_SCHEMA
)
