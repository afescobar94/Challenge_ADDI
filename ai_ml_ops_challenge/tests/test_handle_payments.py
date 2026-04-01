from __future__ import annotations

import pytest

from source.domain.handle_payments import handle_payments
from tests.conftest import StaticAsyncChain


@pytest.mark.asyncio
async def test_handle_payments_blocks_sensitive_data(base_state):
    state = dict(base_state)
    state["question"] = "Mi numero de tarjeta es 4111 1111 1111 1111"
    state["user_data"] = {"primer_nombre": "Carlos"}

    result = await handle_payments(state)

    assert result["selected_topic"] == "PAGOS"
    assert "seguridad" in result["generation"].lower()


@pytest.mark.asyncio
async def test_handle_payments_uses_chain(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Cuanto pagaria a 6 cuotas por 600000?"
    state["user_data"] = {
        "primer_nombre": "Carlos",
        "orders": [],
        "account_status": "ACTIVE",
        "email": "c@example.com",
        "phone": "3000000000",
    }

    payload = {"respuesta_final": "Para 6 cuotas, el pago mensual estimado es 109.000 COP."}
    monkeypatch.setattr(
        "source.domain.handle_payments.get_payments_chain",
        lambda: StaticAsyncChain(payload),
    )

    result = await handle_payments(state)

    assert result["selected_agent"] == "handle_payments"
    assert result["generation"]


@pytest.mark.asyncio
async def test_handle_payments_chain_error_fallback(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Necesito revisar cuotas"
    state["user_data"] = {
        "primer_nombre": "Carlos",
        "orders": [],
        "account_status": "ACTIVE",
        "email": "c@example.com",
        "phone": "3000000000",
    }

    def _raise_chain():
        raise RuntimeError("forced payments failure")

    monkeypatch.setattr("source.domain.handle_payments.get_payments_chain", _raise_chain)

    result = await handle_payments(state)

    assert result["selected_topic"] == "PAGOS"
    assert "problema" in result["generation"].lower()
