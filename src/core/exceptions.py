class ExtractError(Exception):
    """Erro durante a etapa de extração de dados."""
    pass


class TransformError(Exception):
    """Erro durante a transformação de dados."""
    pass


class LoadError(Exception):
    """Erro durante o carregamento no BigQuery."""
    pass


class ConfigError(Exception):
    """Erro relacionado à configuração do projeto."""
    pass
