
import os
import numpy as np
import pandas as pd


# Load cleaned data
input_path = "output/credit_risk_cleaned.csv"
output_path = "output/credit_risk_featured.csv"

df = pd.read_csv(input_path)


# Create customer groups
df["dti_group"] = pd.cut(
    df["debt_to_income_ratio"],
    bins=[-np.inf, 0.2, 0.4, 0.6, np.inf],
    labels=["Low DTI", "Medium DTI", "High DTI", "Very High DTI"]
)

df["loan_income_group"] = pd.cut(
    df["loan_percent_income"],
    bins=[-np.inf, 0.1, 0.2, 0.3, 0.4, np.inf],
    labels=["<10%", "10-20%", "20-30%", "30-40%", ">=40%"]
)

df["income_group"] = pd.cut(
    df["person_income"],
    bins=[-np.inf, 30000, 60000, 100000, np.inf],
    labels=["Low Income", "Medium Income", "High Income", "Very High Income"]
)

df["loan_amount_group"] = pd.cut(
    df["loan_amnt"],
    bins=[-np.inf, 5000, 10000, 20000, np.inf],
    labels=["Small Loan", "Medium Loan", "Large Loan", "Very Large Loan"]
)


# Create risk segment
def assign_risk_segment(row):
    if (
        row["loan_grade"] in ["A", "B"]
        and row["debt_to_income_ratio"] < 0.3
        and row["loan_percent_income"] < 0.2
        and row["cb_person_default_on_file"] == "N"
    ):
        return "Low Risk"

    if (
        row["loan_grade"] in ["D", "E", "F", "G"]
        or row["debt_to_income_ratio"] >= 0.5
        or row["loan_percent_income"] >= 0.3
        or row["cb_person_default_on_file"] == "Y"
    ):
        return "High Risk"

    return "Medium Risk"


df["risk_segment"] = df.apply(assign_risk_segment, axis=1)


# Feature check
print(df.shape)

print(df["dti_group"].value_counts())
print(df["loan_income_group"].value_counts())
print(df["income_group"].value_counts())
print(df["loan_amount_group"].value_counts())
print(df["risk_segment"].value_counts())

print(round(df.groupby("dti_group", observed=False)["loan_status"].mean() * 100, 2))
print(round(df.groupby("loan_income_group", observed=False)["loan_status"].mean() * 100, 2))
print(round(df.groupby("risk_segment")["loan_status"].mean() * 100, 2))


# Save featured data
os.makedirs("output", exist_ok=True)

df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(df.shape)
print("Saved featured data")