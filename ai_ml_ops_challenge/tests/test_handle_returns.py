from __future__ import annotations

import pytest

from source.domain.handle_returns import handle_returns
from tests.conftest import StaticAsyncChain


@pytest.mark.asyncio
async def test_handle_returns_starts_with_order_step(base_state):
    state = dict(base_state)
    state["user_id"] = "user_006"
    state["question"] = "Quiero devolver un producto"
    state["user_data"] = {
        "primer_nombre": "Camila",
        "orders": [
            {
                "order_id": "ORD-2025-078",
                "product_name": "Kit de skincare",
                "status": "DELIVERED",
                "delivery_date": "2025-03-01",
                "return_eligible": True,
            }
        ],
        "delivery_address_city": "Cartagena",
        "email": "camila@example.com",
        "phone": "3000000000",
    }

    result = await handle_returns(state)

    assert result["selected_agent"] == "handle_returns"
    assert result["current_step"] == "returns_step_1_collect_order"


@pytest.mark.asyncio
async def test_handle_returns_moves_to_reason_step_with_order_id(monkeypatch, base_state):
    state = dict(base_state)
    state["user_id"] = "user_006"
    state["question"] = "ORD-2025-078"
    state["user_data"] = {
        "primer_nombre": "Camila",
        "orders": [
            {
                "order_id": "ORD-2025-078",
                "product_name": "Kit de skincare",
                "status": "DELIVERED",
                "delivery_date": "2025-03-01",
                "return_eligible": True,
            }
        ],
        "delivery_address_city": "Cartagena",
        "email": "camila@example.com",
        "phone": "3000000000",
    }

    payload = {"respuesta_final": "Tu pedido es elegible. Dime el motivo (1-5)."}
    monkeypatch.setattr(
        "source.domain.handle_returns.get_returns_chain",
        lambda: StaticAsyncChain(payload),
    )

    result = await handle_returns(state)

    assert result["current_step"] == "returns_step_1_collect_reason"
    assert result["is_return_in_progress"] is True


@pytest.mark.asyncio
async def test_handle_returns_chain_error_keeps_continuity(monkeypatch, base_state):
    state = dict(base_state)
    state["user_id"] = "user_006"
    state["question"] = "Quiero devolver un producto"
    state["user_data"] = {
        "primer_nombre": "Camila",
        "orders": [
            {
                "order_id": "ORD-2025-078",
                "product_name": "Kit de skincare",
                "status": "DELIVERED",
                "delivery_date": "2025-03-01",
                "return_eligible": True,
            }
        ],
        "delivery_address_city": "Cartagena",
        "email": "camila@example.com",
        "phone": "3000000000",
    }

    def _raise_chain():
        raise RuntimeError("forced returns failure")

    monkeypatch.setattr("source.domain.handle_returns.get_returns_chain", _raise_chain)

    result = await handle_returns(state)

    assert result["selected_topic"] == "DEVOLUCIONES"
    assert result["selected_agent"] == "handle_returns"
    assert result["current_step"] == "returns_step_1_collect_order"
    assert result["is_return_in_progress"] is True
