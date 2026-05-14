import pandas as pd

file_path = "data/raw/lca_fy2025.csv"

df = pd.read_csv(
    file_path,
    sep="\t",
    encoding="utf-16",
    nrows=5
)

print("Columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())