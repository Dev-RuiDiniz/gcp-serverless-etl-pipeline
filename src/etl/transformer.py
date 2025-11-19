import pandas as pd
from src.core.logger import logger
from src.core.exceptions import TransformError


class Transformer:
    """
    Classe responsável pela transformação dos dados.
    """

    def to_dataframe(self, raw_data: dict | list) -> pd.DataFrame:
        logger.info({"event": "transform_start"})

        try:
            df = pd.DataFrame(raw_data)

            logger.info({
                "event": "transform_dataframe_success",
                "shape": df.shape
            })

            return df

        except Exception as e:
            logger.error({"event": "transform_error", "error": str(e)})
            raise TransformError(f"Erro ao transformar dados em DataFrame: {e}")

    def clean_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df.columns = (
                df.columns
                .str.lower()
                .str.replace(" ", "_")
                .str.replace("-", "_")
            )

            logger.info({"event": "transform_clean_columns", "columns": df.columns.tolist()})

            return df

        except Exception as e:
            raise TransformError(f"Erro ao limpar colunas: {e}")

    def run(self, raw_data: dict | list) -> pd.DataFrame:
        df = self.to_dataframe(raw_data)
        df = self.clean_columns(df)
        return df
