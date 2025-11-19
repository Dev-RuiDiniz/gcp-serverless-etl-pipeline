class ExtractError(Exception):
    """Failed extraction"""
    pass


class TransformError(Exception):
    """Failed transform"""
    pass


class LoadError(Exception):
    """Failed load"""
    pass


class ConfigError(Exception):
    """Configuration missing or invalid"""
    pass
