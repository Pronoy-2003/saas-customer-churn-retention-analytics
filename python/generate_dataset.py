"""
============================================================
SaaS Customer Churn & Retention Analytics
File: generate_dataset.py
============================================================

Purpose:
    Generate a realistic synthetic dataset for the CloudFlow
    B2B SaaS customer churn and retention analytics project.

The script generates five related datasets:

    1. dim_customer.csv
       Customer master information.

    2. dim_plan.csv
       SaaS subscription plan information.

    3. fact_subscription.csv
       Customer subscription history.

    4. fact_customer_monthly.csv
       Monthly customer activity, revenue, engagement,
       tenure, and churn information.

    5. fact_payment.csv
       Customer payment history.

The generated data is used for:
    - Customer churn analysis
    - Retention and cohort analysis
    - Customer segmentation
    - Revenue analysis
    - Customer lifetime value (CLV)
    - Revenue-at-risk analysis

The dataset covers January 2024 to December 2025
and contains 10,000 synthetic customers.

IMPORTANT:
    This dataset is synthetic and was created specifically
    for portfolio and educational purposes. It does not
    represent data from a real company.
============================================================
"""


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd

from faker import Faker


# ============================================================
# 1. CONFIGURATION
# ============================================================

SEED = 42

np.random.seed(SEED)

fake = Faker()
Faker.seed(SEED)


NUM_CUSTOMERS = 10_000

START_DATE = pd.Timestamp("2024-01-01")
END_DATE = pd.Timestamp("2025-12-31")


OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. REFERENCE DATA
# ============================================================

COUNTRIES = [
    "USA",
    "India",
    "UK",
    "Canada",
    "Australia",
    "Germany",
    "Singapore",
    "Other",
]


COUNTRY_PROBS = [
    0.35,
    0.20,
    0.12,
    0.08,
    0.07,
    0.06,
    0.04,
    0.08,
]


INDUSTRIES = [
    "Technology",
    "Retail",
    "Healthcare",
    "Finance",
    "Education",
    "Professional Services",
    "Manufacturing",
    "Marketing",
    "Other",
]


INDUSTRY_PROBS = [
    0.20,
    0.15,
    0.12,
    0.12,
    0.10,
    0.10,
    0.08,
    0.08,
    0.05,
]


COMPANY_SIZES = [
    "Small",
    "Medium",
    "Large",
    "Enterprise",
]


COMPANY_SIZE_PROBS = [
    0.45,
    0.35,
    0.15,
    0.05,
]


ACQUISITION_CHANNELS = [
    "Organic Search",
    "Paid Search",
    "Paid Social",
    "Referral",
    "Partner",
    "Sales",
    "Email Marketing",
]


ACQUISITION_PROBS = [
    0.25,
    0.18,
    0.12,
    0.15,
    0.10,
    0.12,
    0.08,
]


SALES_REGIONS = {
    "USA": "North America",
    "Canada": "North America",
    "India": "APAC",
    "UK": "Europe",
    "Australia": "APAC",
    "Germany": "Europe",
    "Singapore": "APAC",
    "Other": "Other",
}


# ============================================================
# 3. PLAN MASTER
# ============================================================

PLAN_DATA = [
    {
        "plan_id": "P01",
        "plan_name": "Starter",
        "monthly_price": 29.0,
        "annual_price": 290.0,
    },
    {
        "plan_id": "P02",
        "plan_name": "Professional",
        "monthly_price": 79.0,
        "annual_price": 790.0,
    },
    {
        "plan_id": "P03",
        "plan_name": "Business",
        "monthly_price": 149.0,
        "annual_price": 1490.0,
    },
    {
        "plan_id": "P04",
        "plan_name": "Enterprise",
        "monthly_price": 399.0,
        "annual_price": 3990.0,
    },
]


PLAN_DF = pd.DataFrame(
    PLAN_DATA
)


PLAN_IDS = [
    "P01",
    "P02",
    "P03",
    "P04",
]


PLAN_PROBS = [
    0.40,
    0.35,
    0.20,
    0.05,
]


PLAN_PRICES = {
    "P01": 29.0,
    "P02": 79.0,
    "P03": 149.0,
    "P04": 399.0,
}


PLAN_NAMES = {
    "P01": "Starter",
    "P02": "Professional",
    "P03": "Business",
    "P04": "Enterprise",
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def random_date(start, end):
    """
    Return a random date between two timestamps.
    """

    days = (
        end - start
    ).days

    if days <= 0:
        return start

    return start + pd.Timedelta(
        days=np.random.randint(
            0,
            days + 1
        )
    )


def clamp(
    value,
    minimum,
    maximum
):
    """
    Keep a numeric value inside a specified range.
    """

    return max(
        minimum,
        min(
            maximum,
            value
        )
    )


def month_difference(
    start_date,
    end_date
):
    """
    Return complete calendar month difference.
    """

    return (
        (end_date.year - start_date.year) * 12
        + (end_date.month - start_date.month)
    )


def generate_company_name():
    """
    Generate a simple fictional company name.
    """

    prefixes = [
        "Cloud",
        "Nova",
        "Prime",
        "Vertex",
        "Blue",
        "Bright",
        "Summit",
        "Next",
        "Apex",
        "Fusion",
        "Core",
        "Digital",
    ]

    suffixes = [
        "Labs",
        "Technologies",
        "Solutions",
        "Systems",
        "Works",
        "Group",
        "Software",
        "Analytics",
        "Services",
        "Networks",
    ]

    return (
        f"{np.random.choice(prefixes)} "
        f"{np.random.choice(suffixes)}"
    )


# ============================================================
# 5. GENERATE CUSTOMER MASTER
# ============================================================

def generate_customers():

    print("\nGenerating customers...")

    rows = []

    for i in range(
        1,
        NUM_CUSTOMERS + 1
    ):

        customer_id = (
            f"C{i:05d}"
        )

        signup_date = random_date(
            START_DATE,
            END_DATE - pd.Timedelta(
                days=30
            )
        )

        country = np.random.choice(
            COUNTRIES,
            p=COUNTRY_PROBS
        )

        industry = np.random.choice(
            INDUSTRIES,
            p=INDUSTRY_PROBS
        )

        company_size = np.random.choice(
            COMPANY_SIZES,
            p=COMPANY_SIZE_PROBS
        )

        acquisition_channel = np.random.choice(
            ACQUISITION_CHANNELS,
            p=ACQUISITION_PROBS
        )

        sales_region = (
            SALES_REGIONS[country]
        )

        rows.append(
            {
                "customer_id": customer_id,
                "company_name": generate_company_name(),
                "signup_date": signup_date.date(),
                "country": country,
                "industry": industry,
                "company_size": company_size,
                "acquisition_channel": acquisition_channel,
                "sales_region": sales_region,
            }
        )

    df = pd.DataFrame(rows)

    print(
        f"Customers generated: "
        f"{len(df):,}"
    )

    return df


# ============================================================
# 6. GENERATE SUBSCRIPTIONS
# ============================================================

def generate_subscriptions(
    customers
):

    print("\nGenerating subscriptions...")

    rows = []

    subscription_counter = 1

    for _, customer in customers.iterrows():

        customer_id = (
            customer["customer_id"]
        )

        signup_date = pd.Timestamp(
            customer["signup_date"]
        )

        acquisition_channel = (
            customer["acquisition_channel"]
        )

        company_size = (
            customer["company_size"]
        )

        # ----------------------------------------------------
        # Initial plan
        # ----------------------------------------------------

        plan_id = np.random.choice(
            PLAN_IDS,
            p=PLAN_PROBS
        )

        # Enterprise companies are more likely
        # to select Business / Enterprise.
        if company_size == "Enterprise":

            plan_id = np.random.choice(
                ["P03", "P04"],
                p=[0.40, 0.60]
            )

        elif company_size == "Large":

            plan_id = np.random.choice(
                ["P02", "P03", "P04"],
                p=[0.50, 0.40, 0.10]
            )

        # ----------------------------------------------------
        # Churn probability
        # ----------------------------------------------------

        base_churn = 0.16

        acquisition_effect = {

            "Organic Search": -0.02,

            "Paid Search": 0.03,

            "Paid Social": 0.06,

            "Referral": -0.04,

            "Partner": -0.03,

            "Sales": 0.00,

            "Email Marketing": -0.01,
        }

        churn_probability = (
            base_churn
            + acquisition_effect[
                acquisition_channel
            ]
        )

        # ----------------------------------------------------
        # Plan effect
        # ----------------------------------------------------

        plan_effect = {

            "P01": 0.04,

            "P02": 0.00,

            "P03": -0.03,

            "P04": -0.06,
        }

        churn_probability += (
            plan_effect[plan_id]
        )

        # Enterprise customers are less likely
        # to churn.
        if company_size == "Enterprise":

            churn_probability -= 0.04

        churn_probability = clamp(
            churn_probability,
            0.04,
            0.35
        )

        will_churn = (
            np.random.random()
            < churn_probability
        )

        # ----------------------------------------------------
        # Determine churn date
        # ----------------------------------------------------

        if will_churn:

            minimum_churn_date = (
                signup_date
                + pd.Timedelta(days=60)
            )

            maximum_churn_date = min(
                END_DATE,
                signup_date
                + pd.Timedelta(days=600)
            )

            if (
                minimum_churn_date
                < maximum_churn_date
            ):

                churn_date = random_date(
                    minimum_churn_date,
                    maximum_churn_date
                )

            else:

                churn_date = (
                    maximum_churn_date
                )

        else:

            # Customer remains active
            # through the observation period.
            churn_date = END_DATE

        subscription_end = churn_date

        # ----------------------------------------------------
        # Plan changes
        # ----------------------------------------------------

        number_of_changes = 0

        if (
            subscription_end
            - signup_date
            >= pd.Timedelta(days=180)
        ):

            change_probability = 0.20

            if (
                np.random.random()
                < change_probability
            ):

                number_of_changes = 1

            if (
                subscription_end
                - signup_date
                >= pd.Timedelta(days=365)
                and
                np.random.random() < 0.08
            ):

                number_of_changes = 2

        segment_start = signup_date

        # ----------------------------------------------------
        # Generate subscription segments
        # ----------------------------------------------------

        for change_index in range(
            number_of_changes + 1
        ):

            # Determine segment end.
            if (
                change_index
                < number_of_changes
            ):

                remaining_days = (
                    subscription_end
                    - segment_start
                ).days

                if remaining_days <= 90:

                    segment_end = (
                        subscription_end
                    )

                else:

                    change_days = (
                        np.random.randint(
                            90,
                            remaining_days
                        )
                    )

                    segment_end = (
                        segment_start
                        + pd.Timedelta(
                            days=change_days
                        )
                    )

            else:

                segment_end = (
                    subscription_end
                )

            # ------------------------------------------------
            # Billing cycle
            # ------------------------------------------------

            billing_cycle = np.random.choice(
                [
                    "Monthly",
                    "Annual"
                ],
                p=[
                    0.75,
                    0.25
                ]
            )

            # ------------------------------------------------
            # Subscription status
            # ------------------------------------------------

            status = (
                "Cancelled"
                if (
                    will_churn
                    and segment_end < END_DATE
                )
                else "Active"
            )

            # ------------------------------------------------
            # Store subscription
            # ------------------------------------------------

            rows.append(
                {
                    "subscription_id":
                        f"S{subscription_counter:06d}",

                    "customer_id":
                        customer_id,

                    "plan_id":
                        plan_id,

                    "start_date":
                        segment_start.date(),

                    "end_date":
                        (
                            segment_end.date()
                            if status == "Cancelled"
                            else None
                        ),

                    "billing_cycle":
                        billing_cycle,

                    "monthly_price":
                        PLAN_PRICES[plan_id],

                    "subscription_status":
                        status,
                }
            )

            subscription_counter += 1

            # ------------------------------------------------
            # Determine next plan
            # ------------------------------------------------

            if (
                change_index
                < number_of_changes
            ):

                current_plan_index = (
                    PLAN_IDS.index(
                        plan_id
                    )
                )

                # 65% probability of upgrade
                if (
                    np.random.random()
                    < 0.65
                ):

                    new_index = min(
                        current_plan_index + 1,
                        len(PLAN_IDS) - 1
                    )

                # 35% probability of downgrade
                else:

                    new_index = max(
                        current_plan_index - 1,
                        0
                    )

                plan_id = (
                    PLAN_IDS[new_index]
                )

                segment_start = (
                    segment_end
                )

    df = pd.DataFrame(rows)

    print(
        f"Subscriptions generated: "
        f"{len(df):,}"
    )

    return df


# ============================================================
# 7. GENERATE MONTHLY CUSTOMER STATUS
# ============================================================

def generate_monthly_status(
    customers,
    subscriptions
):

    """
    Generate monthly customer-level analytical snapshots.

    Main analytical table for:

        - Churn
        - Retention
        - Cohort analysis
        - MRR
        - Engagement
        - Customer segmentation
        - Revenue at risk
    """

    print(
        "\nGenerating monthly customer status..."
    )

    # --------------------------------------------------------
    # Monthly calendar
    # --------------------------------------------------------

    months = pd.date_range(
        START_DATE,
        END_DATE,
        freq="MS"
    )

    rows = []

    # --------------------------------------------------------
    # Prepare subscription dates
    # --------------------------------------------------------

    subscriptions = (
        subscriptions.copy()
    )

    subscriptions["start_date"] = (
        pd.to_datetime(
            subscriptions["start_date"]
        )
    )

    subscriptions["end_date"] = (
        pd.to_datetime(
            subscriptions["end_date"]
        )
    )

    # --------------------------------------------------------
    # Customer loop
    # --------------------------------------------------------

    for _, customer in customers.iterrows():

        customer_id = (
            customer["customer_id"]
        )

        signup_date = pd.Timestamp(
            customer["signup_date"]
        )

        acquisition_channel = (
            customer["acquisition_channel"]
        )

        # All subscriptions for customer.
        customer_subs = (
            subscriptions[
                subscriptions["customer_id"]
                == customer_id
            ]
            .sort_values("start_date")
            .reset_index(drop=True)
        )

        # ----------------------------------------------------
        # Monthly loop
        # ----------------------------------------------------

        for month in months:

            month_start = (
                pd.Timestamp(month)
            )

            month_end = (
                month_start
                + pd.offsets.MonthEnd(1)
            )

            # ------------------------------------------------
            # Customer hasn't signed up yet.
            # ------------------------------------------------

            if month_end < signup_date:

                continue

            # ------------------------------------------------
            # Find subscription active at month-end.
            #
            # IMPORTANT:
            # We use month-end status because this is a
            # monthly snapshot table.
            # ------------------------------------------------

            active_subs = customer_subs[
                (
                    customer_subs["start_date"]
                    <= month_end
                )
                &
                (
                    customer_subs["end_date"].isna()
                    |
                    (
                        customer_subs["end_date"]
                        >= month_end
                    )
                )
            ]

            # ------------------------------------------------
            # Determine churn during this month.
            # ------------------------------------------------

            churn_flag = 0

            # Find the customer's final subscription.
            latest_sub = (
                customer_subs.iloc[-1]
            )

            latest_end = (
                latest_sub["end_date"]
            )

            if pd.notna(latest_end):

                if (
                    latest_end.year
                    == month_start.year
                    and
                    latest_end.month
                    == month_start.month
                ):

                    churn_flag = 1

            # ------------------------------------------------
            # Active customer
            # ------------------------------------------------

            if len(active_subs) > 0:

                subscription = (
                    active_subs.iloc[-1]
                )

                active_flag = 1

                plan_id = (
                    subscription["plan_id"]
                )

                monthly_revenue = (
                    PLAN_PRICES[plan_id]
                )

            # ------------------------------------------------
            # Inactive / churned customer
            # ------------------------------------------------

            else:

                active_flag = 0

                # ------------------------------------------------
                # Churn month:
                #
                # Keep final plan + MRR.
                #
                # This allows:
                #   - churn by plan
                #   - MRR lost
                #   - ARR lost
                #   - revenue at risk
                # ------------------------------------------------

                if churn_flag == 1:

                    plan_id = (
                        latest_sub["plan_id"]
                    )

                    monthly_revenue = (
                        PLAN_PRICES[plan_id]
                    )

                else:

                    plan_id = None

                    monthly_revenue = 0.0

            # ------------------------------------------------
            # Tenure
            # ------------------------------------------------

            tenure_months = max(
                0,
                month_difference(
                    signup_date,
                    month_start
                )
            )

            # ------------------------------------------------
            # Engagement
            # ------------------------------------------------

            if active_flag == 1:

                # Base login frequency
                base_login = 12

                # Customers become slightly more engaged
                # as tenure increases.
                tenure_bonus = min(
                    tenure_months * 0.25,
                    8
                )

                login_frequency = (
                    np.random.normal(
                        base_login
                        + tenure_bonus,
                        5
                    )
                )

                login_frequency = int(
                    clamp(
                        login_frequency,
                        0,
                        40
                    )
                )

                # ------------------------------------------------
                # Feature adoption
                # ------------------------------------------------

                feature_adoption = (
                    np.random.normal(
                        0.55
                        + min(
                            tenure_months * 0.01,
                            0.15
                        ),
                        0.15
                    )
                )

                feature_adoption = round(
                    clamp(
                        feature_adoption,
                        0.05,
                        1.00
                    ),
                    2
                )

                # ------------------------------------------------
                # Support tickets
                # ------------------------------------------------

                support_tickets = int(
                    clamp(
                        np.random.poisson(1.5),
                        0,
                        10
                    )
                )

                # ------------------------------------------------
                # Payment failures
                # ------------------------------------------------

                payment_failures = int(
                    np.random.choice(
                        [0, 1, 2, 3],
                        p=[
                            0.88,
                            0.08,
                            0.03,
                            0.01
                        ]
                    )
                )

            else:

                login_frequency = 0

                feature_adoption = 0.0

                support_tickets = 0

                payment_failures = 0

            # ------------------------------------------------
            # Append monthly record
            # ------------------------------------------------

            rows.append(
                {
                    "customer_id":
                        customer_id,

                    "month":
                        month_start.date(),

                    "plan_id":
                        plan_id,

                    "active_flag":
                        active_flag,

                    "monthly_revenue":
                        round(
                            monthly_revenue,
                            2
                        ),

                    "tenure_months":
                        tenure_months,

                    "login_frequency":
                        login_frequency,

                    "feature_adoption_rate":
                        feature_adoption,

                    "support_tickets":
                        support_tickets,

                    "payment_failures":
                        payment_failures,

                    "churn_flag":
                        churn_flag,
                }
            )

    df = pd.DataFrame(rows)

    print(
        f"Monthly records generated: "
        f"{len(df):,}"
    )

    return df


# ============================================================
# 8. GENERATE PAYMENT HISTORY
# ============================================================

def generate_payments(
    monthly_status
):

    """
    Generate payment transactions from
    active monthly customer records.
    """

    print(
        "\nGenerating payment history..."
    )

    rows = []

    payment_counter = 1

    # Only active customers generate
    # regular monthly payments.
    active_records = (
        monthly_status[
            monthly_status["active_flag"] == 1
        ]
        .copy()
    )

    for _, record in (
        active_records.iterrows()
    ):

        customer_id = (
            record["customer_id"]
        )

        month = pd.Timestamp(
            record["month"]
        )

        amount = (
            record["monthly_revenue"]
        )

        # ----------------------------------------------------
        # Payment date
        # ----------------------------------------------------

        payment_date = (
            month
            + pd.Timedelta(
                days=np.random.randint(
                    1,
                    25
                )
            )
        )

        # ----------------------------------------------------
        # Payment status
        # ----------------------------------------------------

        payment_status = np.random.choice(
            [
                "Successful",
                "Failed",
                "Refunded"
            ],
            p=[
                0.94,
                0.05,
                0.01
            ]
        )

        # ----------------------------------------------------
        # Payment method
        # ----------------------------------------------------

        payment_method = np.random.choice(
            [
                "Credit Card",
                "Debit Card",
                "Bank Transfer",
                "PayPal"
            ],
            p=[
                0.55,
                0.15,
                0.20,
                0.10
            ]
        )

        # ----------------------------------------------------
        # Payment amount
        # ----------------------------------------------------

        if payment_status == "Failed":

            payment_amount = 0.0

        elif payment_status == "Refunded":

            payment_amount = -amount

        else:

            payment_amount = amount

        # ----------------------------------------------------
        # Store payment
        # ----------------------------------------------------

        rows.append(
            {
                "payment_id":
                    f"PAY{payment_counter:07d}",

                "customer_id":
                    customer_id,

                "payment_date":
                    payment_date.date(),

                "amount":
                    round(
                        payment_amount,
                        2
                    ),

                "payment_status":
                    payment_status,

                "payment_method":
                    payment_method,
            }
        )

        payment_counter += 1

    # --------------------------------------------------------
    # IMPORTANT:
    # Always create the DataFrame with explicit columns.
    #
    # This prevents:
    #
    # KeyError: 'customer_id'
    #
    # even if no records are generated.
    # --------------------------------------------------------

    df = pd.DataFrame(
        rows,
        columns=[
            "payment_id",
            "customer_id",
            "payment_date",
            "amount",
            "payment_status",
            "payment_method",
        ]
    )

    print(
        f"Payment records generated: "
        f"{len(df):,}"
    )

    return df


# ============================================================
# 9. DATA QUALITY VALIDATION
# ============================================================

def run_basic_validation(
    customers,
    plans,
    subscriptions,
    monthly_status,
    payments
):

    print("\n" + "=" * 60)
    print("DATA VALIDATION")
    print("=" * 60)

    # ========================================================
    # CUSTOMERS
    # ========================================================

    print("\nCustomers")
    print("-" * 40)

    print(
        f"Rows: {len(customers):,}"
    )

    print(
        "Duplicate customer IDs:",
        customers[
            "customer_id"
        ].duplicated().sum()
    )

    # ========================================================
    # PLANS
    # ========================================================

    print("\nPlans")
    print("-" * 40)

    print(
        f"Rows: {len(plans):,}"
    )

    print(
        "Duplicate plan IDs:",
        plans[
            "plan_id"
        ].duplicated().sum()
    )

    # ========================================================
    # SUBSCRIPTIONS
    # ========================================================

    print("\nSubscriptions")
    print("-" * 40)

    print(
        f"Rows: {len(subscriptions):,}"
    )

    orphan_subscriptions = (
        ~subscriptions[
            "customer_id"
        ].isin(
            customers[
                "customer_id"
            ]
        )
    ).sum()

    print(
        "Orphan customer IDs:",
        orphan_subscriptions
    )

    invalid_dates = (
        pd.to_datetime(
            subscriptions["end_date"]
        )
        <
        pd.to_datetime(
            subscriptions["start_date"]
        )
    ).sum()

    print(
        "Invalid subscription dates:",
        invalid_dates
    )

    invalid_plan_ids = (
        ~subscriptions[
            "plan_id"
        ].isin(
            plans[
                "plan_id"
            ]
        )
    ).sum()

    print(
        "Invalid plan IDs:",
        invalid_plan_ids
    )

    # ========================================================
    # MONTHLY CUSTOMER STATUS
    # ========================================================

    print(
        "\nMonthly Customer Status"
    )

    print("-" * 40)

    print(
        f"Rows: {len(monthly_status):,}"
    )

    orphan_monthly = (
        ~monthly_status[
            "customer_id"
        ].isin(
            customers[
                "customer_id"
            ]
        )
    ).sum()

    print(
        "Orphan customer IDs:",
        orphan_monthly
    )

    invalid_adoption = (
        (
            monthly_status[
                "feature_adoption_rate"
            ]
            < 0
        )
        |
        (
            monthly_status[
                "feature_adoption_rate"
            ]
            > 1
        )
    ).sum()

    print(
        "Invalid adoption values:",
        invalid_adoption
    )

    negative_revenue = (
        monthly_status[
            "monthly_revenue"
        ]
        < 0
    ).sum()

    print(
        "Negative MRR records:",
        negative_revenue
    )

    invalid_flags = (
        ~monthly_status[
            "active_flag"
        ].isin(
            [0, 1]
        )
    ).sum()

    print(
        "Invalid active flags:",
        invalid_flags
    )

    invalid_churn_flags = (
        ~monthly_status[
            "churn_flag"
        ].isin(
            [0, 1]
        )
    ).sum()

    print(
        "Invalid churn flags:",
        invalid_churn_flags
    )

    # ========================================================
    # PAYMENT VALIDATION
    # ========================================================

    print("\nPayments")
    print("-" * 40)

    print(
        f"Rows: {len(payments):,}"
    )

    # Prevent KeyError even if payments is empty.
    if "customer_id" in payments.columns:

        orphan_payments = (
            ~payments[
                "customer_id"
            ].isin(
                customers[
                    "customer_id"
                ]
            )
        ).sum()

    else:

        orphan_payments = "N/A"

    print(
        "Orphan customer IDs:",
        orphan_payments
    )

    # ========================================================
    # CHURN
    # ========================================================

    print("\nChurn")
    print("-" * 40)

    churn_events = int(
        monthly_status[
            "churn_flag"
        ].sum()
    )

    unique_churned_customers = (
        monthly_status.loc[
            monthly_status[
                "churn_flag"
            ] == 1,
            "customer_id"
        ].nunique()
    )

    customer_count = (
        customers[
            "customer_id"
        ].nunique()
    )

    churn_rate = (
        unique_churned_customers
        / customer_count
    ) * 100

    print(
        f"Churn events: "
        f"{churn_events:,}"
    )

    print(
        f"Unique churned customers: "
        f"{unique_churned_customers:,}"
    )

    print(
        f"Customer churn rate: "
        f"{churn_rate:.2f}%"
    )

    # ========================================================
    # CHURN BY PLAN
    # ========================================================

    print(
        "\nChurn by Plan"
    )

    print("-" * 40)

    churn_plan = (
        monthly_status[
            monthly_status[
                "churn_flag"
            ] == 1
        ]
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

    if len(churn_plan) > 0:

        churn_plan["plan_name"] = (
            churn_plan[
                "plan_id"
            ].map(
                PLAN_NAMES
            )
        )

        print(
            churn_plan[
                [
                    "plan_id",
                    "plan_name",
                    "churned_customers",
                    "churned_mrr"
                ]
            ]
            .round(2)
            .to_string(
                index=False
            )
        )

    else:

        print(
            "No churn records found."
        )

    # ========================================================
    # REVENUE
    # ========================================================

    active_mrr = (
        monthly_status.loc[
            monthly_status[
                "active_flag"
            ] == 1,
            "monthly_revenue"
        ].sum()
    )

    churned_mrr = (
        monthly_status.loc[
            monthly_status[
                "churn_flag"
            ] == 1,
            "monthly_revenue"
        ].sum()
    )

    print(
        "\nRevenue"
    )

    print("-" * 40)

    print(
        "Total active MRR observations: "
        f"${active_mrr:,.2f}"
    )

    print(
        "MRR associated with churn: "
        f"${churned_mrr:,.2f}"
    )

    print(
        "Annualized revenue at risk: "
        f"${churned_mrr * 12:,.2f}"
    )

    print(
        "\nValidation completed."
    )


# ============================================================
# 10. SAVE DATASETS
# ============================================================

def save_datasets(
    customers,
    plans,
    subscriptions,
    monthly_status,
    payments
):

    print(
        "\nSaving CSV files..."
    )

    # --------------------------------------------------------
    # Customer
    # --------------------------------------------------------

    customers.to_csv(
        OUTPUT_DIR
        / "dim_customer.csv",
        index=False
    )

    # --------------------------------------------------------
    # Plan
    # --------------------------------------------------------

    plans.to_csv(
        OUTPUT_DIR
        / "dim_plan.csv",
        index=False
    )

    # --------------------------------------------------------
    # Subscription
    # --------------------------------------------------------

    subscriptions.to_csv(
        OUTPUT_DIR
        / "fact_subscription.csv",
        index=False
    )

    # --------------------------------------------------------
    # Monthly
    # --------------------------------------------------------

    monthly_status.to_csv(
        OUTPUT_DIR
        / "fact_customer_monthly.csv",
        index=False
    )

    # --------------------------------------------------------
    # Payments
    # --------------------------------------------------------

    payments.to_csv(
        OUTPUT_DIR
        / "fact_payment.csv",
        index=False
    )

    # --------------------------------------------------------
    # File information
    # --------------------------------------------------------

    print(
        "\nFiles created:"
    )

    for file in sorted(
        OUTPUT_DIR.glob("*.csv")
    ):

        size_mb = (
            file.stat().st_size
            / (1024 * 1024)
        )

        print(
            f"  {file.name:<32}"
            f"{size_mb:.2f} MB"
        )


# ============================================================
# 11. MAIN
# ============================================================

def main():

    print("=" * 60)

    print(
        "CLOUDFLOW SAAS DATASET GENERATOR"
    )

    print("=" * 60)

    print(
        f"\nCustomers: "
        f"{NUM_CUSTOMERS:,}"
    )

    print(
        f"Period: "
        f"{START_DATE.date()} "
        f"→ "
        f"{END_DATE.date()}"
    )

    print(
        f"Output: "
        f"{OUTPUT_DIR}"
    )

    # --------------------------------------------------------
    # 1. Customer master
    # --------------------------------------------------------

    customers = (
        generate_customers()
    )

    # --------------------------------------------------------
    # 2. Plan master
    # --------------------------------------------------------

    plans = PLAN_DF.copy()

    # --------------------------------------------------------
    # 3. Subscription history
    # --------------------------------------------------------

    subscriptions = (
        generate_subscriptions(
            customers
        )
    )

    # --------------------------------------------------------
    # 4. Monthly customer snapshots
    # --------------------------------------------------------

    monthly_status = (
        generate_monthly_status(
            customers,
            subscriptions
        )
    )

    # --------------------------------------------------------
    # 5. Payment history
    # --------------------------------------------------------

    payments = (
        generate_payments(
            monthly_status
        )
    )

    # --------------------------------------------------------
    # 6. Validation
    # --------------------------------------------------------

    run_basic_validation(
        customers,
        plans,
        subscriptions,
        monthly_status,
        payments
    )

    # --------------------------------------------------------
    # 7. Save
    # --------------------------------------------------------

    save_datasets(
        customers,
        plans,
        subscriptions,
        monthly_status,
        payments
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "DATASET GENERATION COMPLETED"
    )

    print(
        "=" * 60
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()

