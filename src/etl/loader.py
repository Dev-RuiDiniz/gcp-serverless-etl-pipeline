from google.cloud import bigquery
from src.core.logger import logger
from src.core.exceptions import LoadError


class Loader:
    """
    Classe responsável por carregar dados no BigQuery.
    POO + SOLID — cada classe com uma responsabilidade.
    """

    def __init__(self, project_id: str, dataset: str, table: str):
        self.project_id = project_id
        self.dataset = dataset
        self.table = table
        self.client = bigquery.Client(project=project_id)

    @property
    def table_id(self) -> str:
        return f"{self.project_id}.{self.dataset}.{self.table}"

    def load_dataframe(self, df):
        logger.info({
            "event": "load_start",
            "table": self.table_id,
            "records": len(df)
        })

        try:
            job = self.client.load_table_from_dataframe(df, self.table_id)
            job.result()  # Espera o job finalizar

            logger.info({
                "event": "load_success",
                "table": self.table_id,
                "records_loaded": len(df)
            })

        except Exception as e:
            logger.error({
                "event": "load_error",
                "error": str(e)
            })
            raise LoadError(f"Erro ao carregar dados no BigQuery: {e}")
