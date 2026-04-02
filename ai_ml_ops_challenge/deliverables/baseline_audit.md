# Baseline Audit - Emporyum Tech Assistant

## 1. Context
This document captures the project baseline before implementing challenge improvements.
Goal: provide clear evidence of the initial state, requirement gaps, and success criteria for upcoming branches.

## 2. Scope and Constraints
The following files/directories must not be modified during implementation:

- `source/application/state.py`
- `source/adapters/utils/mock_data.py`
- `source/adapters/utils/data_filter.py`
- `source/examples/*`
- `tests/inline.py`
- `docs/stakeholder_interviews/*`
- `pyproject.toml`

## 3. Current System State (Technical Baseline)

### 3.1 Stack
- Python + Poetry (dependency management)
- LangGraph (`StateGraph`) for conversational flow orchestration
- LangChain + ChatOpenAI for LLM invocation
- Pydantic for structured chain outputs
- `MemorySaver` in interactive tests (`tests/inline.py`)

### 3.2 Current Graph Flow
Single current flow:

`fetch_user_data -> handle_general -> END`

Implications:
- No intent/topic routing exists.
- No specialized domain agents are implemented.
- All requests are handled by a single generic chain.

### 3.3 Existing Components
- `source/domain/fetch_user_data.py`: loads user profile from mock data.
- `source/domain/handle_general.py`: handles all questions in a single node.
- `source/adapters/chains/general_chain.py`: single generic prompt.
- `source/adapters/utils/knowledge_base.py`: initial KB with shallow structure.
- `source/adapters/utils/mock_data.py`: user profiles + broad catalog (key personalization input).

## 4. Functional Findings

### 4.1 What currently works
- The bot responds end-to-end.
- User data is retrieved successfully.
- It can answer simple order/payment questions when the LLM infers correctly from context.

### 4.2 Observed issues
- No topic classification (`selected_topic` remains `None` in current runs).
- No agent selection (`selected_agent` remains `None`).
- KB is too shallow for complex business rules.
- Returns flow is not truly multi-turn.
- Limited coverage for security/compliance edge cases.
- A Pydantic serialization warning appears at runtime (non-blocking but technical debt).

## 5. Gap Analysis vs Challenge Requirements

### 5.1 Challenge requirements
- Significantly improve response quality.
- Improve cognitive architecture (router + agents + graph topology).
- Implement business rules extracted from all 4 stakeholder interviews.
- Implement multi-step flow (especially returns).
- Deliver high-quality `deliverables/architecture.md` and `deliverables/deployment_answers.md`.

### 5.2 Current gaps
- Architecture: missing router and domain specialization.
- Knowledge base: insufficient scenario depth, conditions, and topic variables.
- Multi-turn behavior: state fields exist but are not effectively used.
- Guardrails: missing explicit policies for OTP, credentials, competitor comparisons, and catalog hallucinations.
- Quality traceability: missing behavior regression tests.

## 6. Success Criteria for Next Branches
- Router classifies topic with traceable reasoning.
- Graph routes to specialized domain agents.
- KB includes real rules, edge cases, and actionable guidance.
- Returns flow works in at least two steps with conversational continuity.
- Responses are personalized with user data and consistent COP formatting.
- Guardrails and out-of-scope handling are consistent.
- Unit and integration tests cover critical business scenarios.

## 7. Baseline Evidence (Manual)
Baseline prompts executed in `tests/inline.py` before functional changes:
- `Hola!` -> generic greeting response.
- `Donde esta mi pedido?` -> responds, but without a specialized pipeline.
- `Cuanto debo de cuotas?` -> responds, but without dedicated routing/calculation logic.
- `Quiero devolver un producto` -> one-shot response, no multi-step flow.
- `Que hora es?` -> out-of-scope response handling is limited.

## 8. Initial Risks to Track
- Interview contradictions (e.g., installments via PSE): resolve using highest-authority source or explicit assumptions.
- Mock data has old dates/promotions: avoid claiming real-world validity; respond based on system data available.
- Over-engineering risk within 6-8 hours: prioritize impact according to evaluation criteria.

## 9. Branch Outcome
- Baseline and control documentation is ready.
- No functional assistant code changes were introduced.
