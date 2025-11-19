import time
import requests
from typing import Optional

from src.core.logger import logger
from src.core.exceptions import ExtractError


class APIService:
    """
    Serviço responsável por realizar requisições HTTP com:
    - Retry exponencial
    - Timeout configurável
    - Headers opcionais
    - Logging estruturado
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
        headers: Optional[dict] = None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.headers = headers or {"Content-Type": "application/json"}

    def get(self, endpoint: str = "") -> dict:
        """
        Executa requisição GET profissional com retry exponencial.
        """

        url = f"{self.base_url}{endpoint}"

        for attempt in range(1, self.max_retries + 1):

            logger.info({
                "event": "api_request_start",
                "url": url,
                "attempt": attempt
            })

            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=self.timeout
                )

                response.raise_for_status()

                logger.info({
                    "event": "api_request_success",
                    "status_code": response.status_code,
                })

                return response.json()

            except Exception as e:
                logger.error({
                    "event": "api_request_error",
                    "attempt": attempt,
                    "error": str(e)
                })

                # Se ainda há tentativas restantes, aguardar com backoff
                if attempt < self.max_retries:
                    sleep_time = self.backoff_factor ** attempt
                    logger.info({
                        "event": "api_retry_wait",
                        "sleep_seconds": sleep_time
                    })
                    time.sleep(sleep_time)
                else:
                    raise ExtractError(
                        f"Falha ao consumir API após {self.max_retries} tentativas: {e}"
                    )
        raise ExtractError("Falha desconhecida ao consumir API.")
    