# Assessment Guide — Frequently Asked Questions

This document answers common questions about the assessment. Read it before starting.

---

## Scope & Time

**How much time should I spend on this?**
We suggest budgeting 6–10 hours of focused work. We value quality of thinking over quantity of output — a well-reasoned, clean notebook is better than an exhaustive but messy one.

**Do I need to complete all bonus exercises (A5–A8)?**
No. The four required exercises (A1–A4) are the core of the assessment. Bonus exercises are genuinely optional and are there for candidates who want to go deeper in areas they find interesting. Attempting one bonus exercise thoughtfully is worth more than rushing through all four.

---

## Technical Decisions

**What metric should I optimise for?**
There is no single correct answer — this is intentional. We want to see you make an informed choice and justify it. In credit risk, AUC-ROC and Gini are common, but business context matters: a model deployed at a specific cutoff may call for precision/recall trade-off analysis. Explain your reasoning.

**Do I need to use a time-based train/test split?**
Not strictly required. The dataset covers a 6-month window (April–September 2005) without a clear temporal ordering at the row level, so a random stratified split is a reasonable default. That said, if you choose to simulate a time-based split (e.g., train on April–July, test on August–September), explain your rationale — that reasoning is what we're evaluating.

**Which models should I use?**
At least two different model families. Common choices include logistic regression (good interpretability baseline), gradient boosting (XGBoost, LightGBM), and random forest. What matters is that you can justify your choices and interpret the results — not that you pick the "right" models.

**How polished does the code need to be?**
It should be reproducible and readable, following reasonable Python conventions (PEP 8). It does not need to be production-grade. Clear variable names, section headers, and brief comments explaining non-obvious steps matter more than perfect abstraction.

---

## Presentation (Part B)

**How long should Part B be?**
Short. Think of it as a 5-minute verbal briefing to a Risk Manager who doesn't read code. A few well-written paragraphs or a concise set of bullet points is ideal. You can include a chart or two if it adds clarity. It can live at the end of your notebook — no need for a separate document or slides unless you prefer that format.

---

## AI Tools

**Can I use AI tools (ChatGPT, Copilot, Claude, etc.)?**
Yes. We actively encourage it — using AI tools thoughtfully is part of how modern data scientists work. All we ask is that you note which tools you used and how (see the top of the starter notebook). The key requirement: **you must be able to explain and defend every part of your submission** in a follow-up conversation.

---

## Submission

**What do I need to submit?**
A link to your repository (GitHub, GitLab, etc.) with:
- A notebook (or structured Python project) that runs end-to-end without errors
- A `requirements.txt` or `environment.yml` so we can reproduce your environment
- A completed `SUBMISSION_TEMPLATE.md` at the root of the repo

**Should I include the dataset in my repo?**
The dataset is already included in this repo under `data/`. No need to re-download or re-add it.

---

## Questions

If anything is unclear, please reach out. We'd rather answer a question than have you spend time on a wrong assumption.
