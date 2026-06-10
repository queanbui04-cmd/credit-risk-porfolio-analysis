import os
import sqlite3
import pandas as pd


# Load featured data
csv_path = "output/credit_risk_featured.csv"
db_path = "output/credit_risk.db"

df = pd.read_csv(csv_path)

os.makedirs("output", exist_ok=True)


# Create database
conn = sqlite3.connect(db_path)

df.to_sql("loans", conn, if_exists="replace", index=False)


# Check database
row_count = pd.read_sql_query(
    "SELECT COUNT(*) AS total_rows FROM loans",
    conn
)

risk_summary = pd.read_sql_query(
    """
    SELECT
        risk_segment,
        COUNT(*) AS customers,
        ROUND(AVG(loan_status) * 100, 2) AS default_rate
    FROM loans
    GROUP BY risk_segment
    ORDER BY default_rate DESC
    """,
    conn
)

print(row_count)
print(risk_summary)

conn.close()

print("Saved database")
print(df.shape)