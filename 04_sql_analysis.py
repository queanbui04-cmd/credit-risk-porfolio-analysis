import os
import sqlite3
import pandas as pd


db_path = "output/credit_risk.db"
output_folder = "output/sql_results"

os.makedirs(output_folder, exist_ok=True)

conn = sqlite3.connect(db_path)


# Run SQL and save result
def run_query(query, file_name):
    result = pd.read_sql_query(query, conn)
    result.to_csv(f"{output_folder}/{file_name}", index=False, encoding="utf-8-sig")
    print(result.to_string(index=False))
    print()
    return result


# 1. Portfolio overview
query_1 = """
SELECT
    COUNT(*) AS total_applicants,
    SUM(loan_status) AS total_default,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(AVG(person_income), 2) AS avg_income,
    ROUND(AVG(loan_int_rate), 2) AS avg_interest_rate,
    ROUND(AVG(debt_to_income_ratio), 4) AS avg_dti
FROM loans;
"""

run_query(query_1, "01_portfolio_overview.csv")


# 2. Default rate by loan grade
query_2 = """
SELECT
    loan_grade,
    COUNT(*) AS total_applicants,
    SUM(loan_status) AS total_default,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent,
    ROUND(AVG(loan_int_rate), 2) AS avg_interest_rate
FROM loans
GROUP BY loan_grade
ORDER BY loan_grade;
"""

run_query(query_2, "02_loan_grade_summary.csv")


# 3. Default rate by loan intent
query_3 = """
SELECT
    loan_intent,
    COUNT(*) AS total_applicants,
    SUM(loan_status) AS total_default,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount
FROM loans
GROUP BY loan_intent
ORDER BY default_rate_percent DESC;
"""

run_query(query_3, "03_loan_intent_summary.csv")


# 4. Default rate by home ownership
query_4 = """
SELECT
    person_home_ownership,
    COUNT(*) AS total_applicants,
    SUM(loan_status) AS total_default,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent,
    ROUND(AVG(person_income), 2) AS avg_income
FROM loans
GROUP BY person_home_ownership
ORDER BY default_rate_percent DESC;
"""

run_query(query_4, "04_home_ownership_summary.csv")


# 5. Default rate by previous default
query_5 = """
SELECT
    cb_person_default_on_file,
    COUNT(*) AS total_applicants,
    SUM(loan_status) AS total_default,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent
FROM loans
GROUP BY cb_person_default_on_file
ORDER BY default_rate_percent DESC;
"""

run_query(query_5, "05_previous_default_summary.csv")


# 6. Default rate by DTI group
query_6 = """
SELECT
    dti_group,
    COUNT(*) AS total_applicants,
    SUM(loan_status) AS total_default,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent,
    ROUND(AVG(debt_to_income_ratio), 4) AS avg_dti
FROM loans
GROUP BY dti_group
ORDER BY avg_dti;
"""

run_query(query_6, "06_dti_summary.csv")


# 7. Default rate by loan-to-income group
query_7 = """
SELECT
    loan_income_group,
    COUNT(*) AS total_applicants,
    SUM(loan_status) AS total_default,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent,
    ROUND(AVG(loan_percent_income), 4) AS avg_loan_percent_income
FROM loans
GROUP BY loan_income_group
ORDER BY avg_loan_percent_income;
"""

run_query(query_7, "07_loan_income_summary.csv")


# 8. Default rate by risk segment
query_8 = """
SELECT
    risk_segment,
    COUNT(*) AS total_applicants,
    SUM(loan_status) AS total_default,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(AVG(person_income), 2) AS avg_income,
    ROUND(AVG(debt_to_income_ratio), 4) AS avg_dti
FROM loans
GROUP BY risk_segment
ORDER BY default_rate_percent DESC;
"""

run_query(query_8, "08_risk_segment_summary.csv")


# 9. CTE: risk segment by loan grade
query_9 = """
WITH segment_grade_summary AS (
    SELECT
        risk_segment,
        loan_grade,
        COUNT(*) AS total_applicants,
        SUM(loan_status) AS total_default,
        ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent
    FROM loans
    GROUP BY risk_segment, loan_grade
)

SELECT
    *
FROM segment_grade_summary
ORDER BY default_rate_percent DESC;
"""

run_query(query_9, "09_segment_grade_summary.csv")


# 10. Window function: rank loan intent by default risk
query_10 = """
WITH intent_risk AS (
    SELECT
        loan_intent,
        COUNT(*) AS total_applicants,
        SUM(loan_status) AS total_default,
        ROUND(AVG(loan_status) * 100, 2) AS default_rate_percent
    FROM loans
    GROUP BY loan_intent
)

SELECT
    loan_intent,
    total_applicants,
    total_default,
    default_rate_percent,
    RANK() OVER (ORDER BY default_rate_percent DESC) AS risk_rank
FROM intent_risk;
"""

run_query(query_10, "10_loan_intent_ranking.csv")


conn.close()

print("SQL analysis completed")