"""Specialized domain node for product and promotions requests."""

from typing import Any, Dict, List, Optional
import re

from source.application.state import GraphState
from source.adapters.chains.products_chain import get_products_chain
from source.adapters.utils.data_filter import filter_user_data
from source.adapters.utils.guardrails import is_competitor_comparison
from source.adapters.utils.knowledge_base import SCENARIO_KNOWLEDGE_BASE
from source.adapters.utils.mock_data import MOCK_CATALOG


def _extract_budget_cop(question: str) -> Optional[int]:
    """Extract an approximate COP budget from a free-text question."""
    lowered = (question or "").lower().replace(".", "")

    mil_match = re.search(r"(\d{2,6})\s*mil", lowered)
    if mil_match:
        return int(mil_match.group(1)) * 1000

    digits = re.findall(r"\d{4,9}", lowered)
    if digits:
        return int(digits[0])

    return None


def _build_catalog_candidates(user_data: Dict[str, Any], question: str, max_items: int = 12) -> List[Dict[str, Any]]:
    """Build a compact list of catalog candidates for recommendation context."""
    budget = _extract_budget_cop(question)
    preferred_categories = set(user_data.get("user_category_preferences", []))

    candidates: List[Dict[str, Any]] = []
    for item in MOCK_CATALOG:
        if not item.get("in_stock", False):
            continue

        if budget is not None and item.get("price", 0) > budget:
            continue

        score = 0
        if item.get("trending"):
            score += 2
        if item.get("category") in preferred_categories:
            score += 2
        if item.get("rating", 0) >= 4.6:
            score += 1

        candidates.append({
            "product_id": item.get("product_id"),
            "name": item.get("name"),
            "category": item.get("category"),
            "subcategory": item.get("subcategory"),
            "price": item.get("price"),
            "rating": item.get("rating"),
            "trending": item.get("trending"),
            "score": score,
        })

    candidates.sort(key=lambda x: (x["score"], x["rating"], -x["price"]), reverse=True)
    return candidates[:max_items]


async def handle_products(state: GraphState) -> Dict[str, Any]:
    """Handle product and promotions questions with a specialized chain."""
    state["flow"].append("handle_products")

    topic_name = "PRODUCTOS"
    topic_data = SCENARIO_KNOWLEDGE_BASE.get(topic_name, {})
    relevant_fields = topic_data.get("variables", [])
    filtered_data = filter_user_data(state.get("user_data"), relevant_fields)
    question = state.get("question", "")
    catalog_candidates = _build_catalog_candidates(filtered_data, question)

    if is_competitor_comparison(question):
        return {
            "generation": (
                "No puedo comparar precios con otros comercios, "
                "pero si quieres te muestro nuestras promociones activas."
            ),
            "selected_topic": topic_name,
            "selected_agent": "handle_products",
            "last_topic_selected": topic_name,
        }

    try:
        chain = get_products_chain()
        result = await chain.ainvoke({
            "topic_name": topic_name,
            "topic_context": topic_data.get("contexto", ""),
            "topic_instructions": topic_data.get("instrucciones", ""),
            "topic_scenarios": str(topic_data.get("escenarios", [])),
            "user_data": str(filtered_data),
            "catalog_candidates": str(catalog_candidates),
            "messages": state.get("messages", []),
            "question": question,
        })

        return {
            "generation": result.respuesta_final,
            "selected_topic": topic_name,
            "selected_agent": "handle_products",
            "last_topic_selected": topic_name,
        }

    except Exception as e:
        print(f"[ERROR] handle_products failed: {e}")
        return {
            "generation": (
                "Disculpa, tuve un problema al revisar productos y promociones. "
                "Por favor intenta de nuevo en unos minutos."
            ),
            "selected_topic": topic_name,
            "selected_agent": "handle_products",
            "last_topic_selected": topic_name,
        }
