from __future__ import annotations

import pytest

from source.domain.handle_operations import handle_operations
from tests.conftest import StaticAsyncChain


@pytest.mark.asyncio
async def test_handle_operations_uses_selected_topic(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Donde esta mi pedido?"
    state["selected_topic"] = "PEDIDOS"
    state["user_data"] = {
        "primer_nombre": "Carlos",
        "orders": [],
        "delivery_address_city": "Bogota",
        "email_verified": True,
        "phone_verified": True,
    }

    payload = {"respuesta_final": "Tu pedido esta en transito."}
    monkeypatch.setattr(
        "source.domain.handle_operations.get_operations_chain",
        lambda: StaticAsyncChain(payload),
    )

    result = await handle_operations(state)

    assert result["selected_agent"] == "handle_operations"
    assert result["selected_topic"] == "PEDIDOS"


@pytest.mark.asyncio
async def test_handle_operations_chain_error_fallback(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Como comprar?"
    state["selected_topic"] = "COMO_COMPRAR"
    state["user_data"] = {
        "primer_nombre": "Carlos",
        "orders": [],
        "delivery_address_city": "Bogota",
        "email_verified": True,
        "phone_verified": True,
    }

    def _raise_chain():
        raise RuntimeError("forced operations failure")

    monkeypatch.setattr("source.domain.handle_operations.get_operations_chain", _raise_chain)

    result = await handle_operations(state)

    assert result["selected_topic"] == "COMO_COMPRAR"
    assert "problema" in result["generation"].lower()
