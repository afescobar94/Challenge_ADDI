"""Specialized chain for account, app troubleshooting, and platform security."""

import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()


class PlatformResponse(BaseModel):
    """Structured output for platform and account responses."""

    reasoning: str = Field(..., description="Brief reasoning for the selected platform response strategy. Max 20 words.")
    respuesta_final: str = Field(..., description="Final response in Colombian Spanish.")


PLATFORM_SYSTEM_PROMPT = """\
You are Emporyum Tech's specialized platform assistant.

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

## PLATFORM CONTEXT
{platform_context}

## RULES
- Respond in natural Colombian Spanish.
- Prioritize in-app self-service steps before escalation when possible.
- Never request passwords, OTP codes, or full payment credentials.
- Never echo back sensitive credentials even if user shares them.
- For phishing/suspicious requests, warn clearly and redirect to secure official channels.
- For suspicious activity or locked accounts, guide to secure support verification.
- Keep responses concise and actionable (2-6 sentences).
- Use concrete instructions and include one clear next step.
"""

platform_prompt = ChatPromptTemplate.from_messages([
    ("system", PLATFORM_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{question}"),
])


def get_platform_chain():
    """Build and return the specialized platform chain."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return platform_prompt | llm.with_structured_output(PlatformResponse)
