from __future__ import annotations

import pytest

from source.domain.handle_products import handle_products
from tests.conftest import StaticAsyncChain


@pytest.mark.asyncio
async def test_handle_products_blocks_competitor_comparison(base_state):
    state = dict(base_state)
    state["question"] = "Amazon es mas barato que ustedes?"
    state["user_data"] = {
        "primer_nombre": "Carlos",
        "purchase_history": [],
        "user_category_preferences": ["Electronics"],
        "available_promotions": [],
        "delivery_address_city": "Bogota",
    }

    result = await handle_products(state)

    assert result["selected_agent"] == "handle_products"
    assert "comparar" in result["generation"].lower()


@pytest.mark.asyncio
async def test_handle_products_uses_chain_response(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Recomiendame algo de tecnologia"
    state["user_data"] = {
        "primer_nombre": "Carlos",
        "purchase_history": [],
        "user_category_preferences": ["Electronics"],
        "available_promotions": [],
        "delivery_address_city": "Bogota",
    }

    payload = {"respuesta_final": "Te recomiendo 3 opciones de celulares en tu presupuesto."}
    monkeypatch.setattr(
        "source.domain.handle_products.get_products_chain",
        lambda: StaticAsyncChain(payload),
    )

    result = await handle_products(state)

    assert result["selected_topic"] == "PRODUCTOS"
    assert result["generation"]


@pytest.mark.asyncio
async def test_handle_products_chain_error_fallback(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Quiero recomendaciones"
    state["user_data"] = {
        "primer_nombre": "Carlos",
        "purchase_history": [],
        "user_category_preferences": ["Electronics"],
        "available_promotions": [],
        "delivery_address_city": "Bogota",
    }

    def _raise_chain():
        raise RuntimeError("forced products failure")

    monkeypatch.setattr("source.domain.handle_products.get_products_chain", _raise_chain)

    result = await handle_products(state)

    assert result["selected_topic"] == "PRODUCTOS"
    assert result["selected_agent"] == "handle_products"
    assert "problema" in result["generation"].lower()
