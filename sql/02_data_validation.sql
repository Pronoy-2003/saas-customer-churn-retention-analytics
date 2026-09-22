/*
============================================================
SaaS Customer Churn & Revenue Analytics
File: 02_data_validation.sql

Purpose:
- Validate data quality after loading data into SQL Server.
- Check duplicate records.
- Check missing and NULL values.
- Identify invalid numerical values.
- Validate churn flags and subscription dates.
- Validate payment amounts and payment status.
- Identify potential data quality issues before analysis.

Validation Areas:
- Duplicate records
- Missing values
- Numerical values
- Churn flags
- Subscription dates
- Payment data
============================================================
*/


-- ============================================================
-- 1. DUPLICATE RECORD CHECKS
-- ============================================================

-- Check duplicate customers
SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM dbo.dim_customer
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- Check duplicate subscriptions
SELECT
    subscription_id,
    COUNT(*) AS duplicate_count
FROM dbo.fact_subscription
GROUP BY subscription_id
HAVING COUNT(*) > 1;

-- Check duplicate customer-month records
SELECT
    customer_id,
    [month],
    COUNT(*) AS duplicate_count
FROM dbo.fact_customer_monthly
GROUP BY
    customer_id,
    [month]
HAVING COUNT(*) > 1;


-- ============================================================
-- 2. MISSING VALUE CHECKS
-- ============================================================

-- customer NULL checks
SELECT
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN signup_date IS NULL THEN 1 ELSE 0 END) AS null_signup_date,
    SUM(CASE WHEN acquisition_channel IS NULL THEN 1 ELSE 0 END) AS null_acquisition_channel
FROM dbo.dim_customer;

-- subscription NULL checks
SELECT
    SUM(CASE WHEN subscription_id IS NULL THEN 1 ELSE 0 END) AS null_subscription_id,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN plan_id IS NULL THEN 1 ELSE 0 END) AS null_plan_id,
    SUM(CASE WHEN start_date IS NULL THEN 1 ELSE 0 END) AS null_start_date
FROM dbo.fact_subscription;

-- monthly data NULL checks
SELECT
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN [month] IS NULL THEN 1 ELSE 0 END) AS null_month,
    SUM(CASE WHEN monthly_revenue IS NULL THEN 1 ELSE 0 END) AS null_revenue,
    SUM(CASE WHEN tenure_months IS NULL THEN 1 ELSE 0 END) AS null_tenure,
    SUM(CASE WHEN churn_flag IS NULL THEN 1 ELSE 0 END) AS null_churn_flag
FROM dbo.fact_customer_monthly;


-- ============================================================
-- 3. INVALID NUMERICAL VALUE CHECKS
-- ============================================================

-- revenue
SELECT COUNT(*) AS invalid_revenue_records
FROM dbo.fact_customer_monthly
WHERE monthly_revenue < 0;

-- tenure
SELECT COUNT(*) AS invalid_tenure_records
FROM dbo.fact_customer_monthly
WHERE tenure_months < 0;

-- feature adoption
SELECT COUNT(*) AS invalid_adoption_records
FROM dbo.fact_customer_monthly
WHERE feature_adoption_rate < 0
   OR feature_adoption_rate > 1;

-- login frequency
SELECT COUNT(*) AS invalid_login_records
FROM dbo.fact_customer_monthly
WHERE login_frequency < 0;

-- support tickets
SELECT COUNT(*) AS invalid_support_records
FROM dbo.fact_customer_monthly
WHERE support_tickets < 0;

-- payment failures
SELECT COUNT(*) AS invalid_payment_failure_records
FROM dbo.fact_customer_monthly
WHERE payment_failures < 0;


-- ============================================================
-- 4. CHURN FLAG VALIDATION
-- ============================================================

-- churn_flag distribution
SELECT
    churn_flag,
    COUNT(*) AS records
FROM dbo.fact_customer_monthly
GROUP BY churn_flag
ORDER BY churn_flag;


-- ============================================================
-- 5. SUBSCRIPTION DATE VALIDATION
-- ============================================================

-- invalid start/end dates
SELECT COUNT(*) AS invalid_date_records
FROM dbo.fact_subscription
WHERE end_date IS NOT NULL
  AND start_date > end_date;


-- ============================================================
-- 6. PAYMENT DATA VALIDATION
-- ============================================================

-- negative payment amounts
SELECT COUNT(*) AS invalid_payment_amounts
FROM dbo.fact_payment
WHERE amount < 0;

-- payment status analysis
-- negative payment records
SELECT
    payment_status,
    COUNT(*) AS records,
    SUM(CASE WHEN amount < 0 THEN 1 ELSE 0 END) AS negative_amounts,
    MIN(amount) AS minimum_amount,
    MAX(amount) AS maximum_amount
FROM dbo.fact_payment
GROUP BY payment_status
ORDER BY payment_status;

