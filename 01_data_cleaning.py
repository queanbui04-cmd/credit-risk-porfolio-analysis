import os
import numpy as np
import pandas as pd


# Load data
file_path = "data/Credit Risk Dataset.xlsx"
output_path = "output/credit_risk_cleaned.csv"

df = pd.read_excel(file_path, header=0)
df.columns = df.columns.str.strip()


# Basic data check
target = "loan_status"

print(df.shape)
print(df.head())
print(df.columns)

print(df[target].value_counts())
print(round(df[target].mean() * 100, 2))

print(df.isna().sum())
print(df.duplicated().sum())
print(df.describe())


# Categorical check
print(df["person_home_ownership"].value_counts())
print(df["loan_intent"].value_counts())
print(df["loan_grade"].value_counts())
print(df["cb_person_default_on_file"].value_counts())


# Outlier check
age_outliers = df[df["person_age"] > 100]
emp_age_outliers = df[df["person_emp_length"] > df["person_age"]]
emp_60_outliers = df[df["person_emp_length"] > 60]

print(len(age_outliers))
print(len(emp_age_outliers))
print(len(emp_60_outliers))


# Data cleaning
rows_before = len(df)

df_clean = df[df["person_age"] <= 100].copy()

invalid_emp = (
    (df_clean["person_emp_length"] > df_clean["person_age"]) |
    (df_clean["person_emp_length"] > 60)
)

df_clean.loc[invalid_emp, "person_emp_length"] = np.nan

df_clean["loan_int_rate"] = df_clean.groupby("loan_grade")["loan_int_rate"].transform(
    lambda x: x.fillna(x.median())
)

df_clean["loan_int_rate"] = df_clean["loan_int_rate"].fillna(
    df_clean["loan_int_rate"].median()
)

df_clean["person_emp_length"] = df_clean["person_emp_length"].fillna(
    df_clean["person_emp_length"].median()
)

rows_after = len(df_clean)


# Final check
print(rows_before)
print(rows_after)
print(rows_before - rows_after)

print(df_clean.isna().sum())
print(df_clean.duplicated().sum())
print(round(df_clean[target].mean() * 100, 2))


# Save cleaned data
os.makedirs("output", exist_ok=True)

df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")

print(df_clean.shape)
print("Saved cleaned data")