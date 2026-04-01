"""Specialized domain node for operations and order-management requests."""

from typing import Any, Dict, List

from source.application.state import GraphState
from source.adapters.chains.operations_chain import get_operations_chain
from source.adapters.utils.data_filter import filter_user_data
from source.adapters.utils.knowledge_base import SCENARIO_KNOWLEDGE_BASE
from source.adapters.utils.response_format import apply_response_quality
from source.adapters.utils.safe_chain import get_result_text, log_node_error


DELIVERY_TIMES_BY_CITY = {
    "bogota": 3,
    "medellin": 5,
    "cali": 5,
    "barranquilla": 5,
    "cartagena": 7,
    "bucaramanga": 7,
    "pereira": 7,
}


def _resolve_operations_topic(selected_topic: str) -> str:
    """Return a supported operations topic with a safe fallback."""
    if selected_topic in {"PEDIDOS", "COMO_COMPRAR"}:
        return selected_topic
    return "PEDIDOS"


def _order_status_snapshot(orders: List[Dict[str, Any]]) -> Dict[str, int]:
    """Build a compact status-count summary from user orders."""
    counts: Dict[str, int] = {}
    for order in orders:
        status = str(order.get("status", "UNKNOWN"))
        counts[status] = counts.get(status, 0) + 1
    return counts


def _build_operations_context(filtered_data: Dict[str, Any]) -> Dict[str, Any]:
    """Build deterministic operations context for the chain prompt."""
    city = str(filtered_data.get("delivery_address_city", "")).lower()
    orders = filtered_data.get("orders", []) if isinstance(filtered_data.get("orders", []), list) else []

    return {
        "city": city,
        "estimated_business_days": DELIVERY_TIMES_BY_CITY.get(city, 10),
        "order_status_snapshot": _order_status_snapshot(orders),
        "has_orders": len(orders) > 0,
    }


async def handle_operations(state: GraphState) -> Dict[str, Any]:
    """Handle operations requests using a specialized chain."""
    state["flow"].append("handle_operations")

    topic_name = _resolve_operations_topic(state.get("selected_topic") or "PEDIDOS")
    topic_data = SCENARIO_KNOWLEDGE_BASE.get(topic_name, {})
    relevant_fields = topic_data.get("variables", [])

    filtered_data = filter_user_data(state.get("user_data"), relevant_fields)
    operations_context = _build_operations_context(filtered_data)

    try:
        chain = get_operations_chain()
        result = await chain.ainvoke({
            "topic_name": topic_name,
            "topic_context": topic_data.get("contexto", ""),
            "topic_instructions": topic_data.get("instrucciones", ""),
            "topic_scenarios": str(topic_data.get("escenarios", [])),
            "user_data": str(filtered_data),
            "operations_context": str(operations_context),
            "messages": state.get("messages", []),
            "question": state.get("question", ""),
        })
        raw_response = get_result_text(
            result,
            "respuesta_final",
            "Puedo ayudarte a revisar el estado de tu pedido o el flujo de compra paso a paso.",
        )

        quality_text = apply_response_quality(
            text=raw_response,
            user_data=filtered_data,
            topic=topic_name,
            add_follow_up=True,
        )

        return {
            "generation": quality_text,
            "selected_topic": topic_name,
            "selected_agent": "handle_operations",
            "last_topic_selected": topic_name,
        }

    except Exception as e:
        log_node_error(
            "handle_operations",
            e,
            extra={"topic": topic_name, "question": state.get("question", "")},
        )
        return {
            "generation": (
                "Disculpa, tuve un problema revisando tu solicitud operativa. "
                "Por favor intenta de nuevo en unos minutos."
            ),
            "selected_topic": topic_name,
            "selected_agent": "handle_operations",
            "last_topic_selected": topic_name,
        }
