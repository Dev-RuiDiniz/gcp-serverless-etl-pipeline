from src.services.api_service import APIService
from src.core.logger import logger
from src.core.exceptions import ExtractError


class Extractor:
    """
    Extractor now uses APIService for robust HTTP calls.
    """

    def __init__(self, base_url: str, timeout: int = 10):
        self.service = APIService(base_url=base_url, timeout=timeout)

    def fetch_data(self, endpoint: str = "", params: dict | None = None):
        logger.info({"event": "extract_start", "url": self.service.base_url, "endpoint": endpoint})
        try:
            data = self.service.get(endpoint=endpoint, params=params)
            logger.info({
                "event": "extract_success",
                "records": len(data) if isinstance(data, list) else 1
            })
            return data
        except ExtractError as e:
            logger.error({"event": "extract_error", "error": str(e)})
            raise
        except Exception as e:
            logger.error({"event": "extract_unexpected_error", "error": str(e)})
            raise ExtractError(f"Erro inesperado na extração: {e}")
