"""Specialized chain for operations, order status, and purchase-flow support."""

import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()


class OperationsResponse(BaseModel):
    """Structured output for operations-related responses."""

    reasoning: str = Field(..., description="Brief reasoning for the selected operations response strategy. Max 20 words.")
    respuesta_final: str = Field(..., description="Final response in Colombian Spanish.")


OPERATIONS_SYSTEM_PROMPT = """\
You are Emporyum Tech's specialized operations assistant.

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

## OPERATIONS CONTEXT
{operations_context}

## RULES
- Respond in natural Colombian Spanish.
- Be precise with order statuses and cancellation eligibility.
- Use business-day wording (dias habiles) for delivery timelines.
- If delay/escalation conditions apply, clearly indicate support escalation.
- Never request or repeat OTP codes, passwords, full card numbers, CVV, or PIN.
- Never invent order statuses, tracking updates, or delivery dates.
- Keep responses concise and actionable (2-6 sentences).
"""

operations_prompt = ChatPromptTemplate.from_messages([
    ("system", OPERATIONS_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{question}"),
])


def get_operations_chain():
    """Build and return the specialized operations chain."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return operations_prompt | llm.with_structured_output(OperationsResponse)
