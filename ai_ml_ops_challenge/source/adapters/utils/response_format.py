"""Shared response formatting helpers for quality and personalization."""

from __future__ import annotations

import re
from typing import Any, Dict, Optional


AMOUNT_RE = re.compile(r"(\$?\s*)(\d{1,3}(?:[.,]\d{3})+|\d{5,9})(\s*COP)?", re.IGNORECASE)


def format_cop(value: Optional[float]) -> str:
    """Format numeric value as standardized COP currency."""
    if value is None:
        return "$0 COP"
    rounded = int(round(float(value)))
    formatted = f"{rounded:,}".replace(",", ".")
    return f"${formatted} COP"


def _to_int(token: str) -> Optional[int]:
    """Convert a numeric token with separators into int."""
    cleaned = token.replace(".", "").replace(",", "")
    if not cleaned.isdigit():
        return None
    return int(cleaned)


def normalize_cop_amounts(text: str) -> str:
    """Normalize currency-like numbers in text to COP format when context suggests money."""
    source = text or ""

    def repl(match: re.Match[str]) -> str:
        prefix, number_token, suffix_cop = match.groups()
        value = _to_int(number_token)
        if value is None:
            return match.group(0)

        left_context = source[max(0, match.start() - 20):match.start()].lower()
        right_context = source[match.end():min(len(source), match.end() + 20)].lower()
        local_context = f"{left_context} {right_context}"

        money_markers = [
            "cop", "saldo", "cuota", "pago", "pagos", "precio", "descuento", "monto", "interes",
        ]

        has_money_signal = (
            "$" in (prefix or "")
            or bool(suffix_cop)
            or any(marker in local_context for marker in money_markers)
            or value >= 50000
        )

        if not has_money_signal:
            return match.group(0)

        return format_cop(value)

    return AMOUNT_RE.sub(repl, source)


def clean_response_style(text: str) -> str:
    """Apply lightweight style cleanup for readability."""
    cleaned = re.sub(r"[ \t]+", " ", text or "").strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def personalize_with_name(text: str, user_data: Dict[str, Any], topic: str) -> str:
    """Optionally prepend user name for a warmer and consistent tone."""
    name = str((user_data or {}).get("primer_nombre") or "").strip()
    if not name:
        return text

    lowered = (text or "").lower()
    if name.lower() in lowered:
        return text

    # Keep out-of-scope concise and avoid forcing name there.
    if topic == "FUERA_DE_ALCANCE":
        return text

    return f"{name}, {text}"


def add_follow_up_if_needed(text: str, topic: str) -> str:
    """Add a concise actionable follow-up when response has no next step."""
    if not text:
        return text

    if "?" in text:
        return text

    follow_up_by_topic = {
        "PRODUCTOS": " ¿Quieres que te muestre mas opciones segun tu presupuesto?",
        "PAGOS": " ¿Quieres que te ayude a simular cuotas para un monto especifico?",
        "PEDIDOS": " ¿Quieres que revisemos el detalle de un pedido especifico?",
        "COMO_COMPRAR": " ¿Quieres que te guie con el siguiente paso en tu compra?",
        "CUENTA": " ¿Quieres que te indique la ruta exacta dentro de la app?",
        "DEVOLUCIONES": " ¿Quieres que continuemos con el siguiente paso de la devolucion?",
    }

    suffix = follow_up_by_topic.get(topic)
    if not suffix:
        return text

    return text + suffix


def apply_response_quality(
    *,
    text: str,
    user_data: Dict[str, Any],
    topic: str,
    add_follow_up: bool = False,
) -> str:
    """Apply shared response-quality transforms."""
    result = clean_response_style(text)
    result = normalize_cop_amounts(result)
    result = personalize_with_name(result, user_data=user_data, topic=topic)
    if add_follow_up:
        result = add_follow_up_if_needed(result, topic=topic)
    return result
