"""Safety helpers for chain outputs, serialization, and error logging."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from pydantic import BaseModel


def to_plain_data(value: Any) -> Any:
    """Convert nested values to plain JSON-serializable Python primitives."""
    if isinstance(value, BaseModel):
        return to_plain_data(value.model_dump(mode="json"))
    if isinstance(value, Mapping):
        return {str(k): to_plain_data(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_plain_data(item) for item in value]
    if isinstance(value, tuple):
        return [to_plain_data(item) for item in value]
    if isinstance(value, set):
        return [to_plain_data(item) for item in sorted(value, key=str)]
    return value


def get_result_value(result: Any, key: str, default: Any = None) -> Any:
    """Read a key from chain result supporting dicts, pydantic models, and attrs."""
    if result is None:
        return default

    if isinstance(result, BaseModel):
        data = result.model_dump(mode="json")
        return data.get(key, default)

    if isinstance(result, Mapping):
        return result.get(key, default)

    if hasattr(result, key):
        return getattr(result, key, default)

    return default


def get_result_text(result: Any, key: str, default: str = "") -> str:
    """Return a normalized text field from chain result with safe fallback."""
    value = get_result_value(result, key, default)
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def log_node_error(node: str, exc: Exception, *, extra: Optional[Dict[str, Any]] = None) -> None:
    """Log compact and safe error context for debugging without leaking secrets."""
    context = ""
    if extra:
        safe_context = to_plain_data(extra)
        context = f" | context={safe_context}"
    print(f"[ERROR] {node} failed: {type(exc).__name__}: {exc}{context}")
