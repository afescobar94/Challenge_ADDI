from __future__ import annotations

from typing import Any, Dict

import pytest


@pytest.fixture
def base_state() -> Dict[str, Any]:
    """Reusable baseline GraphState-like payload for unit tests."""
    return {
        "user_id": "user_001",
        "conversation_id": "test-conv",
        "question": "",
        "messages": [],
        "generation": "",
        "flow": [],
        "user_data": None,
        "user_data_summary": None,
        "selected_topic": None,
        "selected_agent": None,
        "router_reasoning": None,
        "current_step": None,
        "is_return_in_progress": False,
        "last_topic_selected": None,
        "set_previous_selected_topics": [],
    }


class StaticAsyncChain:
    """Simple async chain stub that returns a predefined payload."""

    def __init__(self, payload: Any):
        self.payload = payload

    async def ainvoke(self, _: Dict[str, Any]) -> Any:
        return self.payload
