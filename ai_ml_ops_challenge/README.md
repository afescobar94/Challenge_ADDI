# AI & ML Ops Tech Challenge - Emporyum Tech Assistant

## Overview

**Emporyum Tech** is a Colombian e-commerce platform that offers buy-now-pay-later installment plans. In this challenge you will receive a **basic working prototype** of a conversational AI assistant for Emporyum Tech. The prototype runs end-to-end: you can ask it questions and it will respond. **But the quality is poor.** The architecture is minimal, the Knowledge Base is shallow, and responses are vague and generic.

Your task is to **significantly improve the assistant's quality and architecture**. How you do it -- what you build, how you structure it, what design decisions you make -- is entirely up to you.

## Time Estimate

**6-8 hours** for a complete solution. You do not need to finish everything -- a well-designed partial solution with clear documentation is better than a rushed complete one.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- An OpenAI API key (GPT-4o-mini is sufficient and cost-effective)

## Quick Start

Run the basic solution first. See it work. Notice the problems.

```bash
# 1. Install dependencies
poetry install

# 2. Create your .env file and add your OpenAI API key
cp .env.example .env

# 3. Run the assistant
poetry run python tests/inline.py
```

Try these conversations and observe the responses:

| You type | What you should notice |
|----------|----------------------|
| `Hola!` | Generic greeting, not personalized to the user |
| `Donde esta mi pedido?` | Vague answer, no specific order details |
| `Cuanto debo de cuotas?` | Vague answer, no installment breakdown |
| `Quiero devolver un producto` | One-shot generic response, no multi-step return flow |
| `Que hora es?` | Tries to answer anyway -- no out-of-scope handling |

## Business Context

**Emporyum Tech** is a Colombian e-commerce platform that differentiates itself through buy-now-pay-later installment plans. Customers can purchase products across multiple categories and split payments into monthly installments with varying interest rates.

The business is organized around 4 verticals, each with its own set of rules, edge cases, and data requirements:

- **Product & Catalog** (`team_product.md`): ~290 products across 4 categories (Electronics, Home, Fashion, Beauty). Product recommendations based on user history and preferences. 5 active promotions with specific rules.

- **Payments & Installments** (`team_payments.md`): 4 payment methods (PSE, Card, Efecty, Bancolombia A la Mano). Installment plans from 1 to 24 months with different interest rates. Late payment policies and calculations.

- **Operations & Logistics** (`team_operations.md`): Complete purchase flow from browsing to delivery. Order tracking through 6 statuses. Delivery times by city. Returns and refund policies with specific eligibility rules.

- **Platform & Account** (`team_platform.md`): Account management, password reset, 2FA. App features and troubleshooting. Security policies.

Detailed business requirements for each area are available in `docs/stakeholder_interviews/`. These interview transcripts contain the specific rules, flows, edge cases, and data fields you need to design the Knowledge Base and the assistant's architecture.

## Project Structure

```
ai_ml_ops_challenge/
|
|-- README.md                            # <-- YOU ARE HERE
|-- pyproject.toml                       # Project dependencies
|-- .env.example                         # Template for your API key
|-- .env                                 # You create this (not committed to git)
|
|-- docs/
|   |-- stakeholder_interviews/          # Your primary input: business requirements
|       |-- team_product.md              #   Product team interview
|       |-- team_payments.md             #   Payments team interview
|       |-- team_operations.md           #   Operations team interview
|       |-- team_platform.md             #   Platform team interview
|
|-- source/
|   |-- __init__.py
|   |
|   |-- application/
|   |   |-- __init__.py
|   |   |-- state.py                     # GraphState TypedDict (do not modify)
|   |   |-- graph.py                     # Graph definition
|   |
|   |-- domain/
|   |   |-- __init__.py
|   |   |-- fetch_user_data.py           # Fetches user data from mock profiles
|   |   |-- handle_general.py            # Generic agent handler
|   |
|   |-- adapters/
|   |   |-- __init__.py
|   |   |-- chains/
|   |   |   |-- __init__.py
|   |   |   |-- general_chain.py         # Generic LLM chain
|   |   |-- utils/
|   |       |-- __init__.py
|   |       |-- mock_data.py             # 8 mock user profiles (do not modify)
|   |       |-- data_filter.py           # Utility to filter user data by topic
|   |       |-- knowledge_base.py        # Knowledge Base definitions
|   |
|   |-- examples/                        # Framework pattern references (do not modify)
|       |-- README.md
|       |-- example_kb_entry.py          #   Knowledge Base topic schema
|       |-- example_chain.py             #   LLM chain with Pydantic output
|       |-- example_domain_function.py   #   Async domain function pattern
|       |-- example_graph.py             #   Minimal runnable graph (setup verification)
|
|-- tests/
|   |-- __init__.py
|   |-- inline.py                        # Interactive testing script
|
|-- deliverables/
    |-- architecture.md                  # Your architecture document
    |-- deployment_answers.md            # Your deployment answers
```

## What's Pre-Built (Do Not Modify)

These files are provided and should not be modified:

| File | Description |
|------|-------------|
| `source/application/state.py` | `GraphState` TypedDict that defines all fields flowing through the graph |
| `source/adapters/utils/mock_data.py` | 8 mock user profiles with orders, payments, and account data |
| `source/adapters/utils/data_filter.py` | Utility to filter user data to only topic-relevant fields |
| `source/examples/*` | Framework pattern references |
| `tests/inline.py` | Interactive testing script with MemorySaver checkpointing |
| `docs/stakeholder_interviews/*` | 4 stakeholder interview transcripts |
| `pyproject.toml` | Project dependencies |

## Current Problems

Run the assistant and you will notice several problems:

| Problem | Where to look |
|---------|--------------|
| Every question gets the same generic treatment | `handle_general.py`, `graph.py` |
| Responses are vague and impersonal | `general_chain.py` |
| The Knowledge Base is shallow -- vague instructions, single scenarios, missing data fields | `knowledge_base.py` |
| User data is not used effectively | `handle_general.py` |
| The assistant cannot handle multi-turn conversations | `state.py` (note the available fields) |

Your job is to understand the business requirements from the stakeholder interviews, design an improved architecture, and implement it.

## Deliverables

1. **An improved assistant** -- The bot should demonstrate significantly better quality across the topics covered in the stakeholder interviews. How you achieve this -- what you build, how you structure it, what architecture you choose -- is entirely your decision. Use the framework patterns in `source/examples/` as reference.

2. **Architecture documentation** (`deliverables/architecture.md`) -- Document your design: a diagram of your system, the key decisions you made and why, and any trade-offs you considered.

3. **Deployment answers** (`deliverables/deployment_answers.md`) -- Answer the production readiness and ML Ops questions.

## Evaluation Criteria

What we value, roughly in order of importance:

- **Knowledge Base quality** -- Can you extract real business rules from the stakeholder interviews and translate them into structured, useful KB entries?
- **Cognitive architecture** -- How do you decompose the problem? How do agents, state, and graph topology work together? Are your design decisions intentional?
- **Output quality** -- Does the bot give good, personalized answers using the user's data? Does it handle edge cases?
- **Deployment & production thinking** -- Thoughtful answers to the questions in `deliverables/deployment_answers.md`.
- **Architecture documentation** -- Clear explanation of your design in `deliverables/architecture.md`.

You are free to use AI tools (ChatGPT, Claude, Copilot, etc.) during the challenge. However, after submission we will do a **follow-up conversation** where we ask you to walk us through your decisions -- why you chose a particular architecture, how you structured the KB, what trade-offs you considered. You must be able to explain and defend every decision in your solution.

## Tips

1. **Run the basic solution first and notice the problems before changing anything.** Before modifying code, run `poetry run python tests/inline.py` and try several questions. Understand what you are working with.

2. **Read ALL 4 stakeholder interviews before writing code.** They are your primary source of requirements.

3. **Check `source/examples/` for the framework patterns used in this project.** There is a working example for KB entries, LLM chains, domain functions, and graph construction.

4. **Read `state.py` to understand what fields are available in the graph state.** Every node receives the full state and returns a partial dict to update it.

5. **Check `mock_data.py` to see what user data exists.** There are 8 user profiles covering different situations (new users, late payments, return-eligible orders, etc.).

6. **Simple and working is better than complex and broken.**

## Submission

1. Ensure `poetry run python tests/inline.py` runs without import errors.
2. Verify at least one complete conversation flow works end-to-end.
3. Zip the entire `ai_ml_ops_challenge/` folder.
4. Send it back to us.

Good luck!
