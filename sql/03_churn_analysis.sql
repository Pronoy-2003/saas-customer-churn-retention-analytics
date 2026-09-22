/*
============================================================
SaaS Customer Churn & Revenue Analytics
File: 03_churn_analysis.sql

Purpose:
- Measure overall customer churn.
- Identify churn patterns across subscription plans.
- Analyze churn by customer tenure.
- Analyze churn by acquisition channel.
- Segment customers based on value and churn risk.
- Identify customer groups requiring retention attention.

Key Metrics:
- Total Customers
- Churned Customers
- Churn Rate
- Churn by Plan
- Churn by Tenure
- Churn by Acquisition Channel
- Customer Risk Segments
============================================================
*/


-- ============================================================
-- OVERALL CUSTOMER CHURN RATE
-- ============================================================

SELECT
    COUNT(DISTINCT customer_id) AS total_customers,

    COUNT(DISTINCT CASE
        WHEN churn_flag = 1 THEN customer_id
    END) AS churned_customers,

    CAST(
        100.0 *
        COUNT(DISTINCT CASE
            WHEN churn_flag = 1 THEN customer_id
        END)
        / COUNT(DISTINCT customer_id)
        AS DECIMAL(10,2)
    ) AS churn_rate_percent

FROM dbo.fact_customer_monthly;


-- ============================================================
-- CHURN BY SUBSCRIPTION PLAN
-- ============================================================

SELECT
    p.plan_name,

    COUNT(DISTINCT m.customer_id) AS customers,

    COUNT(DISTINCT CASE
        WHEN m.churn_flag = 1 THEN m.customer_id
    END) AS churned_customers,

    CAST(
        100.0 *
        COUNT(DISTINCT CASE
            WHEN m.churn_flag = 1 THEN m.customer_id
        END)
        / COUNT(DISTINCT m.customer_id)
        AS DECIMAL(10,2)
    ) AS churn_rate_percent

FROM dbo.fact_customer_monthly m

INNER JOIN dbo.dim_plan p
    ON m.plan_id = p.plan_id

GROUP BY
    p.plan_name

ORDER BY
    churn_rate_percent DESC;


-- ============================================================
-- CHURN BY CUSTOMER TENURE
-- ============================================================

WITH customer_tenure AS
(
    SELECT
        customer_id,
        MAX(tenure_months) AS tenure_months,
        MAX(churn_flag) AS churn_flag
    FROM dbo.fact_customer_monthly
    GROUP BY customer_id
)

SELECT
    CASE
        WHEN tenure_months <= 3 THEN '0-3 Months'
        WHEN tenure_months <= 6 THEN '4-6 Months'
        WHEN tenure_months <= 12 THEN '7-12 Months'
        WHEN tenure_months <= 24 THEN '13-24 Months'
        ELSE '25+ Months'
    END AS tenure_group,

    COUNT(*) AS customers,

    SUM(churn_flag) AS churned_customers,

    CAST(
        100.0 * SUM(churn_flag) / COUNT(*)
        AS DECIMAL(10,2)
    ) AS churn_rate_percent

FROM customer_tenure

GROUP BY
    CASE
        WHEN tenure_months <= 3 THEN '0-3 Months'
        WHEN tenure_months <= 6 THEN '4-6 Months'
        WHEN tenure_months <= 12 THEN '7-12 Months'
        WHEN tenure_months <= 24 THEN '13-24 Months'
        ELSE '25+ Months'
    END

ORDER BY
    MIN(tenure_months);


-- ============================================================
-- CHURN BY CUSTOMER SEGMENT
-- ============================================================

WITH customer_metrics AS
(
    SELECT
        m.customer_id,
        SUM(m.monthly_revenue) AS total_revenue,
        MAX(m.churn_flag) AS churn_flag
    FROM dbo.fact_customer_monthly m
    GROUP BY m.customer_id
),

revenue_quartiles AS
(
    SELECT
        customer_id,
        total_revenue,
        churn_flag,
        NTILE(4) OVER (ORDER BY total_revenue) AS revenue_quartile
    FROM customer_metrics
)

SELECT
    CASE
        WHEN revenue_quartile = 4 AND churn_flag = 1
            THEN 'High Value - High Risk'

        WHEN revenue_quartile = 4 AND churn_flag = 0
            THEN 'High Value - Low Risk'

        WHEN revenue_quartile <= 3 AND churn_flag = 1
            THEN 'Low/Medium Value - High Risk'

        ELSE 'Low/Medium Value - Low Risk'
    END AS customer_segment,

    COUNT(*) AS customers,
    SUM(total_revenue) AS total_revenue,
    AVG(total_revenue) AS avg_customer_revenue
FROM revenue_quartiles
GROUP BY
    CASE
        WHEN revenue_quartile = 4 AND churn_flag = 1
            THEN 'High Value - High Risk'
        WHEN revenue_quartile = 4 AND churn_flag = 0
            THEN 'High Value - Low Risk'
        WHEN revenue_quartile <= 3 AND churn_flag = 1
            THEN 'Low/Medium Value - High Risk'
        ELSE 'Low/Medium Value - Low Risk'
    END
ORDER BY total_revenue DESC;


-- ============================================================
-- CHURN BY ACQUISITION CHANNEL
-- ============================================================

WITH customer_churn AS
(
    SELECT
        customer_id,
        MAX(churn_flag) AS churn_flag
    FROM dbo.fact_customer_monthly
    GROUP BY customer_id
)

SELECT
    c.acquisition_channel,

    COUNT(*) AS customers,

    SUM(cc.churn_flag) AS churned_customers,

    CAST(
        100.0 * SUM(cc.churn_flag) / COUNT(*)
        AS DECIMAL(10,2)
    ) AS churn_rate_percent

FROM dbo.dim_customer c

INNER JOIN customer_churn cc
    ON c.customer_id = cc.customer_id

GROUP BY
    c.acquisition_channel

ORDER BY
    churn_rate_percent ASC;


-- ============================================================
-- CHURN RATE BY CUSTOMER TENURE
-- ============================================================

SELECT
    tenure_months,

    COUNT(DISTINCT customer_id) AS customers,

    COUNT(DISTINCT
        CASE
            WHEN churn_flag = 1
            THEN customer_id
        END
    ) AS churned_customers,

    CAST(
        100.0 *
        COUNT(DISTINCT
            CASE
                WHEN churn_flag = 1
                THEN customer_id
            END
        )
        / COUNT(DISTINCT customer_id)
        AS DECIMAL(10,2)
    ) AS churn_rate_percent

FROM dbo.fact_customer_monthly

GROUP BY
    tenure_months

ORDER BY
    tenure_months;
