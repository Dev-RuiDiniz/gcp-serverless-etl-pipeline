import time
import requests
from typing import Optional, Any, Dict

from src.core.logger import logger
from src.core.exceptions import ExtractError


class APIService:
    """
    HTTP client with exponential backoff retries, timeout and structured logs.
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.headers = headers or {"Content-Type": "application/json"}

    def get(self, endpoint: str = "", params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        for attempt in range(1, self.max_retries + 1):
            logger.info({
                "event": "api_request_start",
                "url": url,
                "attempt": attempt
            })
            try:
                resp = requests.get(url, headers=self.headers, timeout=self.timeout, params=params)
                resp.raise_for_status()
                logger.info({
                    "event": "api_request_success",
                    "status_code": resp.status_code
                })
                return resp.json()
            except Exception as e:
                logger.error({
                    "event": "api_request_error",
                    "url": url,
                    "attempt": attempt,
                    "error": str(e)
                })
                if attempt < self.max_retries:
                    sleep_time = self.backoff_factor ** attempt
                    logger.info({"event": "api_retry_wait", "sleep_seconds": sleep_time})
                    time.sleep(sleep_time)
                else:
                    raise ExtractError(f"Failed to GET {url} after {self.max_retries} attempts: {e}")
