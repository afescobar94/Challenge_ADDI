"""Specialized chain for payments, installments, and interest explanations."""

import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()


class PaymentsResponse(BaseModel):
    """Structured output for payment-related responses."""

    reasoning: str = Field(..., description="Brief reasoning for the selected payment response strategy. Max 20 words.")
    respuesta_final: str = Field(..., description="Final response in Colombian Spanish.")


PAYMENTS_SYSTEM_PROMPT = """\
You are Emporyum Tech's specialized payments assistant.

## TOPIC
{topic_name}

## TOPIC CONTEXT
{topic_context}

## TOPIC INSTRUCTIONS
{topic_instructions}

## TOPIC SCENARIOS
{topic_scenarios}

## FILTERED USER DATA
{user_data}

## PAYMENT CALCULATION CONTEXT
{payment_context}

## RULES
- Respond in natural Colombian Spanish.
- Use COP formatting with thousands separators when sharing monetary values.
- Be precise with installment rules and interest constraints.
- If user asks about current debt or pending installments, prioritize balances from user order data.
- If user shares sensitive payment credentials, warn and redirect to secure app channels.
- Keep response concise and actionable (2-6 sentences).
"""

payments_prompt = ChatPromptTemplate.from_messages([
    ("system", PAYMENTS_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{question}"),
])


def get_payments_chain():
    """Build and return the specialized payments chain."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return payments_prompt | llm.with_structured_output(PaymentsResponse)
