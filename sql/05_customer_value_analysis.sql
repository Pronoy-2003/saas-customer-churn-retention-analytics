/*
============================================================
SaaS Customer Churn & Revenue Analytics
File: 05_customer_value_analysis.sql

Purpose:
- Measure historical customer lifetime value.
- Identify high-value customers.
- Compare customer value between active and churned customers.
- Analyze revenue contribution by subscription plan.
- Understand the relationship between customer value,
  tenure, and churn status.

Key Metrics:
- Lifetime Revenue
- Average Monthly Revenue
- Lifetime Months
- Customer Tenure
- Revenue Contribution by Plan
- Customer Value by Churn Status
============================================================
*/


-- ============================================================
-- REVENUE CONTRIBUTION BY PLAN
-- ============================================================

SELECT
    p.plan_name,
    COUNT(DISTINCT m.customer_id) AS customers,
    SUM(m.monthly_revenue) AS total_revenue,
    AVG(m.monthly_revenue) AS avg_monthly_revenue_per_customer,
    CAST(
        100.0 * SUM(m.monthly_revenue)
        / SUM(SUM(m.monthly_revenue)) OVER ()
        AS DECIMAL(10,2)
    ) AS revenue_share_percent

FROM dbo.fact_customer_monthly m

INNER JOIN dbo.dim_plan p
    ON m.plan_id = p.plan_id

GROUP BY
    p.plan_name

ORDER BY
    total_revenue DESC;


-- ============================================================
-- CUSTOMER LIFETIME VALUE (HISTORICAL)
-- ============================================================

WITH customer_value AS
(
    SELECT
        customer_id,

        COUNT(DISTINCT month) AS lifetime_months,

        SUM(monthly_revenue) AS lifetime_revenue,

        AVG(monthly_revenue) AS avg_monthly_revenue,

        MAX(tenure_months) AS final_tenure_months,

        MAX(churn_flag) AS churn_flag

    FROM dbo.fact_customer_monthly

    GROUP BY
        customer_id
)

SELECT
    customer_id,

    lifetime_months,

    lifetime_revenue,

    avg_monthly_revenue,

    final_tenure_months,

    CASE
        WHEN churn_flag = 1
            THEN 'Churned'
        ELSE 'Active'
    END AS customer_status

FROM customer_value

ORDER BY
    lifetime_revenue DESC;


-- ============================================================
-- CUSTOMER VALUE BY CHURN STATUS
-- ============================================================

WITH customer_value AS
(
    SELECT
        customer_id,

        SUM(monthly_revenue) AS lifetime_revenue,

        AVG(monthly_revenue) AS avg_monthly_revenue,

        MAX(tenure_months) AS final_tenure_months,

        MAX(churn_flag) AS churn_flag

    FROM dbo.fact_customer_monthly

    GROUP BY
        customer_id
)

SELECT
    CASE
        WHEN churn_flag = 1
            THEN 'Churned'
        ELSE 'Active'
    END AS customer_status,

    COUNT(*) AS customers,

    SUM(lifetime_revenue) AS total_lifetime_revenue,

    AVG(lifetime_revenue) AS avg_lifetime_revenue,

    AVG(avg_monthly_revenue) AS avg_monthly_revenue,

    AVG(final_tenure_months) AS avg_tenure_months

FROM customer_value

GROUP BY
    churn_flag

ORDER BY
    total_lifetime_revenue DESC;
