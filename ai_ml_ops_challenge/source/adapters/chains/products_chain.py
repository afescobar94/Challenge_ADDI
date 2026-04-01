"""Specialized chain for product recommendations and promotions."""

import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()


class ProductsResponse(BaseModel):
    """Structured output for product-related responses."""

    reasoning: str = Field(..., description="Brief reasoning for the selected recommendation path. Max 20 words.")
    respuesta_final: str = Field(..., description="Final response in Colombian Spanish.")


PRODUCTS_SYSTEM_PROMPT = """\
You are Emporyum Tech's specialized products assistant.

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

## CATALOG CANDIDATES
{catalog_candidates}

## RULES
- Respond in natural Colombian Spanish.
- Use COP formatting with thousands separators when sharing prices.
- Prefer concrete recommendations over generic responses.
- If user asks for unavailable or out-of-scope products, redirect to Emporyum categories.
- Never compare competitor prices.
- Never invent products.
- If catalog data is insufficient, state the limitation and offer close alternatives.
- Never request or repeat OTP codes, passwords, full card numbers, CVV, or PIN.
- Keep response concise and actionable (2-6 sentences).
"""

products_prompt = ChatPromptTemplate.from_messages([
    ("system", PRODUCTS_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{question}"),
])


def get_products_chain():
    """Build and return the specialized products chain."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return products_prompt | llm.with_structured_output(ProductsResponse)
