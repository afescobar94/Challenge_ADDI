"""Routing chain for topic and agent selection.

This chain classifies the user's request into one of the valid KB topics,
chooses the responsible agent, and returns short reasoning for traceability.
"""

import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()


class RouterOutput(BaseModel):
    """Structured output for the router chain."""

    selected_topic: str = Field(..., description="One topic from the allowed topics list.")
    selected_agent: str = Field(..., description="The agent/node name responsible for the selected topic.")
    router_reasoning: str = Field(..., description="Short reasoning for classification. Max 20 words.")


ROUTER_SYSTEM_PROMPT = """\
You are a strict router for Emporyum Tech's assistant.

Your task:
1) Classify the user's latest question into one topic from ALLOWED_TOPICS.
2) Select the responsible agent from TOPIC_AGENT_MAP for that topic.
3) Return concise reasoning.

## ALLOWED_TOPICS
{allowed_topics}

## TOPIC_AGENT_MAP
{topic_agent_map}

## USER DATA SUMMARY
{user_data_summary}

## CONTEXT
- last_topic_selected: {last_topic_selected}
- previous_topics: {previous_topics}

## ROUTING RULES
- Output EXACTLY one valid topic from ALLOWED_TOPICS.
- If request is unrelated to Emporyum Tech, choose FUERA_DE_ALCANCE.
- If the current message is ambiguous but context is clear, prefer continuity with last_topic_selected.
- Use Colombian Spanish understanding for intent detection.
- Never invent topics or agents.
"""

router_prompt = ChatPromptTemplate.from_messages([
    ("system", ROUTER_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{question}"),
])


def get_router_chain():
    """Build and return the router chain with structured output."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return router_prompt | llm.with_structured_output(RouterOutput)
