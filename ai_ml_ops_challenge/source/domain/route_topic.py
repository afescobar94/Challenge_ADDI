"""Topic routing node for the assistant graph.

This node classifies the user request into a KB topic and chooses
which agent should handle the request. It also stores routing trace data
in state for observability and downstream routing decisions.
"""

from typing import Any, Dict, List

from source.application.state import GraphState
from source.adapters.chains.router_chain import get_router_chain
from source.adapters.utils.knowledge_base import SCENARIO_KNOWLEDGE_BASE, VALID_TOPICS
from source.adapters.utils.guardrails import (
    has_auth_secret,
    has_sensitive_payment_data,
    is_competitor_comparison,
    is_obviously_out_of_scope,
)


def _safe_previous_topics(raw_topics: Any) -> List[str]:
    """Normalize previous topics into a list of unique strings preserving order."""
    if not isinstance(raw_topics, list):
        return []

    normalized: List[str] = []
    for topic in raw_topics:
        if isinstance(topic, str) and topic and topic not in normalized:
            normalized.append(topic)
    return normalized


def _keyword_topic_override(question: str) -> str:
    """Return a high-priority topic override for safety-critical intents."""
    lowered = (question or "").lower()

    payments_terms = [
        "tarjeta", "cuotas", "pago", "pagos", "debo", "saldo",
        "interes", "intereses", "efecty", "pse", "a la mano",
    ]
    if any(term in lowered for term in payments_terms):
        return "PAGOS"

    platform_terms = [
        "iniciar sesion", "login", "contrasena", "contraseña", "2fa",
        "cuenta bloqueada", "notificaciones", "app", "otp", "phishing",
        "correo", "telefono", "teléfono",
    ]
    if any(term in lowered for term in platform_terms):
        return "CUENTA"

    returns_terms = [
        "devolucion", "devolución", "devolver", "reembolso", "cambio de producto",
        "quiero devolver", "producto danado", "producto dañado",
    ]
    if any(term in lowered for term in returns_terms):
        return "DEVOLUCIONES"

    operations_purchase_terms = [
        "como comprar", "cómo comprar", "hacer una compra", "checkout",
        "carrito", "confirmar compra", "pasos para comprar",
    ]
    if any(term in lowered for term in operations_purchase_terms):
        return "COMO_COMPRAR"

    operations_order_terms = [
        "pedido", "envio", "envío", "entrega", "seguimiento", "rastreo",
        "donde esta mi pedido", "dónde está mi pedido", "cancelar pedido",
    ]
    if any(term in lowered for term in operations_order_terms):
        return "PEDIDOS"

    return ""


def _returns_from_conversation_context(state: GraphState) -> bool:
    """Infer returns continuity from short replies and recent assistant prompts."""
    question = str(state.get("question", "")).strip().lower()
    if question not in {"si", "sí", "ok", "dale", "1", "2", "3", "4", "5"}:
        return False

    for message in reversed(state.get("messages", []) or []):
        if str(message.get("role", "")).lower() != "assistant":
            continue
        content = str(message.get("content", "")).lower()
        if (
            "motivo de la devolucion" in content
            or "motivo de la devolución" in content
            or "numero de pedido" in content
            or "número de pedido" in content
            or "devolucion" in content
            or "devolución" in content
        ):
            return True
        break

    return False


def _guardrail_topic_override(question: str) -> str:
    """Return an early topic override for security and policy guardrails."""
    if has_sensitive_payment_data(question):
        return "PAGOS"
    if has_auth_secret(question):
        return "CUENTA"
    if is_competitor_comparison(question):
        return "PRODUCTOS"
    if is_obviously_out_of_scope(question):
        return "FUERA_DE_ALCANCE"
    return ""


async def route_topic(state: GraphState) -> Dict[str, Any]:
    """Route the current question to a topic and agent.

    Returns updates for topic/agent selection and context tracking fields.
    """
    state["flow"].append("route_topic")

    topic_agent_map = {
        topic: data.get("responsible_agent", "handle_general")
        for topic, data in SCENARIO_KNOWLEDGE_BASE.items()
    }

    last_topic = state.get("last_topic_selected")
    previous_topics = _safe_previous_topics(state.get("set_previous_selected_topics"))

    fallback_topic = "FUERA_DE_ALCANCE"
    fallback_agent = topic_agent_map.get(fallback_topic, "handle_general")

    question = state.get("question", "")
    if state.get("is_return_in_progress"):
        override_topic = "DEVOLUCIONES"
    elif _returns_from_conversation_context(state):
        override_topic = "DEVOLUCIONES"
    else:
        override_topic = _guardrail_topic_override(question) or _keyword_topic_override(question)
    if override_topic and override_topic in VALID_TOPICS:
        selected_topic = override_topic
        selected_agent = topic_agent_map.get(selected_topic, "handle_general")
        router_reasoning = "Guardrail/keyword override applied for policy-safe routing."
    else:
        try:
            chain = get_router_chain()
            result = await chain.ainvoke({
                "allowed_topics": VALID_TOPICS,
                "topic_agent_map": topic_agent_map,
                "user_data_summary": str(state.get("user_data_summary") or {}),
                "last_topic_selected": last_topic,
                "previous_topics": previous_topics,
                "messages": state.get("messages", []),
                "question": question,
            })

            selected_topic = result.selected_topic if result.selected_topic in VALID_TOPICS else fallback_topic
            selected_agent = result.selected_agent or topic_agent_map.get(selected_topic, "handle_general")
            router_reasoning = result.router_reasoning

        except Exception as e:
            print(f"[ERROR] route_topic failed: {e}")
            selected_topic = fallback_topic
            selected_agent = fallback_agent
            router_reasoning = "Router fallback due to processing error."

    # Force consistency with KB mapping when model output drifts.
    kb_agent = SCENARIO_KNOWLEDGE_BASE.get(selected_topic, {}).get("responsible_agent", "handle_general")
    if selected_agent != kb_agent:
        selected_agent = kb_agent

    updated_topics = previous_topics.copy()
    if selected_topic and selected_topic not in updated_topics:
        updated_topics.append(selected_topic)

    return {
        "selected_topic": selected_topic,
        "selected_agent": selected_agent,
        "router_reasoning": router_reasoning,
        "last_topic_selected": selected_topic,
        "set_previous_selected_topics": updated_topics,
    }
