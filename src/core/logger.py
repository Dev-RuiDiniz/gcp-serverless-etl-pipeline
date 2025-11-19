import logging
import json
from pythonjsonlogger import jsonlogger


def configure_logger():
    """
    Configura logging estruturado em JSON,
    ideal para Cloud Functions e observabilidade.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        fmt="%(levelname)s %(asctime)s %(message)s",
        json_indent=2
    )

    log_handler.setFormatter(formatter)
    logger.handlers = [log_handler]

    return logger


# Exporta logger configurado
logger = configure_logger()
