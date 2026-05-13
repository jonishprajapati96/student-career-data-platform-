CREATE TABLE raw_h1b_jobs (
    id SERIAL PRIMARY KEY,
    employer_name TEXT,
    job_title TEXT,
    worksite_city TEXT,
    worksite_state TEXT,
    wage_rate NUMERIC,
    case_status TEXT,
    fiscal_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);