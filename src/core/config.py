import os
from dotenv import load_dotenv

# Load .env for local execution
load_dotenv()


class Config:
    """
    Central configuration class.
    """

    PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    DATASET = os.getenv("BIGQUERY_DATASET")
    TABLE = os.getenv("BIGQUERY_TABLE")

    API_URL = os.getenv(
        "API_URL",
        "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    )

    FUNCTION_REGION = os.getenv("FUNCTION_REGION", "southamerica-east1")
    BQ_LOCATION = os.getenv("BIGQUERY_LOCATION", "US")

    @classmethod
    def validate(cls):
        required = ["GCP_PROJECT_ID", "BIGQUERY_DATASET", "BIGQUERY_TABLE"]
        missing = [var for var in required if os.getenv(var) is None]

        if missing:
            raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(missing)}")
