import requests
from src.core.logger import logger
from src.core.exceptions import ExtractError


class Extractor:
    """
    Classe responsável por extrair dados de uma API externa.
    """

    def __init__(self, api_url: str, timeout: int = 10):
        self.api_url = api_url
        self.timeout = timeout

    def fetch_data(self) -> dict:
        logger.info({"event": "extract_start", "url": self.api_url})

        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            logger.info({
                "event": "extract_success",
                "records": len(data) if isinstance(data, list) else 1
            })

            return data

        except Exception as e:
            logger.error({"event": "extract_error", "error": str(e)})
            raise ExtractError(f"Erro ao extrair dados da API: {e}")
