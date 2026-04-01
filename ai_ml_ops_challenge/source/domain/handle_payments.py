"""Specialized domain node for payments and installments requests."""

from typing import Any, Dict, Optional
import re

from source.application.state import GraphState
from source.adapters.chains.payments_chain import get_payments_chain
from source.adapters.utils.data_filter import filter_user_data
from source.adapters.utils.guardrails import has_auth_secret, has_sensitive_payment_data
from source.adapters.utils.knowledge_base import SCENARIO_KNOWLEDGE_BASE
from source.adapters.utils.mock_data import INSTALLMENT_PLANS
from source.adapters.utils.response_format import apply_response_quality
from source.adapters.utils.safe_chain import get_result_text, log_node_error


def _extract_amount_and_months(question: str) -> Dict[str, Optional[int]]:
    """Extract amount and installment months from user text when possible."""
    lowered = (question or "").lower().replace(".", "")

    amount = None
    months = None

    mil_match = re.search(r"(\d{2,6})\s*mil", lowered)
    if mil_match:
        amount = int(mil_match.group(1)) * 1000
    else:
        amount_match = re.search(r"\b(\d{4,9})\b", lowered)
        if amount_match:
            amount = int(amount_match.group(1))

    months_match = re.search(r"\b(1|3|6|12|24)\s*cuotas?\b", lowered)
    if months_match:
        months = int(months_match.group(1))

    return {"amount": amount, "months": months}


def _build_payment_context(question: str) -> Dict[str, Any]:
    """Create deterministic payment context with optional installment simulation."""
    parsed = _extract_amount_and_months(question)
    amount = parsed["amount"]
    months = parsed["months"]

    context: Dict[str, Any] = {
        "installment_rules": {
            "min_amount_for_installments": 50000,
            "plans": INSTALLMENT_PLANS,
            "months_24_min_amount": 500000,
            "model": "flat_rate",
            "formula": "cuota_mensual = (monto / cuotas) + (monto * tasa_mensual)",
        },
        "parsed_question": parsed,
        "simulation": None,
    }

    if amount and months in INSTALLMENT_PLANS:
        rate_pct = INSTALLMENT_PLANS[months]["monthly_rate"]
        rate = rate_pct / 100
        monthly_payment = (amount / months) + (amount * rate)
        total_payment = monthly_payment * months
        total_interest = total_payment - amount

        context["simulation"] = {
            "amount": amount,
            "months": months,
            "monthly_rate_pct": rate_pct,
            "monthly_payment": round(monthly_payment),
            "total_payment": round(total_payment),
            "total_interest": round(total_interest),
        }

    return context


def _summarize_outstanding_orders(filtered_data: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize outstanding payment obligations from user orders."""
    orders = filtered_data.get("orders", []) if isinstance(filtered_data, dict) else []
    summary = {
        "total_outstanding_balance": 0,
        "orders_with_balance": [],
    }

    if not isinstance(orders, list):
        return summary

    total = 0
    for order in orders:
        if not isinstance(order, dict):
            continue
        outstanding = int(order.get("outstanding_balance", 0) or 0)
        if outstanding <= 0:
            continue

        total += outstanding
        summary["orders_with_balance"].append({
            "order_id": order.get("order_id"),
            "product_name": order.get("product_name"),
            "outstanding_balance": outstanding,
            "monthly_payment": order.get("monthly_payment"),
            "payments_remaining": order.get("payments_remaining"),
            "payment_due_date": order.get("payment_due_date"),
        })

    summary["total_outstanding_balance"] = total
    return summary


async def handle_payments(state: GraphState) -> Dict[str, Any]:
    """Handle payment, installment, and interest questions with a specialized chain."""
    state["flow"].append("handle_payments")

    topic_name = "PAGOS"
    question = state.get("question", "")

    if has_sensitive_payment_data(question) or has_auth_secret(question):
        quality_text = apply_response_quality(
            text=(
                "Por seguridad, no compartas datos de tarjeta, OTP, claves o contrasenas por chat. "
                "Usa siempre los canales seguros de la app para gestionar pagos."
            ),
            user_data=state.get("user_data") or {},
            topic=topic_name,
            add_follow_up=False,
        )
        return {
            "generation": quality_text,
            "selected_topic": topic_name,
            "selected_agent": "handle_payments",
            "last_topic_selected": topic_name,
        }

    topic_data = SCENARIO_KNOWLEDGE_BASE.get(topic_name, {})
    relevant_fields = topic_data.get("variables", [])
    filtered_data = filter_user_data(state.get("user_data"), relevant_fields)
    payment_context = _build_payment_context(question)
    payment_context["outstanding_summary"] = _summarize_outstanding_orders(filtered_data)

    try:
        chain = get_payments_chain()
        result = await chain.ainvoke({
            "topic_name": topic_name,
            "topic_context": topic_data.get("contexto", ""),
            "topic_instructions": topic_data.get("instrucciones", ""),
            "topic_scenarios": str(topic_data.get("escenarios", [])),
            "user_data": str(filtered_data),
            "payment_context": str(payment_context),
            "messages": state.get("messages", []),
            "question": question,
        })
        raw_response = get_result_text(
            result,
            "respuesta_final",
            "Puedo ayudarte con metodos de pago y simulacion de cuotas si me compartes monto y numero de cuotas.",
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
            "selected_agent": "handle_payments",
            "last_topic_selected": topic_name,
        }

    except Exception as e:
        log_node_error(
            "handle_payments",
            e,
            extra={"topic": topic_name, "question": question},
        )
        return {
            "generation": (
                "Disculpa, tuve un problema al revisar tu informacion de pagos. "
                "Por favor intenta de nuevo en unos minutos."
            ),
            "selected_topic": topic_name,
            "selected_agent": "handle_payments",
            "last_topic_selected": topic_name,
        }
