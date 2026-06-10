# credit-risk-porfolio-analysis
Credit Risk Portfolio Analysis

Project Overview

This project analyzes credit risk patterns using loan application data.
The goal is to identify high-risk customer segments, understand key default risk drivers, and support portfolio risk monitoring using Python, SQLite, and SQL.

This project focuses on SQL-based portfolio analytics rather than machine learning. It is designed to demonstrate data cleaning, feature engineering, database creation, SQL querying, risk segmentation, and business recommendation.

Business Problem

Financial institutions need to understand which customer groups are more likely to default.
By analyzing default rates across loan grades, debt-to-income levels, loan-to-income groups, home ownership status, loan purposes, and risk segments, this project helps support:

* Portfolio risk monitoring
* Credit policy analysis
* Risk segmentation
* Early identification of high-risk customer groups
* Data-driven credit decision-making

Dataset

* Dataset: Credit Risk Dataset
* Source: Kaggle - Credit Risk Dataset
* Target variable: loan_status
* Records before cleaning: 32,581 loan applicants
* Records after cleaning: 32,576 loan applicants
* Overall default rate: 21.82%

Tools Used

* Python
* Pandas
* SQLite
* SQL
* CSV output reports

Project Workflow

01. Data Cleaning

The original dataset was loaded and checked for basic data quality issues.

Main steps:

* Checked dataset shape, missing values, duplicated rows, and categorical variables.
* Checked outliers such as age above 100 and invalid employment length.
* Removed 5 age outliers where person_age was above 100.
* Filled missing loan_int_rate using the median interest rate by loan_grade.
* Filled missing person_emp_length using the median value.
* Saved the cleaned dataset as credit_risk_cleaned.csv.

Key results:

* Cleaned dataset: 32,576 rows and 29 columns.
* Missing values after cleaning: 0.
* Duplicated rows: 0.

02. Feature Engineering

New risk-related groups were created to support SQL portfolio analysis.

Created features:

* dti_group
* loan_income_group
* income_group
* loan_amount_group
* risk_segment

After feature engineering, the dataset had 32,576 rows and 34 columns.

Key results:

* Low DTI customers had an 11.08% default rate.
* Very High DTI customers had a 71.98% default rate.
* Low Risk customers had a 5.61% default rate.
* High Risk customers had a 46.82% default rate.

03. SQLite Database

The featured dataset was loaded into a SQLite database.

Main steps:

* Created a SQLite database named credit_risk.db.
* Stored the featured dataset in a SQL table named loans.
* Verified that the SQL table contained 32,576 rows.

04. SQL Portfolio Analysis

SQL queries were used to analyze default risk across multiple customer and loan segments.

Analysis areas:

* Portfolio overview
* Loan grade
* Loan intent
* Home ownership
* Previous default history
* DTI group
* Loan-to-income group
* Risk segment
* Risk segment by loan grade
* Loan intent ranking

SQL concepts used:

* Aggregation
* GROUP BY
* ORDER BY
* Common Table Expression (CTE)
* Window function with RANK()

05. Final Summary

A final summary file was created to collect the most important portfolio metrics, key findings, and business insights.

Key Findings

Overall Portfolio

* Total applicants: 32,576
* Default customers: 7,108
* Overall default rate: 21.82%
* Average loan amount: 9,589.12
* Average income: 65,882.14
* Average interest rate: 11.01%
* Average DTI: 0.3452

Loan Grade

Loan grade was a strong risk driver. Default rate increased as loan grade became worse:

* Grade A: 9.96%
* Grade B: 16.28%
* Grade C: 20.74%
* Grade D: 59.05%
* Grade E: 64.42%
* Grade F: 70.54%
* Grade G: 98.44%

DTI Group

Customers with higher debt-to-income ratio had much higher default risk:

* Low DTI: 11.08%
* Medium DTI: 15.00%
* High DTI: 33.87%
* Very High DTI: 71.98%

Loan-to-Income Group

Customers with higher loan-to-income ratio had higher default risk:

* Less than 10%: 11.73%
* 10–20%: 15.11%
* 20–30%: 21.95%
* 30–40%: 68.72%
* 40% or above: 74.20%

Risk Segment

The rule-based risk segmentation separated customer risk levels clearly:

* Low Risk: 8,407 customers, 5.61% default rate.
* Medium Risk: 12,306 customers, 8.79% default rate.
* High Risk: 11,863 customers, 46.82% default rate.

Loan Intent Ranking

Using SQL window function, loan intents were ranked by default risk:

1. Debt Consolidation: 28.59%
2. Medical: 26.70%
3. Home Improvement: 26.10%
4. Personal: 19.89%
5. Education: 17.22%
6. Venture: 14.82%

Business Recommendations

* Apply stricter review for High Risk customers.
* Monitor customers with Very High DTI and high loan-to-income ratio.
* Review lower loan grades more carefully, especially grades D to G.
* Pay closer attention to debt consolidation, medical, and home improvement loan purposes.
* Use risk segmentation to support credit policy, limit management, and portfolio monitoring.

SQL Output Files

SQL query results are saved in:

output/sql_results/

Main output files include:

* 01_portfolio_overview.csv
* 02_loan_grade_summary.csv
* 03_loan_intent_summary.csv
* 04_home_ownership_summary.csv
* 05_previous_default_summary.csv
* 06_dti_summary.csv
* 07_loan_income_summary.csv
* 08_risk_segment_summary.csv
* 09_segment_grade_summary.csv
* 10_loan_intent_ranking.csv

Project Files

File	Description
01_data_cleaning.py:	Load data, check data quality, clean missing values and outliers

02_feature_engineering.py:	Create risk groups and risk segment

03_create_database.py::	Create SQLite database and store data in SQL table

04_sql_analysis.py:	Run SQL portfolio analysis and export query results

05_final_summary.py: Export final summary and key findings

credit_risk_cleaned.csv: Cleaned dataset

credit_risk_featured.csv:	Dataset after feature engineering

final_summary.txt: Final summary of key results

output/sql_results/: SQL query output files

How to Run

Run the files in this order:

python 01_data_cleaning.py

python 02_feature_engineering.py

python 03_create_database.py

python 04_sql_analysis.py

python 05_final_summary.py

Conclusion

This project demonstrates how Python, SQLite, and SQL can be used to perform credit risk portfolio analysis.
The analysis identifies key default risk drivers such as loan grade, DTI, loan-to-income ratio, previous default history, and risk segment. These findings can support credit risk monitoring, policy review, and data-driven lending decisions.
