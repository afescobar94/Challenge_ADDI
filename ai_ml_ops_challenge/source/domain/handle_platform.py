"""Specialized domain node for account, app, troubleshooting, and security requests."""

from typing import Any, Dict

from source.application.state import GraphState
from source.adapters.chains.platform_chain import get_platform_chain
from source.adapters.utils.data_filter import filter_user_data
from source.adapters.utils.guardrails import has_auth_secret
from source.adapters.utils.knowledge_base import SCENARIO_KNOWLEDGE_BASE
from source.adapters.utils.response_format import apply_response_quality


def _build_platform_context(filtered_data: Dict[str, Any]) -> Dict[str, Any]:
    """Build deterministic platform context for account and app assistance."""
    return {
        "self_service_actions": [
            "actualizar correo",
            "actualizar telefono",
            "actualizar direccion",
            "cambiar contrasena",
            "configurar notificaciones",
            "activar 2FA",
        ],
        "support_required_actions": [
            "cambiar nombre legal",
            "cambiar cedula",
            "fusion de cuentas",
            "desbloqueo por actividad sospechosa",
        ],
        "security_flags": {
            "email_verified": filtered_data.get("email_verified"),
            "phone_verified": filtered_data.get("phone_verified"),
            "account_status": filtered_data.get("account_status"),
        },
    }


async def handle_platform(state: GraphState) -> Dict[str, Any]:
    """Handle platform and account requests using a specialized chain."""
    state["flow"].append("handle_platform")

    topic_name = "CUENTA"
    question = state.get("question", "")

    if has_auth_secret(question):
        quality_text = apply_response_quality(
            text=(
                "No compartas codigos OTP, contrasenas ni claves por chat. "
                "Emporyum Tech nunca solicita esa informacion por este canal."
            ),
            user_data=state.get("user_data") or {},
            topic=topic_name,
            add_follow_up=False,
        )
        return {
            "generation": quality_text,
            "selected_topic": topic_name,
            "selected_agent": "handle_platform",
            "last_topic_selected": topic_name,
        }

    topic_data = SCENARIO_KNOWLEDGE_BASE.get(topic_name, {})
    relevant_fields = topic_data.get("variables", [])

    filtered_data = filter_user_data(state.get("user_data"), relevant_fields)
    platform_context = _build_platform_context(filtered_data)

    try:
        chain = get_platform_chain()
        result = await chain.ainvoke({
            "topic_name": topic_name,
            "topic_context": topic_data.get("contexto", ""),
            "topic_instructions": topic_data.get("instrucciones", ""),
            "topic_scenarios": str(topic_data.get("escenarios", [])),
            "user_data": str(filtered_data),
            "platform_context": str(platform_context),
            "messages": state.get("messages", []),
            "question": question,
        })

        quality_text = apply_response_quality(
            text=result.respuesta_final,
            user_data=filtered_data,
            topic=topic_name,
            add_follow_up=True,
        )

        return {
            "generation": quality_text,
            "selected_topic": topic_name,
            "selected_agent": "handle_platform",
            "last_topic_selected": topic_name,
        }

    except Exception as e:
        print(f"[ERROR] handle_platform failed: {e}")
        return {
            "generation": (
                "Disculpa, tuve un problema revisando tu solicitud de cuenta o app. "
                "Por favor intenta de nuevo en unos minutos."
            ),
            "selected_topic": topic_name,
            "selected_agent": "handle_platform",
            "last_topic_selected": topic_name,
        }
