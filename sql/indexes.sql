-- Index for faster state filtering
CREATE INDEX IF NOT EXISTS idx_cleaned_h1b_state
ON cleaned_h1b_jobs(worksite_state);

-- Index for faster employer search/grouping
CREATE INDEX IF NOT EXISTS idx_cleaned_h1b_employer
ON cleaned_h1b_jobs(employer_name);

-- Index for faster year filtering
CREATE INDEX IF NOT EXISTS idx_cleaned_h1b_year
ON cleaned_h1b_jobs(fiscal_year);