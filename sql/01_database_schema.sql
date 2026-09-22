/*
============================================================
SaaS Customer Churn & Revenue Analytics
File: 01_database_schema.sql

Purpose:
- Create the SaaS_Churn_Analytics database.
- Create dimension and fact tables.
- Define primary keys and foreign key relationships.
- Create analytical indexes for query performance.
- Load raw CSV datasets into the SQL Server tables.

Tables:
- dim_customer
- dim_plan
- fact_subscription
- fact_customer_monthly
- fact_payment
============================================================
*/


-- ============================================================
-- 1. DATABASE CREATION
-- ============================================================

-- Database Creation
CREATE DATABASE SaaS_Churn_Analytics;
GO

-- Using the database
USE SaaS_Churn_Analytics;
GO

-- ============================================================
-- 2. CUSTOMER DIMENSION TABLE
-- ============================================================

CREATE TABLE dbo.dim_customer
(
    customer_id VARCHAR(20) NOT NULL,
    company_name VARCHAR(150) NOT NULL,
    signup_date DATE NOT NULL,
    country VARCHAR(50),
    industry VARCHAR(100),
    company_size VARCHAR(30),
    acquisition_channel VARCHAR(50),
    sales_region VARCHAR(50),

    CONSTRAINT PK_dim_customer
        PRIMARY KEY (customer_id)
);
GO

-- ============================================================
-- 3. PLAN DIMENSION TABLE
-- ============================================================

CREATE TABLE dbo.dim_plan
(
    plan_id VARCHAR(10) NOT NULL,
    plan_name VARCHAR(50) NOT NULL,
    monthly_price DECIMAL(10,2) NOT NULL,
    annual_price DECIMAL(10,2) NOT NULL,

    CONSTRAINT PK_dim_plan
        PRIMARY KEY (plan_id)
);
GO


-- ============================================================
-- 4. SUBSCRIPTION FACT TABLE
-- ============================================================

CREATE TABLE dbo.fact_subscription
(
    subscription_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    plan_id VARCHAR(10) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    billing_cycle VARCHAR(20),
    monthly_price DECIMAL(10,2),
    subscription_status VARCHAR(30),

    CONSTRAINT PK_fact_subscription
        PRIMARY KEY (subscription_id),

    CONSTRAINT FK_subscription_customer
        FOREIGN KEY (customer_id)
        REFERENCES dbo.dim_customer(customer_id),

    CONSTRAINT FK_subscription_plan
        FOREIGN KEY (plan_id)
        REFERENCES dbo.dim_plan(plan_id)
);
GO

-- ============================================================
-- 5. CUSTOMER MONTHLY FACT TABLE
-- ============================================================

CREATE TABLE dbo.fact_customer_monthly
(
    customer_id VARCHAR(20) NOT NULL,
    [month] DATE NOT NULL,
    plan_id VARCHAR(10) NULL,
    active_flag INT NOT NULL,
    monthly_revenue DECIMAL(10,2) NOT NULL,
    tenure_months INT NOT NULL,
    login_frequency INT NOT NULL,
    feature_adoption_rate DECIMAL(5,2) NOT NULL,
    support_tickets INT NOT NULL,
    payment_failures INT NOT NULL,
    churn_flag INT NOT NULL,

    CONSTRAINT PK_fact_customer_monthly
        PRIMARY KEY (customer_id, [month]),

    CONSTRAINT FK_monthly_customer
        FOREIGN KEY (customer_id)
        REFERENCES dbo.dim_customer(customer_id),

    CONSTRAINT FK_monthly_plan
        FOREIGN KEY (plan_id)
        REFERENCES dbo.dim_plan(plan_id)
);
GO


-- ============================================================
-- 6. PAYMENT FACT TABLE
-- ============================================================

CREATE TABLE dbo.fact_payment
(
    payment_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_status VARCHAR(30),
    payment_method VARCHAR(30),

    CONSTRAINT PK_fact_payment
        PRIMARY KEY (payment_id),

    CONSTRAINT FK_payment_customer
        FOREIGN KEY (customer_id)
        REFERENCES dbo.dim_customer(customer_id)
);
GO

-- ============================================================
-- 7. ANALYTICAL INDEXES
-- ============================================================

CREATE INDEX IX_subscription_customer
ON dbo.fact_subscription(customer_id);
GO

CREATE INDEX IX_subscription_plan
ON dbo.fact_subscription(plan_id);
GO

CREATE INDEX IX_monthly_customer
ON dbo.fact_customer_monthly(customer_id);
GO

CREATE INDEX IX_monthly_month
ON dbo.fact_customer_monthly([month]);
GO

CREATE INDEX IX_monthly_plan
ON dbo.fact_customer_monthly(plan_id);
GO

CREATE INDEX IX_monthly_churn
ON dbo.fact_customer_monthly(churn_flag);
GO

CREATE INDEX IX_payment_customer
ON dbo.fact_payment(customer_id);
GO

-- ============================================================
-- 8. DATA LOADING
-- ============================================================

-- Import dim_customer.csv
BULK INSERT dbo.dim_customer
FROM 'D:\Pronoy Sonowal\Portfolio Projects\saas-customer-churn-analysis\data\raw\dim_customer.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    TABLOCK
);
GO

-- Import dim_plan.csv
BULK INSERT dbo.dim_plan
FROM 'D:\Pronoy Sonowal\Portfolio Projects\saas-customer-churn-analysis\data\raw\dim_plan.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    TABLOCK
);
GO

-- Import fact_subscription.csv
BULK INSERT dbo.fact_subscription
FROM 'D:\Pronoy Sonowal\Portfolio Projects\saas-customer-churn-analysis\data\raw\fact_subscription.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    TABLOCK
);
GO

-- Import fact_customer_monthly.csv
BULK INSERT dbo.fact_customer_monthly
FROM 'D:\Pronoy Sonowal\Portfolio Projects\saas-customer-churn-analysis\data\raw\fact_customer_monthly.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    TABLOCK
);
GO

-- Import fact_payment.csv
BULK INSERT dbo.fact_payment
FROM 'D:\Pronoy Sonowal\Portfolio Projects\saas-customer-churn-analysis\data\raw\fact_payment.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    TABLOCK
);
GO
