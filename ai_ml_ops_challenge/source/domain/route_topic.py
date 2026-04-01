"""Topic routing node for the assistant graph.

This node classifies the user request into a KB topic and chooses
which agent should handle the request. It also stores routing trace data
in state for observability and downstream routing decisions.
"""

from typing import Any, Dict, List

from source.application.state import GraphState
from source.adapters.chains.router_chain import get_router_chain
from source.adapters.utils.knowledge_base import SCENARIO_KNOWLEDGE_BASE, VALID_TOPICS


def _safe_previous_topics(raw_topics: Any) -> List[str]:
    """Normalize previous topics into a list of unique strings preserving order."""
    if not isinstance(raw_topics, list):
        return []

    normalized: List[str] = []
    for topic in raw_topics:
        if isinstance(topic, str) and topic and topic not in normalized:
            normalized.append(topic)
    return normalized


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

    try:
        chain = get_router_chain()
        result = await chain.ainvoke({
            "allowed_topics": VALID_TOPICS,
            "topic_agent_map": topic_agent_map,
            "user_data_summary": str(state.get("user_data_summary") or {}),
            "last_topic_selected": last_topic,
            "previous_topics": previous_topics,
            "messages": state.get("messages", []),
            "question": state.get("question", ""),
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
