from src.core.config import Config
from src.core.logger import logger
from src.core.exceptions import ExtractError, TransformError, LoadError

from src.etl.extractor import Extractor
from src.etl.transformer import Transformer
from src.etl.loader import Loader


def run_etl():
    logger.info({"event": "etl_start", "message": "Pipeline ETL iniciado localmente."})
    try:
        Config.validate()
        extractor = Extractor(base_url=Config.API_URL)
        transformer = Transformer()
        loader = Loader(project_id=Config.PROJECT_ID, location=Config.BQ_LOCATION)

        # Extract
        raw = extractor.fetch_data()
        # Transform
        df = transformer.run(raw)
        # Load
        result = loader.load(
            df=df,
            dataset_id=Config.DATASET,
            table_id=Config.TABLE,
            write_disposition="WRITE_APPEND",
            create_dataset=True,
            create_table=False,
            table_schema=None
        )

        logger.info({"event": "etl_finished", "status": "success", "load_result": result})
    except (ExtractError, TransformError, LoadError) as e:
        logger.error({"event": "etl_error", "error": str(e)})
    except Exception as e:
        logger.error({"event": "etl_unexpected_error", "error": str(e)})


if __name__ == "__main__":
    run_etl()
