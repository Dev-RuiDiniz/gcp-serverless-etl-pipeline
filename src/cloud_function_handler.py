from src.core.logger import logger
from src.core.config import Config
from src.core.exceptions import ExtractError, TransformError, LoadError

from src.etl.extractor import Extractor
from src.etl.transformer import Transformer
from src.etl.loader import Loader


def main(request):
    """
    Função principal usada pelo Google Cloud Functions.
    Trigger HTTP.
    """

    logger.info({"event": "cloud_function_start", "message": "Execução iniciada."})

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

        logger.info({"event": "cloud_function_end", "status": "success"})
        return {"status": "success", "message": "Pipeline executado com sucesso."}

    except (ExtractError, TransformError, LoadError) as e:
        logger.error({"event": "cloud_function_etl_error", "error": str(e)})
        return {"status": "error", "message": str(e)}, 500

    except Exception as e:
        logger.error({"event": "cloud_function_unexpected_error", "error": str(e)})
        return {"status": "error", "message": str(e)}, 500
