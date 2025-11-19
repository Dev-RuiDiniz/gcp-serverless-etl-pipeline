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

        extractor = Extractor(api_url=Config.API_URL)
        transformer = Transformer()
        loader = Loader(
            project_id=Config.PROJECT_ID,
            dataset=Config.DATASET,
            table=Config.TABLE
        )

        raw_data = extractor.fetch_data()
        df = transformer.run(raw_data)
        loader.load_dataframe(df)

        logger.info({"event": "etl_finished", "status": "success"})

    except (ExtractError, TransformError, LoadError) as e:
        logger.error({"event": "etl_error", "error": str(e)})
    except Exception as e:
        logger.error({"event": "etl_unexpected_error", "error": str(e)})


if __name__ == "__main__":
    run_etl()
