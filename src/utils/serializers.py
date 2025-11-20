from typing import Any, Dict, Optional
from datetime import datetime

from src.utils.validators import (
    validate_string,
    validate_int,
    validate_float,
    validate_dict,
)


def serialize_region(region: Any) -> Optional[Dict[str, Any]]:
    """
    Serializes nested region object (IBGE example).
    Ensures keys exist and are validated.
    """
    reg = validate_dict(region)
    if not reg:
        return None

    return {
        "id": validate_int(reg.get("id")),
        "nome": validate_string(reg.get("nome")),
        "sigla": validate_string(reg.get("sigla")),
    }


def to_iso_datetime(value: Any) -> Optional[str]:
    """
    Converts any datetime-compatible value to ISO YYYY-MM-DD HH:MM:SS.
    """
    if isinstance(value, datetime):
        return value.isoformat()

    try:
        parsed = datetime.fromisoformat(str(value))
        return parsed.isoformat()
    except Exception:
        return None


def safe_serialize_value(value: Any) -> Any:
    """
    Generic serializer used before DataFrame creation.
    Handles dicts, floats, ints, strings.
    """
    if isinstance(value, dict):
        return {k: safe_serialize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [safe_serialize_value(v) for v in value]
    if isinstance(value, (int, float, str)):
        return value
    return str(value)
