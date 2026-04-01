"""Specialized chain for returns and refund flow messaging."""

import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()


class ReturnsResponse(BaseModel):
    """Structured output for returns-flow responses."""

    reasoning: str = Field(..., description="Brief reasoning for the response strategy. Max 20 words.")
    respuesta_final: str = Field(..., description="Final user-facing response in Colombian Spanish.")


RETURNS_SYSTEM_PROMPT = """\
You are Emporyum Tech's specialized returns assistant.

## FLOW STEP
{current_step}

## RETURNS STATE
{returns_state}

## DRAFT RESPONSE
{draft_response}

## RULES
- Keep business constraints from the draft response exactly intact.
- Keep response in natural Colombian Spanish.
- Keep response concise and actionable (2-6 sentences).
- Do not invent policies, deadlines, or order data.
- Never request or repeat OTP codes, passwords, full card numbers, CVV, or PIN.
- If the draft indicates escalation, keep clear escalation wording.
"""

returns_prompt = ChatPromptTemplate.from_messages([
    ("system", RETURNS_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{question}"),
])


def get_returns_chain():
    """Build and return the specialized returns chain."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return returns_prompt | llm.with_structured_output(ReturnsResponse)
