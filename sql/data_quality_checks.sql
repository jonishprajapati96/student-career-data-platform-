-- 1. Count raw rows
SELECT COUNT(*) AS raw_row_count
FROM raw_h1b_jobs;

-- 2. Count cleaned rows
SELECT COUNT(*) AS cleaned_row_count
FROM cleaned_h1b_jobs;

-- 3. Check missing employer names
SELECT COUNT(*) AS missing_employer_count
FROM cleaned_h1b_jobs
WHERE employer_name IS NULL OR employer_name = '';

-- 4. Check duplicate cleaned rows
SELECT
    employer_name,
    worksite_city,
    worksite_state,
    fiscal_year,
    COUNT(*) AS duplicate_count
FROM cleaned_h1b_jobs
GROUP BY employer_name, worksite_city, worksite_state, fiscal_year
HAVING COUNT(*) > 1;

-- 5. Check invalid state length
SELECT *
FROM cleaned_h1b_jobs
WHERE LENGTH(worksite_state) != 2
LIMIT 20;