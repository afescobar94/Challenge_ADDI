"""Specialized domain node for multi-turn returns and refunds workflow."""

from __future__ import annotations

from datetime import date, datetime
import re
from typing import Any, Dict, List, Optional

from source.application.state import GraphState
from source.adapters.chains.returns_chain import get_returns_chain
from source.adapters.utils.data_filter import filter_user_data
from source.adapters.utils.knowledge_base import SCENARIO_KNOWLEDGE_BASE
from source.adapters.utils.response_format import apply_response_quality
from source.adapters.utils.safe_chain import get_result_text, log_node_error


ORDER_ID_PATTERN = re.compile(r"ORD-\d{4}-\d{3}", re.IGNORECASE)

NON_RETURNABLE_KEYWORDS = [
    "ropa interior",
    "audifonos",
    "audífonos",
    "earbuds",
    "personalizado",
    "grabado",
    "perecedero",
    "licencia",
    "digital",
]

ESCALATION_KEYWORDS = [
    "danado",
    "dañado",
    "defectuoso",
    "producto diferente",
    "equivocado",
    "no recibido",
    "no ha llegado",
    "no me llego",
]

REASON_MAP = {
    "1": "El producto llego danado",
    "2": "Recibi un producto diferente al que pedi",
    "3": "El producto no cumple mis expectativas",
    "4": "Ya no lo necesito",
    "5": "Otro motivo",
    "danado": "El producto llego danado",
    "dañado": "El producto llego danado",
    "diferente": "Recibi un producto diferente al que pedi",
    "equivocado": "Recibi un producto diferente al que pedi",
    "expectativas": "El producto no cumple mis expectativas",
    "no necesito": "Ya no lo necesito",
}


def _extract_order_id(text: str) -> Optional[str]:
    """Extract a normalized order ID from free text."""
    if not text:
        return None
    match = ORDER_ID_PATTERN.search(text)
    if not match:
        return None
    return match.group(0).upper()


def _extract_recent_order_id(messages: List[Dict[str, Any]]) -> Optional[str]:
    """Extract the most recent order ID mentioned in conversation history."""
    for message in reversed(messages or []):
        content = str(message.get("content", ""))
        extracted = _extract_order_id(content)
        if extracted:
            return extracted
    return None


def _find_order(orders: List[Dict[str, Any]], order_id: str) -> Optional[Dict[str, Any]]:
    """Find an order by ID in user order list."""
    for order in orders:
        if str(order.get("order_id", "")).upper() == order_id.upper():
            return order
    return None


def _parse_date(raw_date: Optional[str]) -> Optional[date]:
    """Parse ISO date string into date object."""
    if not raw_date:
        return None
    try:
        return datetime.strptime(raw_date, "%Y-%m-%d").date()
    except ValueError:
        return None


def _is_non_returnable(product_name: str) -> bool:
    """Return True when product text matches a non-returnable rule."""
    lowered = (product_name or "").lower()
    return any(keyword in lowered for keyword in NON_RETURNABLE_KEYWORDS)


def _requires_escalation(question: str) -> bool:
    """Return True when user message triggers immediate escalation flow."""
    lowered = (question or "").lower()
    return any(keyword in lowered for keyword in ESCALATION_KEYWORDS)


def _infer_reason(question: str) -> Optional[str]:
    """Infer a return reason label from user message."""
    lowered = (question or "").lower().strip()

    if lowered in REASON_MAP:
        return REASON_MAP[lowered]

    for key, value in REASON_MAP.items():
        if key in lowered:
            return value

    return None


def _infer_step_from_messages(messages: List[Dict[str, Any]]) -> Optional[str]:
    """Infer returns step from recent assistant prompts when state is reset by caller."""
    for message in reversed(messages or []):
        if str(message.get("role", "")).lower() != "assistant":
            continue
        content = str(message.get("content", "")).lower()
        if "motivo de la devolucion" in content or "motivo de la devolución" in content:
            return "returns_step_1_collect_reason"
        if "numero de pedido" in content or "número de pedido" in content:
            return "returns_step_1_collect_order"
    return None


def _build_draft_response(
    *,
    step: str,
    question: str,
    filtered_data: Dict[str, Any],
    order: Optional[Dict[str, Any]],
    reason: Optional[str],
) -> Dict[str, Any]:
    """Build deterministic draft response and state transitions for returns flow."""
    orders = filtered_data.get("orders", []) if isinstance(filtered_data.get("orders", []), list) else []

    if _requires_escalation(question):
        return {
            "draft": (
                "Lamento lo ocurrido. Este caso requiere atencion prioritaria de soporte. "
                "Por favor comparte fotos del producto y del empaque desde el chat de soporte en la app. "
                "Vamos a escalar tu caso con respuesta estimada en 24-48 horas."
            ),
            "next_step": None,
            "in_progress": False,
        }

    if step == "returns_step_1_collect_order":
        if order is None:
            if not orders:
                return {
                    "draft": (
                        "No encuentro pedidos asociados para devolucion en este momento. "
                        "Si tienes un numero de pedido, compartelo y lo revisamos."
                    ),
                    "next_step": None,
                    "in_progress": False,
                }

            recent_ids = ", ".join(str(o.get("order_id")) for o in orders[:3])
            return {
                "draft": (
                    "Claro, te ayudo con la devolucion. Por favor comparteme el numero de pedido (ej. ORD-2025-001). "
                    f"Si te sirve, tus pedidos recientes son: {recent_ids}."
                ),
                "next_step": "returns_step_1_collect_order",
                "in_progress": True,
            }

        status = str(order.get("status", "")).upper()
        delivery_date = _parse_date(order.get("delivery_date"))
        return_eligible_flag = bool(order.get("return_eligible", False))
        product_name = str(order.get("product_name", ""))

        if _is_non_returnable(product_name):
            return {
                "draft": (
                    "Este producto no es elegible para devolucion por politica del tipo de producto. "
                    "Si quieres, te ayudo a revisar otras alternativas de soporte."
                ),
                "next_step": None,
                "in_progress": False,
            }

        if status != "DELIVERED":
            if status in {"CONFIRMED", "PREPARING"}:
                return {
                    "draft": (
                        "Tu pedido aun no ha sido entregado. En este estado te conviene solicitar cancelacion si ya no lo deseas."
                    ),
                    "next_step": None,
                    "in_progress": False,
                }
            return {
                "draft": (
                    "Tu pedido aun no ha sido entregado, por lo que no podemos iniciar devolucion todavia. "
                    "Cuando se entregue, te ayudo de inmediato con el proceso."
                ),
                "next_step": None,
                "in_progress": False,
            }

        days_since_delivery = None
        if delivery_date is not None:
            days_since_delivery = (date.today() - delivery_date).days

        eligible_by_window = days_since_delivery is not None and days_since_delivery <= 15
        if not (return_eligible_flag or eligible_by_window):
            delivered_text = order.get("delivery_date") or "fecha no disponible"
            return {
                "draft": (
                    "Lamentablemente, el plazo de 15 dias calendario para devolucion ya vencio. "
                    f"Tu pedido fue entregado el {delivered_text}."
                ),
                "next_step": None,
                "in_progress": False,
            }

        return {
            "draft": (
                f"Tu pedido {order.get('order_id')} es elegible para devolucion. "
                "Por favor indicanos el motivo de la devolucion:\n"
                "1. El producto llego danado\n"
                "2. Recibi un producto diferente al que pedi\n"
                "3. El producto no cumple mis expectativas\n"
                "4. Ya no lo necesito\n"
                "5. Otro motivo"
            ),
            "next_step": "returns_step_1_collect_reason",
            "in_progress": True,
        }

    if step == "returns_step_1_collect_reason":
        if order is None:
            return {
                "draft": (
                    "Para continuar, necesito confirmar el numero de pedido que deseas devolver."
                ),
                "next_step": "returns_step_1_collect_order",
                "in_progress": True,
            }

        if not reason:
            return {
                "draft": (
                    "Gracias. Para continuar, indicanos el motivo de la devolucion (1, 2, 3, 4 o 5)."
                ),
                "next_step": "returns_step_1_collect_reason",
                "in_progress": True,
            }

        return {
            "draft": (
                f"Hemos registrado tu solicitud de devolucion para el pedido {order.get('order_id')}. Motivo: {reason}. "
                "Programaremos la recoleccion en tu direccion registrada en 3-5 dias habiles. "
                "Una vez recibamos e inspeccionemos el producto, procesaremos el reembolso en 5-10 dias habiles "
                "al mismo metodo de pago de la compra."
            ),
            "next_step": None,
            "in_progress": False,
        }

    return {
        "draft": (
            "Te ayudo con la devolucion. Por favor comparteme el numero de pedido para validar elegibilidad."
        ),
        "next_step": "returns_step_1_collect_order",
        "in_progress": True,
    }


async def handle_returns(state: GraphState) -> Dict[str, Any]:
    """Handle multi-turn returns flow with deterministic validation and state continuity."""
    state["flow"].append("handle_returns")

    topic_name = "DEVOLUCIONES"
    topic_data = SCENARIO_KNOWLEDGE_BASE.get(topic_name, {})

    try:
        filtered_data = filter_user_data(state.get("user_data"), topic_data.get("variables", []))
        question = state.get("question", "")
        messages = state.get("messages", [])
        orders = filtered_data.get("orders", []) if isinstance(filtered_data.get("orders", []), list) else []

        in_progress = bool(state.get("is_return_in_progress", False))
        current_step = state.get("current_step")

        inferred_step = _infer_step_from_messages(messages)
        if not current_step and inferred_step:
            current_step = inferred_step
            in_progress = True

        if not in_progress:
            in_progress = True
        if not current_step:
            current_step = "returns_step_1_collect_order"

        reason = _infer_reason(question)
        explicit_order_id = _extract_order_id(question)
        historical_order_id = _extract_recent_order_id(messages)

        if explicit_order_id:
            order_id = explicit_order_id
        elif current_step == "returns_step_1_collect_reason":
            order_id = historical_order_id
        else:
            order_id = None

        order = _find_order(orders, order_id) if order_id else None

        decision = _build_draft_response(
            step=current_step,
            question=question,
            filtered_data=filtered_data,
            order=order,
            reason=reason,
        )

        next_step = decision["next_step"]
        next_in_progress = decision["in_progress"]
        draft_response = decision["draft"]

        should_bypass_chain = (
            _requires_escalation(question)
            or (current_step == "returns_step_1_collect_reason" and bool(reason))
        )

        if should_bypass_chain:
            final_response = draft_response
        else:
            try:
                chain = get_returns_chain()
                result = await chain.ainvoke({
                    "current_step": current_step,
                    "returns_state": str({
                        "order_id": order_id,
                        "reason": reason,
                        "in_progress": in_progress,
                    }),
                    "draft_response": draft_response,
                    "messages": messages,
                    "question": question,
                })
                final_response = get_result_text(result, "respuesta_final", draft_response)
            except Exception as e:
                log_node_error(
                    "handle_returns.chain",
                    e,
                    extra={"step": current_step, "order_id": order_id, "in_progress": in_progress},
                )
                final_response = draft_response

        return {
            "generation": apply_response_quality(
                text=final_response,
                user_data=filtered_data,
                topic=topic_name,
                add_follow_up=False,
            ),
            "selected_topic": topic_name,
            "selected_agent": "handle_returns",
            "last_topic_selected": topic_name,
            "is_return_in_progress": next_in_progress,
            "current_step": next_step,
        }
    except Exception as e:
        previous_in_progress = bool(state.get("is_return_in_progress", False))
        previous_step = state.get("current_step")
        if previous_in_progress and not previous_step:
            previous_step = "returns_step_1_collect_order"

        log_node_error(
            "handle_returns",
            e,
            extra={"step": previous_step, "in_progress": previous_in_progress},
        )
        return {
            "generation": (
                "Disculpa, tuve un problema al procesar la devolucion. "
                "Podemos continuar desde el ultimo paso si me compartes de nuevo el numero de pedido."
            ),
            "selected_topic": topic_name,
            "selected_agent": "handle_returns",
            "last_topic_selected": topic_name,
            "is_return_in_progress": previous_in_progress,
            "current_step": previous_step,
        }
