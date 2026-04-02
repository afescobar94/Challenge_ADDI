# Implementation Checklist - Modular Execution Plan

## 1. Control Rules

### 1.1 Non-modifiable files
- `source/application/state.py`
- `source/adapters/utils/mock_data.py`
- `source/adapters/utils/data_filter.py`
- `source/examples/*`
- `tests/inline.py`
- `docs/stakeholder_interviews/*`
- `pyproject.toml`

### 1.2 Branch naming convention
- New capabilities: `feature/<scope>`
- Bug fixes: `fix/<scope>`
- Tests: `test/<scope>`
- Documentation: `docs/<scope>`
- Baseline/light setup tasks: `chore/<scope>`

### 1.3 Commit naming convention
- `feat: ...`
- `fix: ...`
- `test: ...`
- `docs: ...`
- `chore: ...`

## 2. Modules and Deliverables by Branch

### Module 0 - Baseline (current)
- Branch: `chore/baseline-audit`
- Deliverables: `deliverables/baseline_audit.md`, `deliverables/implementation_checklist.md`
- Exit criteria: baseline documented with no functional changes

### Module 1 - Target architecture
- Branch: `docs/architecture-blueprint-v1`
- Deliverable: first version of `deliverables/architecture.md`
- Exit criteria: diagram, proposed agents, initial decisions and trade-offs

### Module 2 - Topic router
- Branch: `feature/router-topic-classification`
- Deliverable: classification node/chain + routing logic in `graph.py`
- Exit criteria: `selected_topic`, `selected_agent`, and `router_reasoning` populated consistently

### Module 3 - Enriched knowledge base
- Branch: `feature/kb-business-rules-expansion`
- Deliverable: `knowledge_base.py` expanded with real domain rules and edge cases
- Exit criteria: each topic includes detailed instructions, scenarios, and relevant variables

### Module 4 - Product and payments agents
- Branch: `feature/agents-product-payments`
- Deliverable: specialized handlers/chains for recommendations, promotions, payment methods, installments, and interests
- Exit criteria: concrete, personalized responses aligned with business rules

### Module 5 - Operations and platform agents
- Branch: `feature/agents-operations-platform`
- Deliverable: handlers/chains for buying flow, order status, account/app support, troubleshooting, and security
- Exit criteria: strong coverage of operations/platform flows and edge cases

### Module 6 - Returns multi-step workflow
- Branch: `feature/returns-multistep-workflow`
- Deliverable: step-1 validation + step-2 confirmation with conversational continuity
- Exit criteria: multi-turn returns flow working with existing state fields

### Module 7 - Guardrails and out-of-scope handling
- Branch: `feature/guardrails-security-scope`
- Deliverable: explicit policies for data leakage prevention, anti-hallucination, no competitor comparison, and out-of-scope handling
- Exit criteria: safe and consistent responses under adversarial prompts

### Module 8 - Response quality
- Branch: `feature/response-quality-personalization`
- Deliverable: improvements in COP formatting, clarity, personalization, and consistency
- Exit criteria: reduced vagueness and increased actionability

### Module 9 - Technical stability
- Branch: `fix/runtime-warnings-and-fallbacks`
- Deliverable: runtime error handling, serialization stability, and fallbacks
- Exit criteria: stable execution across multi-turn conversations

### Module 10 - Testing and regression
- Branch: `test/agent-behavior-regression`
- Deliverable: unit and integration tests for critical routes
- Exit criteria: runnable suite covering key business scenarios

### Module 11 - Final architecture documentation
- Branch: `docs/architecture-final`
- Deliverable: final `deliverables/architecture.md`
- Exit criteria: document fully aligned with real implementation

### Module 12 - Final MLOps answers
- Branch: `docs/deployment-answers-final`
- Deliverable: final `deliverables/deployment_answers.md`
- Exit criteria: practical, defensible, production-oriented answers

### Module 13 - Release closure
- Branch: `release/challenge-submission`
- Deliverable: final consolidation for PR into `main`
- Exit criteria: full checklist completion + end-to-end validation

## 3. Minimum PR Template per Module
- Module objective
- Scope (files changed)
- Business rules covered
- Evidence (test prompts + expected/actual behavior)
- Risks and follow-up items

## 4. Global Completion Checklist
- [x] All non-modifiable files were respected
- [x] Bot routes by topic and agent
- [x] Returns multi-step flow is implemented
- [x] Security/compliance edge cases are covered
- [x] `deliverables/architecture.md` is finalized
- [x] `deliverables/deployment_answers.md` is finalized
- [x] End-to-end conversation validated with `tests/inline.py`
