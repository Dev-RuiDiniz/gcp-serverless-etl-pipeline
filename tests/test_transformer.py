import pandas as pd
from src.etl.transformer import Transformer


def test_transformer_to_dataframe():
    raw = [{"id": 1, "nome": "A"}]
    transformer = Transformer()

    df = transformer.to_dataframe(raw)

    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, "id"] == 1


def test_clean_columns():
    df = pd.DataFrame({"Nome Completo": ["Rui"], "ID-Estado": [1]})
    transformer = Transformer()

    df2 = transformer.clean_columns(df)

    assert "nome_completo" in df2.columns
    assert "id_estado" in df2.columns
