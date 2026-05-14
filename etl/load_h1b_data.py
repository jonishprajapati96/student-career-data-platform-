import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
DATABASE_URL = "postgresql://admin:admin123@localhost:5432/student_career_db"

engine = create_engine(DATABASE_URL)

# Read DOL dataset
df = pd.read_csv(
    "data/raw/lca_fy2025.csv",
    sep="\t",
    encoding="utf-16"
)

df.columns = df.columns.str.strip()
print("the columns are:", df.columns.tolist())  # Print columns to verify
# Rename columns
df = df.rename(columns={
    "Employer (Petitioner) Name": "employer_name",
    "Petitioner City": "worksite_city",
    "Petitioner State": "worksite_state",
    "Fiscal Year": "fiscal_year"
})

# Select only needed columns
df = df[
    [
        "employer_name",
        "worksite_city",
        "worksite_state",
        "fiscal_year"
    ]
]

# Remove missing employers
df = df.dropna(subset=["employer_name"])

# Load into PostgreSQL
df.to_sql(
    "raw_h1b_jobs",
    engine,
    if_exists="append",
    index=False
)

print("Data loaded successfully!")