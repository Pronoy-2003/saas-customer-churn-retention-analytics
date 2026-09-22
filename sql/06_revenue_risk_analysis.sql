/*
============================================================
SaaS Customer Churn & Revenue Analytics
File: 06_revenue_risk_analysis.sql

Purpose:
- Quantify revenue associated with customer churn.
- Estimate revenue at risk across acquisition channels.
- Analyze churned revenue by subscription plan.
- Evaluate payment performance and potential revenue leakage.
- Identify areas where revenue retention efforts should be
  prioritized.

Key Metrics:
- Churned Monthly Revenue
- Churned Annual Revenue
- Revenue at Risk
- Revenue at Risk by Acquisition Channel
- Churned Revenue by Plan
- Payment Performance
- Refunded Amount
============================================================
*/


-- ============================================================
-- REVENUE ASSOCIATED WITH CHURN
-- ============================================================


SELECT
    SUM(monthly_revenue) AS churned_monthly_revenue,
    SUM(monthly_revenue) * 12 AS churned_annual_revenue
FROM dbo.fact_customer_monthly
WHERE churn_flag = 1;

SELECT
    p.plan_name,
    COUNT(DISTINCT m.customer_id) AS churned_customers,
    SUM(m.monthly_revenue) AS churned_monthly_revenue,
    SUM(m.monthly_revenue) * 12 AS churned_annual_revenue
FROM dbo.fact_customer_monthly m
INNER JOIN dbo.dim_plan p
    ON m.plan_id = p.plan_id
WHERE m.churn_flag = 1
GROUP BY p.plan_name
ORDER BY churned_monthly_revenue DESC;


-- ============================================================
-- REVENUE AT RISK BY ACQUISITION CHANNEL
-- ============================================================

WITH channel_revenue AS
(
    SELECT
        c.acquisition_channel,
        SUM(m.monthly_revenue) AS total_monthly_revenue,

        SUM(
            CASE
                WHEN m.churn_flag = 1
                THEN m.monthly_revenue
                ELSE 0
            END
        ) AS churned_monthly_revenue,

        COUNT(DISTINCT m.customer_id) AS customers,

        COUNT(DISTINCT
            CASE
                WHEN m.churn_flag = 1
                THEN m.customer_id
            END
        ) AS churned_customers

    FROM dbo.fact_customer_monthly m

    INNER JOIN dbo.dim_customer c
        ON m.customer_id = c.customer_id

    GROUP BY
        c.acquisition_channel
)

SELECT
    acquisition_channel,
    customers,
    churned_customers,

    CAST(
        100.0 * churned_customers / customers
        AS DECIMAL(10,2)
    ) AS churn_rate_percent,

    total_monthly_revenue,
    churned_monthly_revenue,

    CAST(
        100.0 * churned_monthly_revenue
        / NULLIF(total_monthly_revenue, 0)
        AS DECIMAL(10,2)
    ) AS revenue_at_risk_percent

FROM channel_revenue

ORDER BY
    churned_monthly_revenue DESC;


-- ============================================================
-- PAYMENT PERFORMANCE BY STATUS
-- ============================================================

SELECT
    payment_status,

    COUNT(*) AS payment_records,

    SUM(
        CASE
            WHEN amount > 0
            THEN amount
            ELSE 0
        END
    ) AS positive_payment_amount,

    SUM(
        CASE
            WHEN amount < 0
            THEN ABS(amount)
            ELSE 0
        END
    ) AS refunded_amount,

    AVG(
        CASE
            WHEN amount > 0
            THEN amount
        END
    ) AS avg_positive_payment

FROM dbo.fact_payment

GROUP BY
    payment_status

ORDER BY
    payment_records DESC;
