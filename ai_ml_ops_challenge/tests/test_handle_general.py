from __future__ import annotations

import pytest

from source.domain.handle_general import handle_general
from tests.conftest import StaticAsyncChain


@pytest.mark.asyncio
async def test_handle_general_returns_invariants(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Hola"
    state["selected_topic"] = "SALUDO"
    state["selected_agent"] = "handle_general"
    state["user_data"] = {"primer_nombre": "Carlos"}

    payload = {"respuesta_final": "Hola Carlos, te ayudo con lo que necesites."}
    monkeypatch.setattr(
        "source.domain.handle_general.get_general_chain",
        lambda: StaticAsyncChain(payload),
    )

    result = await handle_general(state)

    assert result["selected_topic"] == "SALUDO"
    assert result["selected_agent"] == "handle_general"
    assert result["generation"]


@pytest.mark.asyncio
async def test_handle_general_fallback_on_chain_error(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Ayuda"
    state["selected_topic"] = "FUERA_DE_ALCANCE"
    state["selected_agent"] = "handle_general"
    state["user_data"] = {"primer_nombre": "Carlos"}

    def _raise_chain():
        raise RuntimeError("forced general failure")

    monkeypatch.setattr("source.domain.handle_general.get_general_chain", _raise_chain)

    result = await handle_general(state)

    assert result["selected_topic"] == "FUERA_DE_ALCANCE"
    assert result["selected_agent"] == "handle_general"
    assert "problema" in result["generation"].lower()
