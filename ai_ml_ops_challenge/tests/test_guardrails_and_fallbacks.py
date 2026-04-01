from __future__ import annotations

import pytest

from source.adapters.utils.guardrails import (
    has_auth_secret,
    has_sensitive_payment_data,
    is_competitor_comparison,
    is_obviously_out_of_scope,
)
from source.domain.handle_payments import handle_payments


def test_guardrails_sensitive_payment_data_detected():
    assert has_sensitive_payment_data("Tarjeta 4111 1111 1111 1111") is True


def test_guardrails_auth_secret_detected():
    assert has_auth_secret("Mi OTP es 123456") is True


def test_guardrails_competitor_comparison_detected():
    assert is_competitor_comparison("Amazon vs ustedes, cual es mas barato?") is True


def test_guardrails_out_of_scope_detected():
    assert is_obviously_out_of_scope("Que hora es en Bogota?") is True


@pytest.mark.asyncio
async def test_payments_guardrail_short_circuits_before_chain(base_state, monkeypatch):
    state = dict(base_state)
    state["question"] = "Mi tarjeta es 4111 1111 1111 1111"
    state["user_data"] = {"primer_nombre": "Carlos"}

    called = {"value": False}

    def _chain_should_not_run():
        called["value"] = True
        raise RuntimeError("should not run")

    monkeypatch.setattr("source.domain.handle_payments.get_payments_chain", _chain_should_not_run)

    result = await handle_payments(state)

    assert called["value"] is False
    assert "seguridad" in result["generation"].lower()
