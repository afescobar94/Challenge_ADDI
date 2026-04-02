from __future__ import annotations

import pytest

from source.domain.route_topic import route_topic
from tests.conftest import StaticAsyncChain


@pytest.mark.asyncio
async def test_route_topic_uses_keyword_override_for_payments(base_state):
    state = dict(base_state)
    state["question"] = "Necesito ayuda con cuotas"
    state["user_data_summary"] = {"primer_nombre": "Carlos"}

    result = await route_topic(state)

    assert result["selected_topic"] == "PAGOS"
    assert result["selected_agent"] == "handle_payments"
    assert result["router_reasoning"]


@pytest.mark.asyncio
async def test_route_topic_chain_failure_falls_back(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Necesito soporte"
    state["user_data_summary"] = {"primer_nombre": "Carlos"}

    def _raise_chain():
        raise RuntimeError("forced router failure")

    monkeypatch.setattr("source.domain.route_topic.get_router_chain", _raise_chain)

    result = await route_topic(state)

    assert result["selected_topic"] == "FUERA_DE_ALCANCE"
    assert result["selected_agent"] == "handle_general"
    assert "fallback" in result["router_reasoning"].lower()


@pytest.mark.asyncio
async def test_route_topic_uses_chain_when_no_override(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Hola, buen dia"
    state["user_data_summary"] = {"primer_nombre": "Carlos"}

    payload = {
        "selected_topic": "SALUDO",
        "selected_agent": "handle_general",
        "router_reasoning": "Greeting intent identified.",
    }
    monkeypatch.setattr(
        "source.domain.route_topic.get_router_chain",
        lambda: StaticAsyncChain(payload),
    )

    result = await route_topic(state)

    assert result["selected_topic"] == "SALUDO"
    assert result["selected_agent"] == "handle_general"
    assert "Greeting" in result["router_reasoning"]
