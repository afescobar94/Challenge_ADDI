# Data Dictionary — Default of Credit Card Clients

**Source:** UCI Machine Learning Repository
**DOI:** 10.24432/C55S3H
**License:** CC BY 4.0

## Dataset Overview

- **Instances:** 30,000
- **Features:** 23 (+ 1 target variable)
- **Missing Values:** None
- **Time Period:** April–September 2005
- **Geography:** Taiwan

## Variables

| Variable | Description | Type | Values |
|----------|-------------|------|--------|
| `ID` | Client ID | Integer | Unique identifier |
| `LIMIT_BAL` | Amount of given credit (NT dollars) | Continuous | Includes individual and family credit |
| `SEX` | Gender | Categorical | 1 = male, 2 = female |
| `EDUCATION` | Education level | Categorical | 1 = graduate school, 2 = university, 3 = high school, 4 = others, 5 = unknown, 6 = unknown |
| `MARRIAGE` | Marital status | Categorical | 1 = married, 2 = single, 3 = others |
| `AGE` | Age in years | Continuous | — |
| `PAY_0` | Repayment status in September 2005 | Categorical | -2 = no consumption, -1 = paid in full, 0 = use of revolving credit, 1 = payment delay 1 month, ..., 9 = payment delay 9+ months |
| `PAY_2` | Repayment status in August 2005 | Categorical | Same as PAY_0 |
| `PAY_3` | Repayment status in July 2005 | Categorical | Same as PAY_0 |
| `PAY_4` | Repayment status in June 2005 | Categorical | Same as PAY_0 |
| `PAY_5` | Repayment status in May 2005 | Categorical | Same as PAY_0 |
| `PAY_6` | Repayment status in April 2005 | Categorical | Same as PAY_0 |
| `BILL_AMT1` | Bill statement amount in September 2005 (NT dollars) | Continuous | — |
| `BILL_AMT2` | Bill statement amount in August 2005 (NT dollars) | Continuous | — |
| `BILL_AMT3` | Bill statement amount in July 2005 (NT dollars) | Continuous | — |
| `BILL_AMT4` | Bill statement amount in June 2005 (NT dollars) | Continuous | — |
| `BILL_AMT5` | Bill statement amount in May 2005 (NT dollars) | Continuous | — |
| `BILL_AMT6` | Bill statement amount in April 2005 (NT dollars) | Continuous | — |
| `PAY_AMT1` | Amount of previous payment in September 2005 (NT dollars) | Continuous | — |
| `PAY_AMT2` | Amount of previous payment in August 2005 (NT dollars) | Continuous | — |
| `PAY_AMT3` | Amount of previous payment in July 2005 (NT dollars) | Continuous | — |
| `PAY_AMT4` | Amount of previous payment in June 2005 (NT dollars) | Continuous | — |
| `PAY_AMT5` | Amount of previous payment in May 2005 (NT dollars) | Continuous | — |
| `PAY_AMT6` | Amount of previous payment in April 2005 (NT dollars) | Continuous | — |

## Target Variable

| Variable | Description | Type | Values |
|----------|-------------|------|--------|
| `default payment next month` | Whether the client defaults in the following month | Binary | 0 = no default, 1 = default |

## Notes

- The repayment status variables (`PAY_0` through `PAY_6`) use a scale where negative values indicate no delay, 0 indicates revolving credit usage, and positive values indicate months of payment delay.
- `PAY_0` refers to September (the most recent month), while `PAY_6` refers to April (the earliest month in the dataset).
- Note there is no `PAY_1` variable in the dataset — the naming jumps from `PAY_0` to `PAY_2`.
- The dataset is imbalanced: approximately 22% of clients default.

## Citation

Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. *Expert Systems with Applications, 36*(2), 2473-2480.
