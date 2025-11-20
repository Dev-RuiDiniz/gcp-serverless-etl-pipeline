from typing import Any, Optional


def is_empty(value: Any) -> bool:
    """
    Checks if a value is considered empty.
    """
    return value is None or value == "" or (hasattr(value, "__len__") and len(value) == 0)


def validate_string(value: Any) -> Optional[str]:
    """
    Ensures value is a clean string or None.
    """
    if value is None:
        return None
    try:
        return str(value).strip()
    except Exception:
        return None


def validate_int(value: Any) -> Optional[int]:
    """
    Convert to int if possible, return None otherwise.
    """
    try:
        return int(value)
    except Exception:
        return None


def validate_float(value: Any) -> Optional[float]:
    """
    Convert to float if possible, return None otherwise.
    """
    try:
        return float(value)
    except Exception:
        return None


def validate_dict(value: Any) -> Optional[dict]:
    """
    Ensures the value is a dictionary.
    """
    return value if isinstance(value, dict) else None
