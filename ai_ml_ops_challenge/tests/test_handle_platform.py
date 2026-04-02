from __future__ import annotations

import pytest

from source.domain.handle_platform import handle_platform
from tests.conftest import StaticAsyncChain


@pytest.mark.asyncio
async def test_handle_platform_blocks_auth_secret(base_state):
    state = dict(base_state)
    state["question"] = "Mi OTP es 123456"
    state["user_data"] = {"primer_nombre": "Carlos"}

    result = await handle_platform(state)

    assert result["selected_topic"] == "CUENTA"
    assert "otp" in result["generation"].lower()


@pytest.mark.asyncio
async def test_handle_platform_chain_error_fallback(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "No puedo iniciar sesion"
    state["user_data"] = {
        "primer_nombre": "Carlos",
        "email": "c@example.com",
        "phone": "3000000000",
        "email_verified": True,
        "phone_verified": True,
        "account_status": "ACTIVE",
    }

    def _raise_chain():
        raise RuntimeError("forced platform failure")

    monkeypatch.setattr("source.domain.handle_platform.get_platform_chain", _raise_chain)

    result = await handle_platform(state)

    assert result["selected_agent"] == "handle_platform"
    assert "problema" in result["generation"].lower()


@pytest.mark.asyncio
async def test_handle_platform_chain_success(monkeypatch, base_state):
    state = dict(base_state)
    state["question"] = "Como cambio mi correo?"
    state["user_data"] = {
        "primer_nombre": "Carlos",
        "email": "c@example.com",
        "phone": "3000000000",
        "email_verified": True,
        "phone_verified": True,
        "account_status": "ACTIVE",
    }

    payload = {"respuesta_final": "Ve a Mi Perfil para actualizar tu correo y verificarlo."}
    monkeypatch.setattr(
        "source.domain.handle_platform.get_platform_chain",
        lambda: StaticAsyncChain(payload),
    )

    result = await handle_platform(state)

    assert result["selected_topic"] == "CUENTA"
    assert result["generation"]
