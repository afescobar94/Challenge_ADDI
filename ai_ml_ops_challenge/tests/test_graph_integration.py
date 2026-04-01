from __future__ import annotations

import pytest

from langgraph.checkpoint.memory import MemorySaver

from source.application.graph import workflow


class DynamicRouterChain:
    async def ainvoke(self, payload):
        question = str(payload.get("question", "")).lower()
        messages = payload.get("messages", []) or []
        recent_assistant = ""
        for message in reversed(messages):
            if str(message.get("role", "")).lower() == "assistant":
                recent_assistant = str(message.get("content", "")).lower()
                break

        if "promocion" in question or "promociones" in question:
            return {
                "selected_topic": "PRODUCTOS",
                "selected_agent": "handle_products",
                "router_reasoning": "Promotions intent.",
            }
        if "ord-" in question:
            return {
                "selected_topic": "DEVOLUCIONES",
                "selected_agent": "handle_returns",
                "router_reasoning": "Order id for returns flow.",
            }
        if question.strip() in {"1", "2", "3", "4", "5"} and "devol" in recent_assistant:
            return {
                "selected_topic": "DEVOLUCIONES",
                "selected_agent": "handle_returns",
                "router_reasoning": "Returns reason continuation.",
            }
        if "hola" in question:
            return {
                "selected_topic": "SALUDO",
                "selected_agent": "handle_general",
                "router_reasoning": "Greeting intent.",
            }
        if "comprar" in question:
            return {
                "selected_topic": "COMO_COMPRAR",
                "selected_agent": "handle_operations",
                "router_reasoning": "Purchase flow intent.",
            }
        return {
            "selected_topic": "FUERA_DE_ALCANCE",
            "selected_agent": "handle_general",
            "router_reasoning": "Out of scope.",
        }


class EchoChain:
    def __init__(self, text: str):
        self.text = text

    async def ainvoke(self, _):
        return {"respuesta_final": self.text}


@pytest.mark.asyncio
async def test_graph_end_to_end_routes_across_domains(monkeypatch, base_state):
    monkeypatch.setattr("source.domain.route_topic.get_router_chain", lambda: DynamicRouterChain())
    monkeypatch.setattr("source.domain.handle_general.get_general_chain", lambda: EchoChain("Hola, te ayudo."))
    monkeypatch.setattr("source.domain.handle_products.get_products_chain", lambda: EchoChain("Opciones de productos."))
    monkeypatch.setattr("source.domain.handle_payments.get_payments_chain", lambda: EchoChain("Detalle de pagos."))
    monkeypatch.setattr("source.domain.handle_operations.get_operations_chain", lambda: EchoChain("Detalle de pedidos."))
    monkeypatch.setattr("source.domain.handle_platform.get_platform_chain", lambda: EchoChain("Detalle de cuenta."))
    monkeypatch.setattr("source.domain.handle_returns.get_returns_chain", lambda: EchoChain("Seguimos devolucion."))

    graph = workflow.compile(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "graph-integration-1"}}

    history = []
    prompts = [
        "Hola",
        "Que promociones hay?",
        "Cuanto debo de cuotas?",
        "No puedo iniciar sesion y mi OTP es 123456",
        "Quiero devolver un producto",
        "ORD-2025-078",
        "2",
        "Que hora es?",
    ]
    expected_topics = [
        "SALUDO",
        "PRODUCTOS",
        "PAGOS",
        "CUENTA",
        "DEVOLUCIONES",
        "DEVOLUCIONES",
        "DEVOLUCIONES",
        "FUERA_DE_ALCANCE",
    ]

    for i, prompt in enumerate(prompts):
        state = dict(base_state)
        state["user_id"] = "user_006"
        state["conversation_id"] = "graph-integration-1"
        state["question"] = prompt
        state["messages"] = history

        out = await graph.ainvoke(state, config=config)

        assert out["selected_topic"] == expected_topics[i]
        assert out["selected_agent"]
        assert out["generation"]

        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": out.get("generation", "")})


@pytest.mark.asyncio
async def test_graph_operations_and_returns_state_continuity(monkeypatch, base_state):
    monkeypatch.setattr("source.domain.route_topic.get_router_chain", lambda: DynamicRouterChain())
    monkeypatch.setattr("source.domain.handle_general.get_general_chain", lambda: EchoChain("General ok."))
    monkeypatch.setattr("source.domain.handle_operations.get_operations_chain", lambda: EchoChain("Operacion ok."))
    monkeypatch.setattr("source.domain.handle_returns.get_returns_chain", lambda: EchoChain("Devolucion ok."))

    graph = workflow.compile(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "graph-integration-2"}}

    # operations
    state_ops = dict(base_state)
    state_ops["question"] = "Como comprar?"
    state_ops["messages"] = []

    out_ops = await graph.ainvoke(state_ops, config=config)
    assert out_ops["selected_topic"] == "COMO_COMPRAR"
    assert out_ops["selected_agent"] == "handle_operations"

    # returns step continuity
    state_r1 = dict(base_state)
    state_r1["user_id"] = "user_006"
    state_r1["question"] = "Quiero devolver un producto"
    state_r1["messages"] = []
    out_r1 = await graph.ainvoke(state_r1, config=config)
    assert out_r1["selected_topic"] == "DEVOLUCIONES"
    assert out_r1["current_step"] == "returns_step_1_collect_order"

    state_r2 = dict(base_state)
    state_r2["user_id"] = "user_006"
    state_r2["question"] = "ORD-2025-078"
    state_r2["messages"] = [
        {"role": "user", "content": "Quiero devolver un producto"},
        {"role": "assistant", "content": out_r1["generation"]},
    ]
    out_r2 = await graph.ainvoke(state_r2, config=config)
    assert out_r2["selected_topic"] == "DEVOLUCIONES"
    assert out_r2["current_step"] == "returns_step_1_collect_reason"
