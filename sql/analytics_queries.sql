-- Top 10 sponsoring companies
SELECT 
    employer_name, 
    COUNT(*) AS total_applications
FROM raw_h1b_jobs
GROUP BY employer_name
ORDER BY total_applications DESC
LIMIT 10;


-- Top 10 states by applications
SELECT 
    worksite_state,
    COUNT(*) AS total_applications
FROM raw_h1b_jobs
GROUP BY worksite_state
ORDER BY total_applications DESC
LIMIT 10;


-- Applications by fiscal year
SELECT 
    fiscal_year,
    COUNT(*) AS total_applications
FROM raw_h1b_jobs
GROUP BY fiscal_year
ORDER BY fiscal_year;


-- Texas companies
SELECT *
FROM raw_h1b_jobs
WHERE worksite_state = 'TX'
LIMIT 20;