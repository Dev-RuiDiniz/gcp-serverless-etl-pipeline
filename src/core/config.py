import os
from dotenv import load_dotenv

# Carrega variáveis do .env (execução local)
load_dotenv()


class Config:
    """
    Classe responsável por centralizar configurações do projeto.
    Usa variáveis de ambiente para integração com GCP.
    """

    PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    DATASET = os.getenv("BIGQUERY_DATASET")
    TABLE = os.getenv("BIGQUERY_TABLE")

    API_URL = os.getenv("API_URL", "https://servicodados.ibge.gov.br/api/v1/localidades/estados")

    # Cloud Function
    FUNCTION_REGION = os.getenv("FUNCTION_REGION", "southamerica-east1")

    @classmethod
    def validate(cls):
        """Garante que variáveis essenciais estão definidas."""
        required = ["GCP_PROJECT_ID", "BIGQUERY_DATASET", "BIGQUERY_TABLE"]

        missing = [var for var in required if os.getenv(var) is None]

        if missing:
            raise EnvironmentError(
                f"Variáveis de ambiente ausentes: {', '.join(missing)}"
            )
