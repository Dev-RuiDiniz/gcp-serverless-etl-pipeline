from typing import Optional
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound

from src.core.logger import logger
from src.core.exceptions import ConfigError


class SecretsService:
    """
    Serviço para acessar segredos do Google Cloud Secret Manager.
    - Acesso à versão (default: "latest")
    - Retorna string com o payload do segredo
    """

    def __init__(self, project_id: Optional[str] = None):
        """
        Se project_id não for informado, tenta inferir do ambiente (GOOGLE_CLOUD_PROJECT).
        """
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id

    def _build_secret_path(self, secret_id: str, version: str = "latest") -> str:
        """
        Retorna o resource name do Secret Manager:
        projects/{project_id}/secrets/{secret_id}/versions/{version}
        """
        if self.project_id:
            project = self.project_id
        else:
            # fallback para variável do ambiente (gcloud define GOOGLE_CLOUD_PROJECT)
            import os
            project = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")

        if not project:
            raise ConfigError("Project id não encontrado. Defina GCP_PROJECT_ID ou GOOGLE_CLOUD_PROJECT.")

        return f"projects/{project}/secrets/{secret_id}/versions/{version}"

    def access_secret(self, secret_id: str, version: str = "latest") -> str:
        """
        Acessa o segredo e retorna o payload como string.
        """
        secret_path = self._build_secret_path(secret_id, version)

        logger.info({"event": "secret_access_start", "secret": secret_id, "version": version})

        try:
            response = self.client.access_secret_version(name=secret_path)
            payload = response.payload.data.decode("UTF-8")
            logger.info({"event": "secret_access_success", "secret": secret_id})
            return payload
        except NotFound:
            logger.error({"event": "secret_access_notfound", "secret": secret_id})
            raise ConfigError(f"Segredo não encontrado: {secret_id}")
        except Exception as e:
            logger.error({"event": "secret_access_error", "secret": secret_id, "error": str(e)})
            raise ConfigError(f"Erro ao acessar segredo {secret_id}: {e}")
