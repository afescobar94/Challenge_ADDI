# Lending Data Scientist - Business Case

---

## Overview

This exercise is designed to evaluate your skills in applying data science techniques to solve real business problems in the lending and credit risk domain. There are no single correct answers — we aim to learn as much as possible about your knowledge, analytical thinking, and abilities as a Data Scientist.

The assessment has **two parts**:

1. **Part A** — Business Case: Credit Default Prediction (hands-on coding)
2. **Part B** — Results Presentation & Business Recommendations

**Estimated time:** max 5 days from receipt. Please let us know if you need more time.

---

## Part A — Business Case: Credit Default Prediction

### Context

You are a Data Scientist on the Risk team of a lending company. The Risk team needs a model that explains the **probability of default** for credit card clients, using historical data. Your work will inform the credit evaluation process and help the team make better lending decisions.

### Dataset

The **Default of Credit Card Clients** dataset is included in this repository under the `data/` folder.

- **Source:** [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients)
- **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Citation:** Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. *Expert Systems with Applications, 36*(2), 2473-2480.

The dataset contains 30,000 observations of credit card clients in Taiwan (April–September 2005) with 24 features including demographics, credit limit, repayment status, bill statements, and payment amounts.

**Target variable:** `default payment next month`

See `data/DATA_DICTIONARY.md` for a detailed description of all variables.

### Required Exercises

**A1. Exploratory Data Analysis (EDA)**
Obtain descriptive statistics of the population and create visualizations you consider important for your evaluation and for the business. Consider class balance, feature distributions, correlations, and any data quality issues.

**A2. Feature Engineering & Selection**
Select and/or engineer the features that have the greatest predictive power for the target variable. Justify your selection using appropriate techniques (e.g., IV/WoE analysis, statistical tests, feature importance, correlation analysis). Provide a per-variable report on your process.

**A3. Model Training & Evaluation**
Train at least two different model families and find the best-performing model. Justify your decisions using appropriate metrics (e.g., AUC-ROC, Gini, KS, precision-recall, F1). Discuss your validation strategy (e.g., cross-validation, hold-out, time-based split reasoning).

**A4. Model Interpretation & Business Recommendations**
Interpret the model results from a business perspective. Explain which factors most influence default probability and provide actionable recommendations to the Risk team. Consider how the model could be integrated into the credit approval workflow.

### Suggested Additional Exercises (Bonus)

These are not mandatory but will be positively valued:

**A5. Model Fairness & Bias Analysis**
Analyze whether your model exhibits disparate impact across demographic groups (e.g., gender, education level). Discuss how you would address fairness concerns in a production credit model.

**A6. Monitoring & Drift Strategy**
Propose a monitoring plan for the model once deployed. How would you detect concept drift or data drift? What metrics and alerts would you set up?

**A7. Rejection Inference**
Discuss the challenge of reject inference in credit scoring. The training data only contains clients who were previously approved — how might this bias the model, and what techniques could mitigate it?

**A8. Business Simulation**
Create a simple simulation showing the financial impact (expected profit/loss) of using your model at different score cutoff thresholds. Include assumptions about loan amounts, interest rates, and recovery rates.

---

## Part B — Results Presentation

Prepare a brief summary (can be part of your notebook or a separate document) that a non-technical stakeholder could understand. It should include:

- Key findings from your EDA
- What your model learned (top drivers of default)
- Your recommendation for a decision threshold and why
- Expected business impact and limitations

---

## A Note on AI Tools

We know AI tools like ChatGPT, GitHub Copilot, Claude, Cursor, and others are part of how many data scientists work today — and that's totally fine! You're welcome to use any AI tools you feel comfortable with during this assessment. If you leverage them thoughtfully, it can actually be a positive signal in your evaluation.

All we ask is that you're transparent about it. If you use AI, include a short note mentioning which tools you used and how (e.g., "Used Copilot for boilerplate plotting code" or "Asked ChatGPT to explain WoE, then implemented myself"). You can add this at the end of your notebook or as inline comments — whatever feels natural.

The key thing is: **make sure you can explain and defend every part of your solution.** Using AI smartly shows good judgment and is something we value. However, if any part of your submission was AI-generated and you can't walk us through it during the review, that could work against you. Think of AI as a co-pilot — you're still the one flying the plane.

---

## Technical Requirements

- Code must be **reproducible** — include a `requirements.txt` or equivalent, and set random seeds where applicable
- Follow good programming practices (e.g., PEP 8 for Python)
- Deliver as a **Jupyter Notebook** (.ipynb) with clear markdown sections, or as a well-structured Python project
- You may use any programming language, but **Python** is strongly preferred
- If using a GitHub repository, please ensure the reviewers has access (share the repo link or add the reviewer's GitHub username)

---

## Submission

- Share a link to your repository by the agreed deadline
- Ensure all code runs end-to-end without errors

---

## Questions?

If you have any questions about the assessment, dataset, or expectations, please don't hesitate to reach out. We're happy to clarify.

Good luck — we look forward to reviewing your work!
