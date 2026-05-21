import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# -----------------------------
# Database Connection
# -----------------------------

DATABASE_URL = "postgresql://admin:admin123@localhost:5432/student_career_db"
engine = create_engine(DATABASE_URL)

# -----------------------------
# Page Setup
# -----------------------------

st.set_page_config(
    page_title="H1B Sponsorship Analytics Dashboard",
    layout="wide"
)

st.title("H1B Sponsorship Analytics Dashboard")

st.write(
    "End-to-end analytics engineering project using Python ETL, PostgreSQL warehouse layers, SQL analytics, and Streamlit."
)

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Dashboard Filters")

states_df = pd.read_sql(
    """
    SELECT DISTINCT worksite_state
    FROM cleaned_h1b_jobs
    WHERE worksite_state IS NOT NULL
    ORDER BY worksite_state
    """,
    engine
)

years_df = pd.read_sql(
    """
    SELECT DISTINCT fiscal_year
    FROM cleaned_h1b_jobs
    WHERE fiscal_year IS NOT NULL
    ORDER BY fiscal_year
    """,
    engine
)

selected_state = st.sidebar.selectbox(
    "Select State",
    ["ALL"] + states_df["worksite_state"].tolist()
)

selected_year = st.sidebar.selectbox(
    "Select Fiscal Year",
    ["ALL"] + years_df["fiscal_year"].astype(str).tolist()
)

# -----------------------------
# Dynamic WHERE Conditions
# -----------------------------

where_conditions = []

if selected_state != "ALL":
    where_conditions.append(f"worksite_state = '{selected_state}'")

if selected_year != "ALL":
    where_conditions.append(f"fiscal_year = {selected_year}")

where_clause = ""

if where_conditions:
    where_clause = "WHERE " + " AND ".join(where_conditions)

# -----------------------------
# Load Dashboard Data
# -----------------------------

total_applications_df = pd.read_sql(
    f"""
    SELECT COUNT(*) AS total_applications
    FROM cleaned_h1b_jobs
    {where_clause}
    """,
    engine
)

top_companies = pd.read_sql(
    f"""
    SELECT
        employer_name,
        COUNT(*) AS total_applications
    FROM cleaned_h1b_jobs
    {where_clause}
    GROUP BY employer_name
    ORDER BY total_applications DESC
    LIMIT 10
    """,
    engine
)

state_summary = pd.read_sql(
    f"""
    SELECT
        worksite_state,
        COUNT(*) AS total_applications
    FROM cleaned_h1b_jobs
    {where_clause}
    GROUP BY worksite_state
    ORDER BY total_applications DESC
    LIMIT 10
    """,
    engine
)

yearly_trends = pd.read_sql(
    f"""
    SELECT
        fiscal_year,
        COUNT(*) AS total_applications
    FROM cleaned_h1b_jobs
    {where_clause}
    GROUP BY fiscal_year
    ORDER BY fiscal_year
    """,
    engine
)

# -----------------------------
# KPI Metrics
# -----------------------------

total_applications = int(total_applications_df.iloc[0]["total_applications"])

top_employer = (
    top_companies.iloc[0]["employer_name"]
    if not top_companies.empty
    else "N/A"
)

top_state = (
    state_summary.iloc[0]["worksite_state"]
    if not state_summary.empty
    else "N/A"
)

total_years = (
    yearly_trends["fiscal_year"].nunique()
    if not yearly_trends.empty
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Applications", total_applications)
col2.metric("Top Employer", top_employer)
col3.metric("Top State", top_state)
col4.metric("Fiscal Years", total_years)

# -----------------------------
# Top Companies Chart
# -----------------------------

st.subheader("Top 10 Sponsoring Companies")

if not top_companies.empty:
    top_companies["company_display"] = (
        top_companies["employer_name"]
        .astype(str)
        .str.slice(0, 25)
    )

    st.bar_chart(
        top_companies.set_index("company_display")["total_applications"]
    )

    st.dataframe(
        top_companies[["employer_name", "total_applications"]],
        use_container_width=True
    )
else:
    st.warning("No company data found for selected filters.")

# -----------------------------
# State Summary Chart
# -----------------------------

st.subheader("Top States by Applications")

if not state_summary.empty:
    st.bar_chart(
        state_summary.set_index("worksite_state")["total_applications"]
    )

    st.dataframe(
        state_summary,
        use_container_width=True
    )
else:
    st.warning("No state data found for selected filters.")

# -----------------------------
# Yearly Trend Chart
# -----------------------------

st.subheader("Applications by Fiscal Year")

if not yearly_trends.empty:
    st.line_chart(
        yearly_trends.set_index("fiscal_year")["total_applications"]
    )

    st.dataframe(
        yearly_trends,
        use_container_width=True
    )
else:
    st.warning("No yearly trend data found for selected filters.")

# -----------------------------
# Footer
# -----------------------------

st.markdown("---")

st.write(
    "Pipeline: DOL H1B/LCA data → Python ETL → PostgreSQL warehouse → cleaned/analytics layers → Streamlit dashboard."
)