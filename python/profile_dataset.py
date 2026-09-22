"""
============================================================
SaaS Customer Churn & Retention Analytics
File: profile_dataset.py
============================================================

Purpose:
    Profile and validate the synthetic CloudFlow SaaS
    datasets before they are loaded into SQL Server.

The script performs:

    - Dataset size and structure checks
    - Duplicate record checks
    - Missing-value analysis
    - Customer profile analysis
    - Subscription and plan analysis
    - Churn analysis
    - Tenure analysis
    - Acquisition-channel analysis
    - Monthly revenue analysis
    - Revenue-at-risk analysis
    - Customer engagement analysis
    - Payment analysis
    - Cohort analysis
    - Data-quality validation

IMPORTANT:
    This script only reads and analyzes the CSV files.
    It does NOT modify the source datasets.

The output is used to verify that the generated data
is suitable for SQL Server analysis and Power BI reporting.
============================================================
"""

from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "raw"

CUSTOMER_FILE = DATA_DIR / "dim_customer.csv"
PLAN_FILE = DATA_DIR / "dim_plan.csv"
SUBSCRIPTION_FILE = DATA_DIR / "fact_subscription.csv"
MONTHLY_FILE = DATA_DIR / "fact_customer_monthly.csv"
PAYMENT_FILE = DATA_DIR / "fact_payment.csv"


# ============================================================
# 2. LOAD DATA
# ============================================================

def load_data():

    print("=" * 70)
    print("LOADING DATA")
    print("=" * 70)

    customers = pd.read_csv(
        CUSTOMER_FILE,
        parse_dates=["signup_date"]
    )

    plans = pd.read_csv(
        PLAN_FILE
    )

    subscriptions = pd.read_csv(
        SUBSCRIPTION_FILE,
        parse_dates=["start_date", "end_date"]
    )

    monthly = pd.read_csv(
        MONTHLY_FILE,
        parse_dates=["month"]
    )

    payments = pd.read_csv(
        PAYMENT_FILE,
        parse_dates=["payment_date"]
    )

    print(f"Customers:      {len(customers):,}")
    print(f"Plans:          {len(plans):,}")
    print(f"Subscriptions:  {len(subscriptions):,}")
    print(f"Monthly:        {len(monthly):,}")
    print(f"Payments:       {len(payments):,}")

    return (
        customers,
        plans,
        subscriptions,
        monthly,
        payments
    )


# ============================================================
# 3. BASIC TABLE INFORMATION
# ============================================================

def basic_information(
    customers,
    plans,
    subscriptions,
    monthly,
    payments
):

    print("\n" + "=" * 70)
    print("BASIC DATASET INFORMATION")
    print("=" * 70)

    datasets = {
        "dim_customer": customers,
        "dim_plan": plans,
        "fact_subscription": subscriptions,
        "fact_customer_monthly": monthly,
        "fact_payment": payments
    }

    for name, df in datasets.items():

        print(f"\n{name}")
        print("-" * 50)

        print(
            f"Rows: {len(df):,}"
        )

        print(
            f"Columns: {len(df.columns)}"
        )

        print(
            "Memory:",
            f"{df.memory_usage(deep=True).sum() / (1024**2):.2f} MB"
        )

        print(
            "Duplicate rows:",
            df.duplicated().sum()
        )


# ============================================================
# 4. MISSING VALUE ANALYSIS
# ============================================================

def missing_value_analysis(
    customers,
    plans,
    subscriptions,
    monthly,
    payments
):

    print("\n" + "=" * 70)
    print("MISSING VALUE ANALYSIS")
    print("=" * 70)

    datasets = {
        "dim_customer": customers,
        "dim_plan": plans,
        "fact_subscription": subscriptions,
        "fact_customer_monthly": monthly,
        "fact_payment": payments
    }

    for name, df in datasets.items():

        print(f"\n{name}")
        print("-" * 50)

        missing = df.isna().sum()

        missing = missing[
            missing > 0
        ]

        if len(missing) == 0:

            print("No missing values.")

        else:

            for column, count in missing.items():

                percentage = (
                    count / len(df)
                ) * 100

                print(
                    f"{column:<30}"
                    f"{count:>8,} "
                    f"({percentage:>6.2f}%)"
                )


# ============================================================
# 5. CUSTOMER PROFILE
# ============================================================

def customer_profile(customers):

    print("\n" + "=" * 70)
    print("CUSTOMER PROFILE")
    print("=" * 70)

    print("\nCountry Distribution")
    print("-" * 50)

    country = (
        customers["country"]
        .value_counts()
        .to_frame("customers")
    )

    country["percentage"] = (
        country["customers"]
        / len(customers)
        * 100
    )

    print(country.round(2).to_string())

    print("\nCompany Size Distribution")
    print("-" * 50)

    size = (
        customers["company_size"]
        .value_counts()
        .to_frame("customers")
    )

    size["percentage"] = (
        size["customers"]
        / len(customers)
        * 100
    )

    print(size.round(2).to_string())

    print("\nIndustry Distribution")
    print("-" * 50)

    industry = (
        customers["industry"]
        .value_counts()
        .to_frame("customers")
    )

    industry["percentage"] = (
        industry["customers"]
        / len(customers)
        * 100
    )

    print(industry.round(2).to_string())

    print("\nAcquisition Channel Distribution")
    print("-" * 50)

    channel = (
        customers["acquisition_channel"]
        .value_counts()
        .to_frame("customers")
    )

    channel["percentage"] = (
        channel["customers"]
        / len(customers)
        * 100
    )

    print(channel.round(2).to_string())


# ============================================================
# 6. PLAN PROFILE
# ============================================================

def plan_profile(
    plans,
    subscriptions
):

    print("\n" + "=" * 70)
    print("PLAN PROFILE")
    print("=" * 70)

    plan_counts = (
        subscriptions
        .groupby("plan_id")
        .size()
        .reset_index(name="subscription_records")
    )

    result = plans.merge(
        plan_counts,
        on="plan_id",
        how="left"
    )

    print(
        result.to_string(index=False)
    )


# ============================================================
# 7. CHURN ANALYSIS
# ============================================================

def churn_analysis(
    customers,
    monthly
):

    print("\n" + "=" * 70)
    print("CHURN ANALYSIS")
    print("=" * 70)

    # --------------------------------------------------------
    # Unique churned customers
    # --------------------------------------------------------

    churned_customers = (
        monthly.loc[
            monthly["churn_flag"] == 1,
            "customer_id"
        ]
        .nunique()
    )

    total_customers = (
        customers["customer_id"]
        .nunique()
    )

    churn_rate = (
        churned_customers
        / total_customers
        * 100
    )

    print(
        f"\nTotal customers:      {total_customers:,}"
    )

    print(
        f"Unique churned:       {churned_customers:,}"
    )

    print(
        f"Customer churn rate:  {churn_rate:.2f}%"
    )

    # --------------------------------------------------------
    # Monthly churn events
    # --------------------------------------------------------

    print("\nMonthly Churn Events")
    print("-" * 50)

    monthly_churn = (
        monthly[
            monthly["churn_flag"] == 1
        ]
        .groupby("month")
        .size()
        .reset_index(
            name="churned_customers"
        )
    )

    print(
        monthly_churn.to_string(index=False)
    )

    # --------------------------------------------------------
    # Churn by plan
    # --------------------------------------------------------

    print("\nChurn by Plan")
    print("-" * 50)

    active_or_churn = monthly[
        monthly["active_flag"] == 1
    ].copy()

    # Customers whose churn event happened
    # while associated with a specific plan.
    churn_by_plan = (
        monthly[
            monthly["churn_flag"] == 1
        ]
        .groupby("plan_id")
        .size()
        .reset_index(
            name="churned_customers"
        )
    )

    customer_by_plan = (
        active_or_churn
        .groupby("plan_id")["customer_id"]
        .nunique()
        .reset_index(
            name="customers"
        )
    )

    plan_result = customer_by_plan.merge(
        churn_by_plan,
        on="plan_id",
        how="left"
    )

    plan_result["churned_customers"] = (
        plan_result["churned_customers"]
        .fillna(0)
    )

    plan_result["churn_rate"] = (
        plan_result["churned_customers"]
        / plan_result["customers"]
        * 100
    )

    print(
        plan_result.round(2).to_string(
            index=False
        )
    )


# ============================================================
# 8. TENURE ANALYSIS
# ============================================================

def tenure_analysis(monthly):

    print("\n" + "=" * 70)
    print("TENURE ANALYSIS")
    print("=" * 70)

    churn = monthly[
        monthly["churn_flag"] == 1
    ].copy()

    churn["tenure_bucket"] = pd.cut(
        churn["tenure_months"],
        bins=[
            -1,
            3,
            6,
            12,
            24,
            np.inf
        ],
        labels=[
            "0-3 months",
            "4-6 months",
            "7-12 months",
            "13-24 months",
            "25+ months"
        ]
    )

    churned = (
        churn
        .groupby(
            "tenure_bucket",
            observed=True
        )
        .size()
        .reset_index(
            name="churned_customers"
        )
    )

    # Customer population by tenure bucket.
    active_records = monthly[
        monthly["active_flag"] == 1
    ].copy()

    active_records["tenure_bucket"] = pd.cut(
        active_records["tenure_months"],
        bins=[
            -1,
            3,
            6,
            12,
            24,
            np.inf
        ],
        labels=[
            "0-3 months",
            "4-6 months",
            "7-12 months",
            "13-24 months",
            "25+ months"
        ]
    )

    population = (
        active_records
        .groupby(
            "tenure_bucket",
            observed=True
        )["customer_id"]
        .nunique()
        .reset_index(
            name="customers"
        )
    )

    result = population.merge(
        churned,
        on="tenure_bucket",
        how="left"
    )

    result["churned_customers"] = (
        result["churned_customers"]
        .fillna(0)
    )

    result["churn_rate"] = (
        result["churned_customers"]
        / result["customers"]
        * 100
    )

    print(
        result.round(2).to_string(
            index=False
        )
    )


# ============================================================
# 9. ACQUISITION CHANNEL ANALYSIS
# ============================================================

def acquisition_analysis(
    customers,
    monthly
):

    print("\n" + "=" * 70)
    print("ACQUISITION CHANNEL ANALYSIS")
    print("=" * 70)

    churned_customers = (
        monthly[
            monthly["churn_flag"] == 1
        ]
        .groupby("customer_id")
        .size()
        .reset_index(
            name="churn_events"
        )
    )

    result = customers[
        [
            "customer_id",
            "acquisition_channel"
        ]
    ].merge(
        churned_customers[
            ["customer_id"]
        ],
        on="customer_id",
        how="left",
        indicator=True
    )

    result["churned"] = np.where(
        result["_merge"] == "both",
        1,
        0
    )

    channel_result = (
        result
        .groupby("acquisition_channel")
        .agg(
            customers=(
                "customer_id",
                "nunique"
            ),
            churned_customers=(
                "churned",
                "sum"
            )
        )
        .reset_index()
    )

    channel_result["churn_rate"] = (
        channel_result["churned_customers"]
        / channel_result["customers"]
        * 100
    )

    print(
        channel_result
        .sort_values(
            "churn_rate",
            ascending=False
        )
        .round(2)
        .to_string(index=False)
    )


# ============================================================
# 10. MONTHLY MRR ANALYSIS
# ============================================================

def monthly_revenue_analysis(monthly):

    print("\n" + "=" * 70)
    print("MONTHLY MRR ANALYSIS")
    print("=" * 70)

    result = (
        monthly[
            monthly["active_flag"] == 1
        ]
        .groupby("month")
        .agg(
            active_customers=(
                "customer_id",
                "nunique"
            ),
            mrr=(
                "monthly_revenue",
                "sum"
            )
        )
        .reset_index()
    )

    result["arr"] = (
        result["mrr"] * 12
    )

    print(
        result.round(2).to_string(
            index=False
        )
    )

    print("\nMRR Summary")
    print("-" * 50)

    print(
        f"Starting MRR: "
        f"${result.iloc[0]['mrr']:,.2f}"
    )

    print(
        f"Ending MRR:   "
        f"${result.iloc[-1]['mrr']:,.2f}"
    )

    growth = (
        (
            result.iloc[-1]["mrr"]
            /
            result.iloc[0]["mrr"]
        )
        - 1
    ) * 100

    print(
        f"MRR growth:   {growth:.2f}%"
    )


# ============================================================
# 11. REVENUE AT RISK
# ============================================================

def revenue_at_risk(monthly):

    print("\n" + "=" * 70)
    print("REVENUE AT RISK")
    print("=" * 70)

    churn_records = monthly[
        monthly["churn_flag"] == 1
    ].copy()

    churned_mrr = (
        churn_records[
            "monthly_revenue"
        ].sum()
    )

    print(
        f"\nMRR associated with churn events: "
        f"${churned_mrr:,.2f}"
    )

    print(
        f"Annualized revenue impact: "
        f"${churned_mrr * 12:,.2f}"
    )

    # Churned MRR by plan
    by_plan = (
        churn_records
        .groupby("plan_id")
        .agg(
            churned_customers=(
                "customer_id",
                "nunique"
            ),
            churned_mrr=(
                "monthly_revenue",
                "sum"
            )
        )
        .reset_index()
    )

    by_plan["annualized_revenue"] = (
        by_plan["churned_mrr"] * 12
    )

    print("\nChurned Revenue by Plan")
    print("-" * 50)

    print(
        by_plan.round(2).to_string(
            index=False
        )
    )


# ============================================================
# 12. ENGAGEMENT VS CHURN
# ============================================================

def engagement_analysis(monthly):

    print("\n" + "=" * 70)
    print("ENGAGEMENT VS CHURN")
    print("=" * 70)

    # Take the customer's last active month
    # before churn or latest available month.
    active = monthly[
        monthly["active_flag"] == 1
    ].copy()

    latest = (
        active
        .sort_values("month")
        .groupby("customer_id")
        .tail(1)
    )

    churned_ids = set(
        monthly.loc[
            monthly["churn_flag"] == 1,
            "customer_id"
        ]
    )

    latest["churned"] = (
        latest["customer_id"]
        .isin(churned_ids)
        .astype(int)
    )

    latest["adoption_bucket"] = pd.cut(
        latest["feature_adoption_rate"],
        bins=[
            0,
            0.25,
            0.50,
            0.75,
            1.00
        ],
        labels=[
            "0-25%",
            "26-50%",
            "51-75%",
            "76-100%"
        ],
        include_lowest=True
    )

    result = (
        latest
        .groupby(
            "adoption_bucket",
            observed=True
        )
        .agg(
            customers=(
                "customer_id",
                "nunique"
            ),
            churned_customers=(
                "churned",
                "sum"
            )
        )
        .reset_index()
    )

    result["churn_rate"] = (
        result["churned_customers"]
        / result["customers"]
        * 100
    )

    print(
        result.round(2).to_string(
            index=False
        )
    )


# ============================================================
# 13. PAYMENT ANALYSIS
# ============================================================

def payment_analysis(payments):

    print("\n" + "=" * 70)
    print("PAYMENT ANALYSIS")
    print("=" * 70)

    print("\nPayment Status")
    print("-" * 50)

    status = (
        payments["payment_status"]
        .value_counts()
        .to_frame("payments")
    )

    status["percentage"] = (
        status["payments"]
        / len(payments)
        * 100
    )

    print(
        status.round(2).to_string()
    )

    print("\nPayment Method")
    print("-" * 50)

    method = (
        payments["payment_method"]
        .value_counts()
        .to_frame("payments")
    )

    method["percentage"] = (
        method["payments"]
        / len(payments)
        * 100
    )

    print(
        method.round(2).to_string()
    )

    print("\nPayment Amount Summary")
    print("-" * 50)

    print(
        payments["amount"].describe().round(2)
    )


# ============================================================
# 14. COHORT PROFILE
# ============================================================

def cohort_profile(
    customers,
    monthly
):

    print("\n" + "=" * 70)
    print("COHORT PROFILE")
    print("=" * 70)

    customer_cohorts = customers[
        [
            "customer_id",
            "signup_date"
        ]
    ].copy()

    customer_cohorts["cohort_month"] = (
        customer_cohorts["signup_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    cohort_counts = (
        customer_cohorts
        .groupby("cohort_month")
        ["customer_id"]
        .nunique()
        .reset_index(
            name="customers"
        )
    )

    print(
        cohort_counts.to_string(
            index=False
        )
    )

    print(
        f"\nNumber of cohorts: "
        f"{len(cohort_counts)}"
    )

    print(
        f"Largest cohort: "
        f"{cohort_counts['customers'].max():,}"
    )

    print(
        f"Smallest cohort: "
        f"{cohort_counts['customers'].min():,}"
    )


# ============================================================
# 15. DATA QUALITY RULES
# ============================================================

def data_quality_rules(
    customers,
    plans,
    subscriptions,
    monthly,
    payments
):

    print("\n" + "=" * 70)
    print("DATA QUALITY RULES")
    print("=" * 70)

    checks = []

    # Customer IDs
    checks.append(
        (
            "Unique customer IDs",
            customers["customer_id"].is_unique
        )
    )

    # Subscription foreign keys
    checks.append(
        (
            "Valid subscription customer IDs",
            subscriptions["customer_id"]
            .isin(customers["customer_id"])
            .all()
        )
    )

    checks.append(
        (
            "Valid subscription plan IDs",
            subscriptions["plan_id"]
            .isin(plans["plan_id"])
            .all()
        )
    )

    # Monthly foreign keys
    checks.append(
        (
            "Valid monthly customer IDs",
            monthly["customer_id"]
            .isin(customers["customer_id"])
            .all()
        )
    )

    checks.append(
        (
            "Valid monthly plan IDs",
            monthly.loc[
                monthly["plan_id"].notna(),
                "plan_id"
            ]
            .isin(plans["plan_id"])
            .all()
        )
    )

    # Revenue
    checks.append(
        (
            "Monthly revenue >= 0",
            (monthly["monthly_revenue"] >= 0).all()
        )
    )

    # Feature adoption
    checks.append(
        (
            "Feature adoption between 0 and 1",
            monthly[
                "feature_adoption_rate"
            ].between(0, 1).all()
        )
    )

    # Numeric fields
    checks.append(
        (
            "Login frequency >= 0",
            (monthly["login_frequency"] >= 0).all()
        )
    )

    checks.append(
        (
            "Support tickets >= 0",
            (monthly["support_tickets"] >= 0).all()
        )
    )

    checks.append(
        (
            "Payment failures >= 0",
            (monthly["payment_failures"] >= 0).all()
        )
    )

    # Payment foreign key
    checks.append(
        (
            "Valid payment customer IDs",
            payments["customer_id"]
            .isin(customers["customer_id"])
            .all()
        )
    )

    # Subscription dates
    valid_subscription_dates = (
        subscriptions["end_date"].isna()
        |
        (
            subscriptions["end_date"]
            >= subscriptions["start_date"]
        )
    )

    checks.append(
        (
            "Valid subscription date ranges",
            valid_subscription_dates.all()
        )
    )

    # Print results
    print()

    passed = 0

    for check_name, result in checks:

        if result:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"

        print(
            f"[{status}] {check_name}"
        )

    print(
        f"\nPassed: {passed}/{len(checks)}"
    )


# ============================================================
# 16. MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("CLOUDFLOW SAAS DATASET PROFILE")
    print("=" * 70)

    (
        customers,
        plans,
        subscriptions,
        monthly,
        payments
    ) = load_data()

    basic_information(
        customers,
        plans,
        subscriptions,
        monthly,
        payments
    )

    missing_value_analysis(
        customers,
        plans,
        subscriptions,
        monthly,
        payments
    )

    customer_profile(
        customers
    )

    plan_profile(
        plans,
        subscriptions
    )

    churn_analysis(
        customers,
        monthly
    )

    tenure_analysis(
        monthly
    )

    acquisition_analysis(
        customers,
        monthly
    )

    monthly_revenue_analysis(
        monthly
    )

    revenue_at_risk(
        monthly
    )

    engagement_analysis(
        monthly
    )

    payment_analysis(
        payments
    )

    cohort_profile(
        customers,
        monthly
    )

    data_quality_rules(
        customers,
        plans,
        subscriptions,
        monthly,
        payments
    )

    print("\n" + "=" * 70)
    print("DATASET PROFILING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()

