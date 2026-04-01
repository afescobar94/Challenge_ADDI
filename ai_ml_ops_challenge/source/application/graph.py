"""
LangGraph workflow for the Emporyum Tech assistant.

Current flow:
fetch_user_data -> route_topic -> selected_agent -> END

This module exports `workflow` as a StateGraph instance (NOT compiled).
The inline.py entry point compiles it with a checkpointer.
"""

from langgraph.graph import StateGraph, END

from source.application.state import GraphState
from source.domain.fetch_user_data import fetch_user_data
from source.domain.route_topic import route_topic
from source.domain.handle_general import handle_general

# Build graph
workflow = StateGraph(GraphState)

workflow.add_node("fetch_user_data", fetch_user_data)
workflow.add_node("route_topic", route_topic)
workflow.add_node("handle_general", handle_general)


def _route_to_agent(state: GraphState) -> str:
    """Return the next node from router output with a safe fallback."""
    selected_agent = state.get("selected_agent")
    if selected_agent == "handle_general":
        return "handle_general"
    return "handle_general"


workflow.set_entry_point("fetch_user_data")
workflow.add_edge("fetch_user_data", "route_topic")
workflow.add_conditional_edges(
    "route_topic",
    _route_to_agent,
    {
        "handle_general": "handle_general",
    },
)
workflow.add_edge("handle_general", END)
