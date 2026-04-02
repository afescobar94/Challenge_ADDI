"""
Generic agent node: handles ALL questions using the general chain.

This basic implementation passes the entire Knowledge Base and filtered user data
into a single prompt. There is no topic routing or specialized handling —
every question gets the same treatment regardless of the topic.
"""

from typing import Any, Dict

from source.application.state import GraphState
from source.adapters.utils.knowledge_base import SCENARIO_KNOWLEDGE_BASE
from source.adapters.utils.data_filter import filter_user_data
from source.adapters.chains.general_chain import get_general_chain
from source.adapters.utils.response_format import apply_response_quality
from source.adapters.utils.safe_chain import get_result_text, log_node_error


# Fields the generic agent uses — a specialized agent would use fewer, topic-relevant fields.
GENERAL_RELEVANT_FIELDS = [
    "delivery_address_city",
    "purchase_history",
    "user_category_preferences",
    "available_promotions",
]


async def handle_general(state: GraphState) -> Dict[str, Any]:
    """Handle any question by passing the entire KB and filtered user data to the LLM."""
    state["flow"].append("handle_general")

    knowledge_base = str(SCENARIO_KNOWLEDGE_BASE)
    filtered_data = filter_user_data(state.get("user_data"), GENERAL_RELEVANT_FIELDS)

    selected_topic = state.get("selected_topic") or "FUERA_DE_ALCANCE"
    selected_agent = state.get("selected_agent") or "handle_general"

    try:
        chain = get_general_chain()
        result = await chain.ainvoke({
            "knowledge_base": knowledge_base,
            "user_data": str(filtered_data),
            "messages": state.get("messages", []),
            "question": state["question"],
        })

        raw_response = get_result_text(
            result,
            "respuesta_final",
            (
                "Solo puedo ayudarte con temas de Emporyum Tech, como pedidos, pagos, "
                "productos, cuenta o devoluciones."
            ),
        )
        quality_text = apply_response_quality(
            text=raw_response,
            user_data=filtered_data,
            topic=selected_topic,
            add_follow_up=selected_topic != "FUERA_DE_ALCANCE",
        )
        return {
            "generation": quality_text,
            "selected_topic": selected_topic,
            "selected_agent": selected_agent,
            "last_topic_selected": selected_topic,
        }

    except Exception as e:
        log_node_error(
            "handle_general",
            e,
            extra={"selected_topic": selected_topic, "selected_agent": selected_agent},
        )
        return {
            "generation": (
                "Disculpa, tuve un problema procesando tu solicitud. "
                "Por favor intenta de nuevo o contacta a nuestro equipo de soporte."
            ),
            "selected_topic": selected_topic,
            "selected_agent": selected_agent,
            "last_topic_selected": selected_topic,
        }
