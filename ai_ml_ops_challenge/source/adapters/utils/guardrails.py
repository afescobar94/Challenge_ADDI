"""Deterministic guardrail utilities used by router and domain handlers."""

from __future__ import annotations

import re


CARD_NUMBER_RE = re.compile(r"\b(?:\d[ -]*?){13,19}\b")


def has_sensitive_payment_data(text: str) -> bool:
    """Return True when user text appears to include card-like payment credentials."""
    lowered = (text or "").lower()

    payment_keywords = [
        "tarjeta", "card number", "numero de tarjeta", "número de tarjeta",
        "cvv", "cvc", "expira", "vencimiento",
    ]
    if any(keyword in lowered for keyword in payment_keywords):
        if CARD_NUMBER_RE.search(text or ""):
            return True

    return bool(CARD_NUMBER_RE.search(text or ""))


def has_auth_secret(text: str) -> bool:
    """Return True when text suggests sharing OTP/password/PIN-like secrets."""
    lowered = (text or "").lower()

    auth_markers = [
        "otp", "codigo de verificacion", "código de verificación", "codigo otp",
        "verification code", "contrasena", "contraseña", "password", "pin",
        "clave", "token de acceso",
    ]

    share_markers = ["mi", "es", "es:", "te doy", "aqui", "aquí"]

    has_auth_marker = any(marker in lowered for marker in auth_markers)
    has_share_marker = any(marker in lowered for marker in share_markers)

    return has_auth_marker and has_share_marker


def is_competitor_comparison(text: str) -> bool:
    """Return True for competitor comparison requests in product context."""
    lowered = (text or "").lower()

    competitor_markers = [
        "mercado libre", "falabella", "amazon", "linio", "alkosto", "exito", "éxito",
    ]
    comparison_markers = [
        "mas barato", "más barato", "mejor que", "comparar", "vs", "versus",
        "precio con", "precio vs", "precio que",
    ]

    return any(c in lowered for c in competitor_markers) and any(m in lowered for m in comparison_markers)


def is_obviously_out_of_scope(text: str) -> bool:
    """Return True for clearly external intents unrelated to Emporyum Tech."""
    lowered = (text or "").lower()

    in_scope_markers = [
        "pedido", "compra", "pago", "cuota", "devolucion", "devolución",
        "producto", "promocion", "promoción", "cuenta", "app", "emporyum",
    ]
    if any(marker in lowered for marker in in_scope_markers):
        return False

    out_scope_markers = [
        "que hora es", "qué hora es", "hora en", "clima", "pronostico", "pronóstico",
        "partido", "futbol", "fútbol", "presidente", "capital de", "bitcoin", "traduce",
    ]

    return any(marker in lowered for marker in out_scope_markers)
