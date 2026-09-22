# Data Dictionary

This document describes the main tables and important fields used in the **SaaS Customer Churn & Retention Analytics** project.

## 1. dim_customer

Customer master table containing customer and company information.

| Column | Description |
|---|---|
| `customer_id` | Unique identifier for each customer |
| `company_name` | Customer/company name |
| `signup_date` | Date when the customer signed up |
| `country` | Customer's country |
| `industry` | Customer's industry |
| `company_size` | Size category of the customer company |
| `acquisition_channel` | Channel through which the customer was acquired |
| `sales_region` | Sales region associated with the customer |

## 2. dim_plan

Subscription plan master table containing pricing information.

| Column | Description |
|---|---|
| `plan_id` | Unique identifier for each subscription plan |
| `plan_name` | Name of the subscription plan |
| `monthly_price` | Monthly subscription price in USD |
| `annual_price` | Annual subscription price in USD |

## 3. fact_subscription

Subscription-level table containing customer subscription history.

| Column | Description |
|---|---|
| `subscription_id` | Unique identifier for each subscription |
| `customer_id` | Customer associated with the subscription |
| `plan_id` | Subscription plan |
| `start_date` | Subscription start date |
| `end_date` | Subscription end date, if applicable |
| `billing_cycle` | Billing frequency |
| `monthly_price` | Monthly subscription price in USD |
| `subscription_status` | Current subscription status |

## 4. fact_customer_monthly

Monthly customer-level fact table used for churn, retention, revenue, and customer behavior analysis.

| Column | Description |
|---|---|
| `customer_id` | Customer associated with the monthly record |
| `month` | Reporting month |
| `plan_id` | Subscription plan during the month |
| `active_flag` | Indicates whether the customer was active |
| `monthly_revenue` | Revenue generated during the month in USD |
| `tenure_months` | Customer tenure in months |
| `login_frequency` | Number of customer logins during the month |
| `feature_adoption_rate` | Rate of feature adoption |
| `support_tickets` | Number of support tickets raised |
| `payment_failures` | Number of failed payments |
| `churn_flag` | Indicates whether the customer churned |

## 5. fact_payment

Payment-level fact table containing customer payment transactions.

| Column | Description |
|---|---|
| `payment_id` | Unique identifier for each payment |
| `customer_id` | Customer associated with the payment |
| `payment_date` | Date of payment |
| `amount` | Payment amount in USD |
| `payment_status` | Payment status |
| `payment_method` | Payment method used |

## Key Relationships

```text
dim_customer
     │
     ├─────────────── fact_subscription
     ├─────────────── fact_customer_monthly
     └─────────────── fact_payment

dim_plan
     │
     ├─────────────── fact_subscription
     └─────────────── fact_customer_monthly
```

## Primary Keys

- `dim_customer` → `customer_id`
- `dim_plan` → `plan_id`
- `fact_subscription` → `subscription_id`
- `fact_customer_monthly` → `customer_id + month`
- `fact_payment` → `payment_id`

## Main Analytical Fields

- **Churn:** `churn_flag`
- **Revenue:** `monthly_revenue`, `amount`
- **Retention:** `active_flag`
- **Customer Tenure:** `tenure_months`
- **Customer Behavior:** `login_frequency`, `feature_adoption_rate`
- **Customer Risk:** `payment_failures`, `support_tickets`
- **Customer Segmentation:** `plan_id`, `acquisition_channel`, `industry`, `company_size`
