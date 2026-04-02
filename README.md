# Addi Data Science Technical Assessment

For this assessment, I completed the **AI & ML Ops — Emporyum Tech Chatbot** challenge as my main implementation. Additionally, I selected the **Lending — Credit Default Prediction** challenge for the solution proposal.

## Repository Structure

- `ai_ml_ops_challenge/` — Main implemented challenge
- `lending_ds_challenge/` — Additional challenge delivered as a high-level solution proposal

## 1) AI & ML Ops — Emporyum Tech Chatbot (Main Implementation)

### Challenge goal
Improve a baseline conversational assistant with poor response quality, shallow knowledge coverage, and weak handling of real business flows.

### What I implemented

- Built a **stateful LangGraph architecture** with routing and specialized handlers:
  - `fetch_user_data -> route_topic -> specialized agent -> END`
- Implemented **hybrid routing** in `route_topic`:
  - deterministic guardrails and keyword overrides first
  - LLM router for ambiguous intents
  - safe fallback behavior when routing fails
- Implemented **specialized domain agents**:
  - `handle_products`
  - `handle_payments`
  - `handle_operations`
  - `handle_platform`
  - `handle_returns`
  - `handle_general` as safe fallback
- Expanded and structured the **Knowledge Base** (`SCENARIO_KNOWLEDGE_BASE`) with business rules, scenarios, and topic-level variables.
- Added **deterministic guardrails** for security and policy compliance:
  - sensitive payment/auth secret detection
  - competitor-comparison restriction
  - out-of-scope detection and redirection
- Implemented a **multi-turn returns workflow** with explicit step continuity (`current_step`, `is_return_in_progress`) and eligibility checks.
- Added **response quality controls** (formatting, clarity, actionability) and defensive error handling/fallbacks.
- Added and validated a **test suite** for domain handlers, routing, guardrails, and graph integration.

### Evidence of implementation quality

- Automated tests: `26 passed` (`pytest -q`)
- End-to-end validation matrix: `51/51` scenarios passed
- Interactive flow validated with `tests/inline.py`

### Main deliverables

- Architecture design: `ai_ml_ops_challenge/deliverables/architecture.md`
- Production readiness answers: `ai_ml_ops_challenge/deliverables/deployment_answers.md`
- Validation evidence: `ai_ml_ops_challenge/deliverables/release_validation.md`

## 2) Lending — Credit Default Prediction (Solution Proposal)

### Challenge goal
Design an end-to-end credit default prediction approach for risk decisioning using the provided UCI credit-card dataset.

### What I delivered

I delivered a **high-level, production-oriented proposal** (not a full implementation), covering:

- Problem framing and success metrics (AUC-ROC, Gini, KS, calibration, business impact)
- Data ingestion and quality strategy (including handling of dataset header structure)
- EDA plan focused on risk signal and business interpretation
- Feature engineering strategy (delinquency, utilization, payment behavior, trends)
- Champion/challenger modeling approach:
  - interpretable baseline (Logistic Regression + WoE)
  - high-performance candidate (LightGBM/XGBoost)
- Threshold selection via expected-loss / business-cost optimization
- Model interpretation approach (global + local explanations)
- Bonus strategy proposals:
  - fairness and bias analysis
  - monitoring and drift detection
  - reject inference
  - business simulation by threshold
- Scalable MLOps architecture and an 8-week implementation roadmap

### Proposal deliverable

- `lending_ds_challenge/SUBMISSION_TEMPLATE.md`

## Notes

- The AI & ML Ops challenge is the main implemented solution in this repository.
- The Lending challenge is intentionally documented as a proposal, aligned with the assessment requirement to provide one additional challenge at solution-design level.
