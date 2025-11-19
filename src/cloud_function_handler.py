from flask import jsonify, Request  # flask provided in Cloud Functions runtime
from src.core.logger import logger
from src.core.config import Config
from src.core.exceptions import ExtractError, TransformError, LoadError

from src.etl.extractor import Extractor
from src.etl.transformer import Transformer
from src.etl.loader import Loader


def main(request: Request):
    """
    Cloud Functions HTTP entrypoint. Returns JSON response.
    """
    logger.info({"event": "cloud_function_start", "message": "Execution started."})
    try:
        Config.validate()
        extractor = Extractor(base_url=Config.API_URL)
        transformer = Transformer()
        loader = Loader(project_id=Config.PROJECT_ID, location=Config.BQ_LOCATION)

        raw = extractor.fetch_data()
        df = transformer.run(raw)
        result = loader.load(
            df=df,
            dataset_id=Config.DATASET,
            table_id=Config.TABLE,
            write_disposition="WRITE_APPEND",
            create_dataset=True,
            create_table=False
        )

        logger.info({"event": "cloud_function_end", "status": "success", "load_result": result})
        return jsonify({"status": "success", "load_result": result}), 200
    except (ExtractError, TransformError, LoadError) as e:
        logger.error({"event": "cloud_function_etl_error", "error": str(e)})
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        logger.error({"event": "cloud_function_unexpected_error", "error": str(e)})
        return jsonify({"status": "error", "message": str(e)}), 500
