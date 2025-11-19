from typing import Optional, List, Dict, Any
import pandas as pd

from google.cloud import bigquery
from google.api_core.exceptions import NotFound, Conflict

from src.core.logger import logger
from src.core.exceptions import LoadError


class BigQueryService:
    """
    Serviço de alto nível para operações com BigQuery.
    - Cria dataset/tabela se não existirem (create_if_not_exists)
    - Carrega DataFrame de forma segura (load_table_from_dataframe)
    - Permite execução de queries
    """

    def __init__(self, project_id: str, location: str = "US"):
        self.project_id = project_id
        self.client = bigquery.Client(project=self.project_id)
        self.location = location

    # ---------- Helpers ----------
    def _dataset_ref(self, dataset_id: str) -> bigquery.DatasetReference:
        return bigquery.DatasetReference(self.project_id, dataset_id)

    def _table_ref(self, dataset_id: str, table_id: str) -> bigquery.TableReference:
        dataset_ref = self._dataset_ref(dataset_id)
        return dataset_ref.table(table_id)

    # ---------- Create if not exists ----------
    def create_dataset_if_not_exists(self, dataset_id: str, description: Optional[str] = None) -> None:
        """
        Cria um dataset se não existir.
        """
        dataset_ref = self._dataset_ref(dataset_id)
        try:
            self.client.get_dataset(dataset_ref)
            logger.info({"event": "bigquery_dataset_exists", "dataset": f"{self.project_id}.{dataset_id}"})
            return
        except NotFound:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = self.location
            if description:
                dataset.description = description

            try:
                self.client.create_dataset(dataset)
                logger.info({"event": "bigquery_dataset_created", "dataset": f"{self.project_id}.{dataset_id}"})
            except Conflict:
                # race condition: dataset created by another process
                logger.info({"event": "bigquery_dataset_conflict", "dataset": f"{self.project_id}.{dataset_id}"})
            except Exception as e:
                logger.error({"event": "bigquery_dataset_create_error", "dataset": dataset_id, "error": str(e)})
                raise LoadError(f"Erro ao criar dataset {dataset_id}: {e}")

    def create_table_if_not_exists(self, dataset_id: str, table_id: str, schema: Optional[List[bigquery.SchemaField]] = None) -> None:
        """
        Cria uma tabela no BigQuery se não existir.
        - schema: lista de bigquery.SchemaField (opcional). Se não informado, a tabela será criada no primeiro load automático (schema inferred).
        """
        table_ref = self._table_ref(dataset_id, table_id)

        try:
            self.client.get_table(table_ref)
            logger.info({"event": "bigquery_table_exists", "table": f"{self.project_id}.{dataset_id}.{table_id}"})
            return
        except NotFound:
            table = bigquery.Table(table_ref, schema=schema)
            try:
                self.client.create_table(table)
                logger.info({"event": "bigquery_table_created", "table": f"{self.project_id}.{dataset_id}.{table_id}"})
            except Conflict:
                logger.info({"event": "bigquery_table_conflict", "table": f"{self.project_id}.{dataset_id}.{table_id}"})
            except Exception as e:
                logger.error({"event": "bigquery_table_create_error", "table": f"{dataset_id}.{table_id}", "error": str(e)})
                raise LoadError(f"Erro ao criar tabela {dataset_id}.{table_id}: {e}")

    # ---------- Load DataFrame ----------
    def load_dataframe(
        self,
        df: pd.DataFrame,
        dataset_id: str,
        table_id: str,
        write_disposition: str = "WRITE_APPEND",
        create_dataset: bool = True,
        create_table: bool = False,
        table_schema: Optional[List[bigquery.SchemaField]] = None,
        job_labels: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Carrega um pandas DataFrame no BigQuery.
        - write_disposition: "WRITE_APPEND" | "WRITE_TRUNCATE" | "WRITE_EMPTY"
        - create_dataset: cria dataset se não existir
        - create_table: cria tabela com schema (se informado) se não existir
        - table_schema: lista de bigquery.SchemaField para criar a tabela (opcional)
        """

        if df is None or df.empty:
            logger.info({"event": "bigquery_load_skipped", "reason": "empty_dataframe"})
            return {"status": "skipped", "reason": "empty_dataframe"}

        # Garantir dataset
        if create_dataset:
            self.create_dataset_if_not_exists(dataset_id)

        # Possível criação de tabela
        if create_table and table_schema:
            self.create_table_if_not_exists(dataset_id, table_id, schema=table_schema)

        table_ref = self._table_ref(dataset_id, table_id)
        table_id_full = f"{self.project_id}.{dataset_id}.{table_id}"

        logger.info({
            "event": "bigquery_load_start",
            "table": table_id_full,
            "records": len(df)
        })

        job_config = bigquery.LoadJobConfig()
        # Mapeia string para enum
        if write_disposition == "WRITE_TRUNCATE":
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        elif write_disposition == "WRITE_EMPTY":
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
        else:
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

        if table_schema:
            job_config.schema = table_schema

        if job_labels:
            job_config.labels = job_labels

        try:
            load_job = self.client.load_table_from_dataframe(df, table_ref, job_config=job_config, location=self.location)
            result = load_job.result()  # bloqueia até finalizar

            logger.info({
                "event": "bigquery_load_success",
                "table": table_id_full,
                "total_rows": self.client.get_table(table_ref).num_rows,
                "load_job_id": load_job.job_id
            })

            return {"status": "success", "job_id": load_job.job_id, "total_rows": self.client.get_table(table_ref).num_rows}

        except Exception as e:
            logger.error({"event": "bigquery_load_error", "table": table_id_full, "error": str(e)})
            raise LoadError(f"Erro ao carregar DataFrame no BigQuery: {e}")

    # ---------- Query ----------
    def run_query(self, query: str, job_config: Optional[bigquery.QueryJobConfig] = None) -> List[Dict[str, Any]]:
        """
        Executa query no BigQuery e retorna uma lista de dicts.
        """
        logger.info({"event": "bigquery_query_start", "query": query[:200]})
        try:
            query_job = self.client.query(query, job_config=job_config)
            result = query_job.result()
            rows = [dict(row) for row in result]
            logger.info({"event": "bigquery_query_success", "rows": len(rows)})
            return rows
        except Exception as e:
            logger.error({"event": "bigquery_query_error", "error": str(e)})
            raise LoadError(f"Erro ao executar query no BigQuery: {e}")
