import os
import sqlite3
import pandas as pd


db_path = "output/credit_risk.db"
output_path = "output/final_summary.txt"

conn = sqlite3.connect(db_path)


def get_query(query):
    return pd.read_sql_query(query, conn)


overall = get_query("""
SELECT
    COUNT(*) AS total_applicants,
    SUM(loan_status) AS total_default,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(AVG(person_income), 2) AS avg_income,
    ROUND(AVG(loan_int_rate), 2) AS avg_interest_rate,
    ROUND(AVG(debt_to_income_ratio), 4) AS avg_dti
FROM loans;
""")

risk_segment = get_query("""
SELECT
    risk_segment,
    COUNT(*) AS customers,
    SUM(loan_status) AS default_customers,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate
FROM loans
GROUP BY risk_segment
ORDER BY default_rate DESC;
""")

dti_group = get_query("""
SELECT
    dti_group,
    COUNT(*) AS customers,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate
FROM loans
GROUP BY dti_group
ORDER BY default_rate;
""")

loan_income_group = get_query("""
SELECT
    loan_income_group,
    COUNT(*) AS customers,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate
FROM loans
GROUP BY loan_income_group
ORDER BY default_rate;
""")

loan_grade = get_query("""
SELECT
    loan_grade,
    COUNT(*) AS customers,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate
FROM loans
GROUP BY loan_grade
ORDER BY loan_grade;
""")

loan_intent_rank = get_query("""
WITH intent_risk AS (
    SELECT
        loan_intent,
        COUNT(*) AS customers,
        ROUND(AVG(loan_status) * 100, 2) AS default_rate
    FROM loans
    GROUP BY loan_intent
)

SELECT
    loan_intent,
    customers,
    default_rate,
    RANK() OVER (ORDER BY default_rate DESC) AS risk_rank
FROM intent_risk;
""")


os.makedirs("output", exist_ok=True)

with open(output_path, "w", encoding="utf-8") as file:
    file.write("Credit Risk Portfolio Analysis - Final Summary\n")
    file.write("=" * 60 + "\n\n")

    file.write("1. Overall Portfolio\n")
    file.write(overall.to_string(index=False))
    file.write("\n\n")

    file.write("2. Risk Segment Summary\n")
    file.write(risk_segment.to_string(index=False))
    file.write("\n\n")

    file.write("3. DTI Group Summary\n")
    file.write(dti_group.to_string(index=False))
    file.write("\n\n")

    file.write("4. Loan-to-Income Group Summary\n")
    file.write(loan_income_group.to_string(index=False))
    file.write("\n\n")

    file.write("5. Loan Grade Summary\n")
    file.write(loan_grade.to_string(index=False))
    file.write("\n\n")

    file.write("6. Loan Intent Ranking\n")
    file.write(loan_intent_rank.to_string(index=False))
    file.write("\n\n")

    file.write("Key Findings\n")
    file.write("- Overall default rate was 21.82%.\n")
    file.write("- High Risk customers had a 46.82% default rate, compared with 5.61% for Low Risk customers.\n")
    file.write("- Very High DTI customers had a 71.98% default rate.\n")
    file.write("- Customers with loan-to-income ratio >=40% had a 74.20% default rate.\n")
    file.write("- Loan grade G had the highest default rate at 98.44%.\n")
    file.write("- Debt consolidation had the highest default rate among loan intents at 28.59%.\n")

conn.close()

print("Saved final summary")
print(output_path)