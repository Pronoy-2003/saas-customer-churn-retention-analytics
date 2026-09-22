/*
============================================================
SaaS Customer Churn & Revenue Analytics
File: 04_retention_analysis.sql

Purpose:
- Analyze customer retention over time.
- Create customer acquisition cohorts.
- Measure active customers by cohort and month.
- Calculate retention rates by months since acquisition.
- Support cohort retention analysis for the Power BI dashboard.

Key Metrics:
- Cohort Month
- Cohort Customers
- Active Customers
- Months Since Cohort
- Retention Rate
============================================================
*/


-- ============================================================
-- COHORT RETENTION ANALYSIS
-- ============================================================

WITH customer_cohort AS
(
    -- Identify each customer's first month
    SELECT
        customer_id,
        MIN(month) AS cohort_month
    FROM dbo.fact_customer_monthly
    GROUP BY
        customer_id
),

cohort_activity AS
(
    SELECT
        c.cohort_month,
        m.month,

        DATEDIFF(
            MONTH,
            c.cohort_month,
            m.month
        ) AS months_since_cohort,

        COUNT(DISTINCT m.customer_id) AS active_customers

    FROM dbo.fact_customer_monthly m

    INNER JOIN customer_cohort c
        ON m.customer_id = c.customer_id

    WHERE
        m.active_flag = 1

    GROUP BY
        c.cohort_month,
        m.month
),

cohort_size AS
(
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_customers

    FROM customer_cohort

    GROUP BY
        cohort_month
)

SELECT
    a.cohort_month,

    a.months_since_cohort,

    s.cohort_customers,

    a.active_customers,

    CAST(
        100.0 * a.active_customers
        / NULLIF(s.cohort_customers, 0)
        AS DECIMAL(10,2)
    ) AS retention_rate_percent

FROM cohort_activity a

INNER JOIN cohort_size s
    ON a.cohort_month = s.cohort_month

ORDER BY
    a.cohort_month,
    a.months_since_cohort;
