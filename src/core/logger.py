import logging
from pythonjsonlogger import jsonlogger


def configure_logger():
    """
    Configura logging estruturado em JSON,
    ideal para Cloud Functions e observabilidade.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        fmt="%(levelname)s %(asctime)s %(message)s",
        json_indent=2
    )

    handler.setFormatter(formatter)
    logger.handlers = [handler]

    return logger


logger = configure_logger()
