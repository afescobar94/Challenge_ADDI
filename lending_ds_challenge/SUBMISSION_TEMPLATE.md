# Submission Checklist

Please complete this file before submitting. It takes ~5 minutes and helps reviewers quickly orient to your work.

---

## Candidate Info

- **Name:** Andres Escobar
- **Submission date:** 2026-04-01
- **Repository link:** https://github.com/afescobar94/Challenge_ADDI.git

---

## AI Tools Disclosure

*(List any AI tools used and how. Examples: "Used GitHub Copilot for boilerplate plotting code", "Asked ChatGPT to explain WoE, then implemented myself", "None")*

- I used Codex/ChatGPT to structure and refine this solution proposal, improve technical writing quality, and check consistency with the assessment requirements. I reviewed and validated all final decisions and trade-offs.

---

## Reproducibility

- [x] This file is a **solution proposal** for the additional challenge (full implementation is not required)
- [ ] All code runs end-to-end without errors from a clean environment
- [ ] Random seeds are set (default: `RANDOM_SEED = 42`)
- [x] Dependencies are listed in `requirements.txt` or `environment.yml`
- [x] Dataset is present at `data/default_of_credit_card_clients.csv`

**Python version used:** 3.11 (planned for implementation)

**How to run:**
```bash
# Planned flow (if implemented):
pip install -r requirements.txt
jupyter notebook notebooks/starter.ipynb
```

---

## Exercises Completed

- [] A1 — Exploratory Data Analysis *(proposal level)*
- [] A2 — Feature Engineering & Selection *(proposal level)*
- [] A3 — Model Training & Evaluation *(proposal level)*
- [] A4 — Model Interpretation & Business Recommendations *(proposal level)*
- [] A5 — Model Fairness & Bias Analysis *(bonus, proposal level)*
- [] A6 — Monitoring & Drift Strategy *(bonus, proposal level)*
- [] A7 — Rejection Inference *(bonus, proposal level)*
- [] A8 — Business Simulation *(bonus, proposal level)*
- [] Part B — Results Presentation *(proposal level)*

---

## Summary (for the reviewer)

**Best model and key metric:**
I would use a Gradient Boosting model (LightGBM) as the likely champion for predictive power, and a Logistic Regression + WoE scorecard as an interpretable baseline/challenger. I would prioritize AUC-ROC, Gini, and KS, and then choose the final operating point using expected-loss minimization.

**Recommended decision threshold and rationale:**
I would select the threshold through business-cost optimization (false negative cost > false positive cost), with constraints for risk appetite and approval-rate targets. I would finalize it with Risk and Product teams using expected profit and delinquency stress scenarios.

**Top 3 drivers of default:**
1. Recent delinquency behavior (`PAY_0`, `PAY_2`, and delinquency trend)
2. Payment-to-bill dynamics (payment ratio and persistent underpayment)
3. Utilization pressure (bill-to-limit behavior and volatility)

**One thing you'd do differently with more time:**
I would incorporate external/alternative data and design a complete reject inference pipeline with policy simulation on new vintages to improve calibration under selection bias.

---

## Notes for Reviewers

### 0) Scope clarification
This document is intentionally a **high-level solution proposal** for the additional challenge in the assessment instructions. It is not presented as a fully implemented notebook.

### 1) Problem framing and success criteria
I would frame the problem as estimating next-month probability of default (PD) and integrating the score into credit underwriting decisions.

Business KPIs I would target:
- Lower expected credit losses while preserving healthy approval rates.
- Improve risk ranking quality (separation between good and bad clients).
- Maintain transparent model governance for validation and audit.

Technical KPIs I would track:
- Discrimination: AUC-ROC, Gini, KS.
- Threshold-level performance: precision, recall, F1, default capture rate.
- Calibration: Brier score and calibration curves.
- Stability: population and score stability by time slices.

### 2) Data understanding and ingestion strategy
Based on the repository dataset, I would account for the following:
- The CSV has a double-header structure (`X1...X23, Y` + a second line with canonical names), so I would normalize schema explicitly during ingestion.
- The dataset size is around 30k rows with moderate class imbalance (~22% defaults).
- Missing values are not expected, but category values include uncommon labels (e.g., `EDUCATION` has values 0/5/6).

Ingestion steps I would implement:
1. Deterministic parsing with explicit mapping to canonical column names.
2. Exclude `ID` from modeling while keeping it for lineage and traceability.
3. Generate a data-quality report (nulls, duplicates, invalid ranges, outliers, category anomalies).
4. Freeze a versioned modeling dataset (`vYYYYMMDD`) for reproducibility.

### 3) A1 — EDA proposal
Analyses I would prioritize:
- Class balance and baseline default rate.
- Univariate distributions (skewness, heavy tails, outliers).
- Categorical risk profiling by `SEX`, `EDUCATION`, `MARRIAGE`.
- Temporal behavior encoded in `PAY_x`, `BILL_AMTx`, `PAY_AMTx`.
- Correlation and multicollinearity checks across monthly series.

Business-oriented visuals I would include:
- Default rate by delinquency bucket.
- Default heatmap by age and credit-limit bands.
- Payment-ratio trajectories for defaulters vs non-defaulters.

### 4) A2 — Feature engineering and selection proposal
Features I would engineer (high signal + explainability):
- **Repayment behavior features:**
  - `max_delinquency_6m`, `avg_delinquency_6m`, `recent_delinquency_gap`
  - Count of months with delay > 0
- **Utilization and stress features:**
  - `utilization_t = BILL_AMT_t / LIMIT_BAL` (with clipping/winsorization)
  - Peak utilization and utilization volatility over 6 months
- **Payment discipline features:**
  - `payment_ratio_t = PAY_AMT_t / BILL_AMT_t` (safe denominator rules)
  - Rolling underpayment count and trend
- **Trend features:**
  - Month-over-month slope in delinquency and payment ratio

Selection framework I would apply:
- Initial filtering: variance checks, missingness checks, high-correlation pruning.
- Predictive power: IV/WoE with `optbinning` for interpretable variables.
- Model-based validation: SHAP importance + permutation importance.
- Stability filter: retain variables with consistent signal across CV folds.

### 5) A3 — Modeling and evaluation proposal
Champion/challenger setup I would use:
1. **Interpretable baseline:** Logistic Regression with WoE-transformed features.
2. **Non-linear candidate:** LightGBM (or XGBoost) with class-imbalance handling.
3. Optional benchmark: Random Forest.

Validation strategy I would use:
- Stratified train/validation/test split for the primary benchmark.
- Repeated stratified cross-validation for variance estimation.
- Optional pseudo-temporal validation for generalization stress testing.

Threshold optimization I would perform:
- Define a business cost matrix (FP/FN) with the Risk team.
- Simulate expected loss/profit across threshold grids.
- Select the threshold that maximizes utility under approval and bad-rate constraints.

Analytical artifacts I would deliver:
- ROC/PR curves, KS table, lift/gain curves.
- Confusion matrices at candidate thresholds.
- Calibration curve and recalibration (Platt/Isotonic) if needed.

### 6) A4 — Interpretation and business recommendations proposal
Interpretation stack I would produce:
- Global explanations: SHAP summary and partial dependence.
- Local explanations: reason-code style outputs for decision transparency.
- Segment-level decomposition: risk behavior by customer profile.

Decision workflow I would propose:
- `PD < T1`: auto-approve.
- `T1 <= PD < T2`: manual review + reduced exposure/limit.
- `PD >= T2`: decline or request stronger conditions.

Business levers I would enable:
- Risk-based credit limits.
- Risk-based pricing / installment constraints.
- Early-warning lists for collections strategy.

### 7) Bonus proposal A5–A8
A5. Fairness & bias:
- I would compare TPR/FPR and approval rates across sensitive groups (`SEX` and proxy segments).
- I would compute disparate impact ratio and equal-opportunity gaps.
- If material gaps appear, I would evaluate feature revisions, policy adjustments, and constrained retraining.

A6. Monitoring & drift:
- I would monitor data drift with PSI (numeric) and CSI (categorical).
- I would monitor score drift with score PSI and approval-rate drift.
- I would monitor delayed-label performance drift (AUC/KS/calibration by vintage).
- I would define warning/critical alerts with clear remediation playbooks.

A7. Rejection inference:
- I would explicitly address selection bias (only approved applicants have observed outcomes).
- I would evaluate augmentation, parceling, fuzzy augmentation, and semi-supervised approaches.
- I would recommend a controlled pilot before production use.

A8. Business simulation:
- I would build an expected-value simulator by threshold.
- Inputs: loan amount, APR/margin, PD, LGD, recovery rate, operational cost.
- Outputs: expected profit, expected loss, approval rate, projected bad rate.
- I would include base/adverse/severe stress scenarios for risk committee decisions.

### 8) Scalable production architecture (proposed)
Architecture components I would implement:
1. **Data layer:** scheduled ingestion, feature marts, and quality controls.
2. **Feature layer:** reusable definitions with offline/online parity.
3. **Training layer:** reproducible pipelines, experiment tracking, model registry.
4. **Serving layer:** batch portfolio scoring + low-latency API for originations.
5. **Monitoring layer:** drift/performance/fairness dashboards and alerts.
6. **Governance layer:** model cards, lineage, approval workflows, rollback.

MLOps principles I would enforce:
- Immutable data/model versioning.
- CI checks for schema, tests, and reproducibility.
- Champion/challenger deployment with shadow testing.
- Scheduled retraining with Risk approval gates.

### 9) Implementation roadmap (8 weeks)
- Week 1: ingestion hardening, EDA, and business metric alignment.
- Week 2: feature engineering and variable report (IV/WoE + domain features).
- Week 3: baseline/challenger model development and validation framework.
- Week 4: threshold optimization, business simulation, interpretation package.
- Week 5: fairness baseline and initial drift monitoring setup.
- Week 6: pipeline automation and model registry integration.
- Week 7: UAT with Risk stakeholders and policy calibration.
- Week 8: controlled rollout (champion/challenger) and hypercare.

### 10) Key risks and trade-offs
- Interpretability vs raw performance: tree models may perform better but require stronger explanation and governance layers.
- Historical bias and reject inference: observed labels are policy-dependent.
- Label latency: monitoring should separate leading and lagging indicators.
- Policy drift: underwriting policy changes can deteriorate calibration without timely retraining.
