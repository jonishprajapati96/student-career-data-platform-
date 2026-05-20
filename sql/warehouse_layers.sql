-- Rebuild warehouse layers safely
DROP TABLE IF EXISTS analytics_yearly_trends;
DROP TABLE IF EXISTS analytics_state_summary;
DROP TABLE IF EXISTS analytics_top_companies;
DROP TABLE IF EXISTS cleaned_h1b_jobs;


-- Cleaned layer with deduplication
CREATE TABLE cleaned_h1b_jobs AS
SELECT DISTINCT
    TRIM(employer_name) AS employer_name,
    TRIM(worksite_city) AS worksite_city,
    UPPER(TRIM(worksite_state)) AS worksite_state,
    fiscal_year
FROM raw_h1b_jobs
WHERE employer_name IS NOT NULL;


-- Top companies analytics table
CREATE TABLE analytics_top_companies AS
SELECT
    employer_name,
    COUNT(*) AS total_applications
FROM cleaned_h1b_jobs
GROUP BY employer_name
ORDER BY total_applications DESC;


-- State summary analytics table
CREATE TABLE analytics_state_summary AS
SELECT
    worksite_state,
    COUNT(*) AS total_applications
FROM cleaned_h1b_jobs
GROUP BY worksite_state
ORDER BY total_applications DESC;


-- Yearly trend analytics table
CREATE TABLE analytics_yearly_trends AS
SELECT
    fiscal_year,
    COUNT(*) AS total_applications
FROM cleaned_h1b_jobs
GROUP BY fiscal_year
ORDER BY fiscal_year;

-- Indexes
CREATE INDEX idx_worksite_state
ON cleaned_h1b_jobs(worksite_state);

CREATE INDEX idx_employer_name
ON cleaned_h1b_jobs(employer_name);