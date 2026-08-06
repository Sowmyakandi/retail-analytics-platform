import random
import uuid
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

# Create the raw data folder if it doesn't exist
RAW_DATA_PATH = Path("data/raw")
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

# Create a Faker object
fake = Faker()

print("Retail Analytics Project Started")
print(f"Raw data folder: {RAW_DATA_PATH.resolve()}")

customers = []

for customer_id in range(1, 1001):

    customer = {
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
        "state": fake.state(),
        "signup_date": fake.date_between(start_date="-3y", end_date="today")
    }

    customers.append(customer)

print(f"Generated {len(customers)} customers")

customers_df = pd.DataFrame(customers)

customers_df.to_csv(
    RAW_DATA_PATH / "customers.csv",
    index=False
)

print("customers.csv created successfully!")
# -----------------------------
# Product generation
# -----------------------------

product_catalog = {
    "Electronics": {
        "brands": ["Samsung", "Sony", "LG", "HP", "Dell", "Lenovo", "Apple", "Bose"],
        "products": ["Laptop", "Tablet", "Camera", "Monitor", "Headphones", "Smartphone", "Smartwatch", "Speaker"],
        "price_range": (100, 2000),
    },
    "Clothing": {
        "brands": ["Nike", "Adidas", "Zara", "H&M", "Levi's", "Gap", "Puma"],
        "products": ["T-Shirt", "Jeans", "Jacket", "Hoodie", "Shorts", "Sneakers", "Dress"],
        "price_range": (15, 200),
    },
    "Home & Kitchen": {
        "brands": ["IKEA", "KitchenAid", "Cuisinart", "Instant Pot", "Dyson"],
        "products": ["Blender", "Toaster", "Cookware Set", "Vacuum", "Air Fryer", "Coffee Maker"],
        "price_range": (10, 500),
    },
    "Toys": {
        "brands": ["LEGO", "Hasbro", "Mattel", "Fisher-Price", "Nerf"],
        "products": ["Building Set", "Action Figure", "Puzzle", "Board Game", "Doll", "RC Car"],
        "price_range": (5, 100),
    },
    "Books": {
        "brands": ["Penguin", "HarperCollins", "Scholastic", "Simon & Schuster"],
        "products": ["Novel", "Cookbook", "Biography", "Journal", "Guidebook"],
        "price_range": (5, 60),
    },
    "Sports Equipment": {
        "brands": ["Wilson", "Spalding", "Under Armour", "Nike", "Adidas"],
        "products": ["Basketball", "Yoga Mat", "Dumbbell Set", "Running Shoes", "Tennis Racket"],
        "price_range": (10, 300),
    },
    "Beauty": {
        "brands": ["L'Oreal", "Maybelline", "Nivea", "Neutrogena", "Dove"],
        "products": ["Face Cream", "Shampoo", "Lipstick", "Perfume", "Serum"],
        "price_range": (5, 150),
    },
    "Grocery": {
        "brands": ["Kraft", "Nestle", "General Mills", "Kellogg's", "Heinz"],
        "products": ["Cereal", "Pasta Sauce", "Snack Bar", "Coffee", "Juice"],
        "price_range": (2, 50),
    },
}

product_adjectives = [
    "Pro",
    "Ultra",
    "Max",
    "Plus",
    "Classic",
    "Deluxe",
    "Mini",
    "Smart",
    "Premium",
    "Essential",
]

products = []
categories = list(product_catalog.keys())

for product_id in range(1, 201):
    category = random.choice(categories)
    catalog_entry = product_catalog[category]

    brand = random.choice(catalog_entry["brands"])
    product_type = random.choice(catalog_entry["products"])
    adjective = random.choice(product_adjectives)

    minimum_price, maximum_price = catalog_entry["price_range"]

    product = {
        "product_id": product_id,
        "product_name": f"{brand} {adjective} {product_type}",
        "category": category,
        "brand": brand,
        "price": round(
            random.uniform(minimum_price, maximum_price),
            2
        ),
    }

    products.append(product)

products_df = pd.DataFrame(products)

products_df.to_csv(
    RAW_DATA_PATH / "products.csv",
    index=False
)

print(f"Generated {len(products)} products")
print("products.csv created successfully!")
# ---------------------------------------------------------
# GENERATE ORDERS
# ---------------------------------------------------------

quantity_ranges = {
    "Electronics": (1, 2),
    "Clothing": (1, 4),
    "Home & Kitchen": (1, 3),
    "Toys": (1, 5),
    "Books": (1, 6),
    "Sports Equipment": (1, 3),
    "Beauty": (1, 5),
    "Grocery": (1, 12),
}

order_statuses = [
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled",
    "Returned",
]

order_status_weights = [
    0.70,
    0.12,
    0.08,
    0.06,
    0.04,
]

START_DATE = date(2024, 1, 1)
END_DATE = date(2025, 12, 31)

DATE_RANGE_DAYS = (END_DATE - START_DATE).days

orders = []

for order_id in range(1, 10001):
    selected_customer = random.choice(customers)
    selected_product = random.choice(products)

    category = selected_product["category"]
    unit_price = selected_product["price"]

    minimum_quantity, maximum_quantity = quantity_ranges[category]

    quantity = random.randint(
        minimum_quantity,
        maximum_quantity,
    )

    order_status = random.choices(
        order_statuses,
        weights=order_status_weights,
        k=1,
    )[0]

    total_amount = round(quantity * unit_price, 2)

    # Cancelled orders do not contribute to completed revenue.
    if order_status == "Cancelled":
        total_amount = 0.00

    order_date = START_DATE + timedelta(
        days=random.randint(0, DATE_RANGE_DAYS)
    )

    order = {
        "order_id": order_id,
        "customer_id": selected_customer["customer_id"],
        "product_id": selected_product["product_id"],
        "quantity": quantity,
        "unit_price": unit_price,
        "total_amount": total_amount,
        "order_date": order_date,
        "order_status": order_status,
        "shipping_city": selected_customer["city"],
        "shipping_state": selected_customer["state"],
    }

    orders.append(order)

orders_df = pd.DataFrame(orders)

orders_df.to_csv(
    RAW_DATA_PATH / "orders.csv",
    index=False,
)

print()
print(f"Generated {len(orders)} orders")
print("orders.csv created successfully!")


# ---------------------------------------------------------
# DATA VALIDATION
# ---------------------------------------------------------

valid_customer_ids = set(customers_df["customer_id"])
valid_product_ids = set(products_df["product_id"])

invalid_customer_orders = orders_df[
    ~orders_df["customer_id"].isin(valid_customer_ids)
]

invalid_product_orders = orders_df[
    ~orders_df["product_id"].isin(valid_product_ids)
]

duplicate_customer_ids = customers_df["customer_id"].duplicated().sum()
duplicate_product_ids = products_df["product_id"].duplicated().sum()
duplicate_order_ids = orders_df["order_id"].duplicated().sum()

print()
print("Data validation results:")
print(f"Invalid customer references: {len(invalid_customer_orders)}")
print(f"Invalid product references: {len(invalid_product_orders)}")
print(f"Duplicate customer IDs: {duplicate_customer_ids}")
print(f"Duplicate product IDs: {duplicate_product_ids}")
print(f"Duplicate order IDs: {duplicate_order_ids}")

print()
print("Order status distribution:")
print(orders_df["order_status"].value_counts())

print()
print("Retail data generation completed successfully!")
# ---------------------------------------------------------
# GENERATE PAYMENTS
# ---------------------------------------------------------

payment_methods = [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "Digital Wallet",
    "Gift Card",
]

payment_method_weights = [
    0.35,
    0.25,
    0.15,
    0.20,
    0.05,
]

payments = []
payment_id = 1

for order in orders:

    order_id = order["order_id"]
    order_total = order["total_amount"]
    order_date = order["order_date"]
    order_status = order["order_status"]

    # Skip cancelled orders
    if order_status == "Cancelled":
        continue

    payment_scenario = random.choices(
        ["single", "retry", "split"],
        weights=[0.90, 0.08, 0.02],
        k=1
    )[0]

    payment_date = order_date + timedelta(
        days=random.randint(0, 2)
    )

    # -----------------------------------------------------
    # SINGLE SUCCESSFUL PAYMENT
    # -----------------------------------------------------

    if payment_scenario == "single":

        payment_method = random.choices(
            payment_methods,
            weights=payment_method_weights,
            k=1
        )[0]

        payment = {
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": payment_date,
            "payment_method": payment_method,
            "payment_amount": order_total,
            "payment_status": "Successful",
            "transaction_reference": fake.uuid4(),
            "payment_attempt": 1
        }

        payments.append(payment)
        payment_id += 1

    # -----------------------------------------------------
    # FAILED PAYMENT THEN SUCCESSFUL RETRY
    # -----------------------------------------------------

    elif payment_scenario == "retry":

        first_method = random.choices(
            payment_methods,
            weights=payment_method_weights,
            k=1
        )[0]

        failed_payment = {
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": payment_date,
            "payment_method": first_method,
            "payment_amount": order_total,
            "payment_status": "Failed",
            "transaction_reference": fake.uuid4(),
            "payment_attempt": 1
        }

        payments.append(failed_payment)
        payment_id += 1

        second_method = random.choices(
            payment_methods,
            weights=payment_method_weights,
            k=1
        )[0]

        successful_payment = {
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": payment_date + timedelta(days=1),
            "payment_method": second_method,
            "payment_amount": order_total,
            "payment_status": "Successful",
            "transaction_reference": fake.uuid4(),
            "payment_attempt": 2
        }

        payments.append(successful_payment)
        payment_id += 1

    # -----------------------------------------------------
    # SPLIT PAYMENT
    # -----------------------------------------------------

    else:

        first_amount = round(
            order_total * random.uniform(0.20, 0.80),
            2
        )

        second_amount = round(
            order_total - first_amount,
            2
        )

        first_payment = {
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": payment_date,
            "payment_method": "Gift Card",
            "payment_amount": first_amount,
            "payment_status": "Successful",
            "transaction_reference": fake.uuid4(),
            "payment_attempt": 1
        }

        payments.append(first_payment)
        payment_id += 1

        second_payment = {
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": payment_date,
            "payment_method": random.choice([
                "Credit Card",
                "Debit Card",
                "PayPal",
                "Digital Wallet"
            ]),
            "payment_amount": second_amount,
            "payment_status": "Successful",
            "transaction_reference": fake.uuid4(),
            "payment_attempt": 1
        }

        payments.append(second_payment)
        payment_id += 1


payments_df = pd.DataFrame(payments)

payments_df.to_csv(
    RAW_DATA_PATH / "payments.csv",
    index=False
)

print()
print(f"Generated {len(payments)} payment records")
print("payments.csv created successfully!")
# ---------------------------------------------------------
# PAYMENT VALIDATION
# ---------------------------------------------------------

valid_order_ids = set(orders_df["order_id"])

invalid_payment_orders = payments_df[
    ~payments_df["order_id"].isin(valid_order_ids)
]

duplicate_payment_ids = payments_df[
    "payment_id"
].duplicated().sum()

print()
print("Payment validation results:")
print(f"Invalid payment order references: {len(invalid_payment_orders)}")
print(f"Duplicate payment IDs: {duplicate_payment_ids}")

print()
print("Payment status distribution:")
print(payments_df["payment_status"].value_counts())

print()
print("Payment method distribution:")
print(payments_df["payment_method"].value_counts())

# ============================================================
# PAYMENT DATA GENERATION
# ============================================================

payment_methods = [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "Gift Card",
    "Amazon Pay",
]

# Payment scenarios:
# 90% -> one successful payment
# 8%  -> failed attempt followed by a successful retry
# 2%  -> split payment across two payment methods
SINGLE_PAYMENT_PROB = 0.90
RETRY_PROB = 0.08

payments = []
payment_id = 1


for order in orders:
    order_id = order["order_id"]
    order_total = round(float(order["total_amount"]), 2)
    order_status = order["order_status"]

    # Convert order_date to a datetime value so timedelta works safely
    order_date = pd.to_datetime(order["order_date"])

    # Cancelled orders have no completed payment
    if order_status == "Cancelled":
        continue

    scenario_roll = random.random()

    # --------------------------------------------------------
    # Scenario 1: Single successful payment
    # --------------------------------------------------------
    if scenario_roll < SINGLE_PAYMENT_PROB:
        payment_method = random.choice(payment_methods)

        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": order_date,
            "payment_method": payment_method,
            "payment_amount": order_total,
            "payment_status": "Successful",
            "transaction_reference": f"txn_{uuid.uuid4().hex}",
            "payment_attempt": 1,
            "parent_payment_id": None,
        })

        payment_id += 1

    # --------------------------------------------------------
    # Scenario 2: Failed payment followed by successful retry
    # --------------------------------------------------------
    elif scenario_roll < SINGLE_PAYMENT_PROB + RETRY_PROB:
        payment_method = random.choice(payment_methods)

        # First failed attempt
        failed_payment_id = payment_id

        payments.append({
            "payment_id": failed_payment_id,
            "order_id": order_id,
            "payment_date": order_date,
            "payment_method": payment_method,
            "payment_amount": order_total,
            "payment_status": "Failed",
            "transaction_reference": f"txn_{uuid.uuid4().hex}",
            "payment_attempt": 1,
            "parent_payment_id": None,
        })

        payment_id += 1

        # Successful retry within 0–2 days
        retry_date = order_date + timedelta(
            days=random.randint(0, 2)
        )

        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": retry_date,
            "payment_method": payment_method,
            "payment_amount": order_total,
            "payment_status": "Successful",
            "transaction_reference": f"txn_{uuid.uuid4().hex}",
            "payment_attempt": 2,
            "parent_payment_id": failed_payment_id,
        })

        payment_id += 1

    # --------------------------------------------------------
    # Scenario 3: Split payment across two payment methods
    # --------------------------------------------------------
    else:
        split_fraction = random.uniform(0.20, 0.80)

        first_amount = round(order_total * split_fraction, 2)
        second_amount = round(order_total - first_amount, 2)

        method_1, method_2 = random.sample(
            payment_methods,
            2
        )

        # First portion
        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": order_date,
            "payment_method": method_1,
            "payment_amount": first_amount,
            "payment_status": "Successful",
            "transaction_reference": f"txn_{uuid.uuid4().hex}",
            "payment_attempt": 1,
            "parent_payment_id": None,
        })

        payment_id += 1

        # Second portion
        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": order_date,
            "payment_method": method_2,
            "payment_amount": second_amount,
            "payment_status": "Successful",
            "transaction_reference": f"txn_{uuid.uuid4().hex}",
            "payment_attempt": 1,
            "parent_payment_id": None,
        })

        payment_id += 1


# ============================================================
# CREATE PAYMENTS DATAFRAME
# ============================================================

payments_df = pd.DataFrame(payments)

payments_df["payment_date"] = pd.to_datetime(
    payments_df["payment_date"]
).dt.strftime("%Y-%m-%d")


# ============================================================
# PAYMENT DATA VALIDATION
# ============================================================

# 1. Validate payment_id uniqueness
assert payments_df["payment_id"].is_unique, (
    "Validation failed: duplicate payment IDs found."
)

# 2. Validate transaction_reference uniqueness
assert payments_df["transaction_reference"].is_unique, (
    "Validation failed: duplicate transaction references found."
)

# 3. Validate required fields
required_payment_columns = [
    "payment_id",
    "order_id",
    "payment_date",
    "payment_method",
    "payment_amount",
    "payment_status",
    "transaction_reference",
    "payment_attempt",
]

assert not payments_df[required_payment_columns].isnull().any().any(), (
    "Validation failed: required payment fields contain null values."
)

# 4. Validate payment statuses
valid_payment_statuses = {
    "Successful",
    "Failed",
}

invalid_status_rows = payments_df[
    ~payments_df["payment_status"].isin(valid_payment_statuses)
]

assert invalid_status_rows.empty, (
    "Validation failed: invalid payment statuses found."
)

# 5. Validate payment methods
invalid_method_rows = payments_df[
    ~payments_df["payment_method"].isin(payment_methods)
]

assert invalid_method_rows.empty, (
    "Validation failed: invalid payment methods found."
)

# 6. Validate positive payment amounts
invalid_amount_rows = payments_df[
    payments_df["payment_amount"] <= 0
]

assert invalid_amount_rows.empty, (
    "Validation failed: zero or negative payment amounts found."
)

# 7. Validate payment order references
orders_df = pd.DataFrame(orders)

valid_order_ids = set(orders_df["order_id"])

invalid_order_references = payments_df[
    ~payments_df["order_id"].isin(valid_order_ids)
]

assert invalid_order_references.empty, (
    "Validation failed: payments contain invalid order IDs."
)

# 8. Validate cancelled orders have no payments
cancelled_order_ids = set(
    orders_df.loc[
        orders_df["order_status"] == "Cancelled",
        "order_id"
    ]
)

cancelled_order_payments = payments_df[
    payments_df["order_id"].isin(cancelled_order_ids)
]

assert cancelled_order_payments.empty, (
    "Validation failed: cancelled orders contain payments."
)

# 9. Validate retry relationships
retry_rows = payments_df[
    payments_df["payment_attempt"] > 1
]

assert retry_rows["parent_payment_id"].notna().all(), (
    "Validation failed: retry payments are missing parent_payment_id."
)

original_payment_ids = set(payments_df["payment_id"])

invalid_parent_rows = retry_rows[
    ~retry_rows["parent_payment_id"].isin(original_payment_ids)
]

assert invalid_parent_rows.empty, (
    "Validation failed: invalid parent payment references found."
)

# 10. Reconcile successful payments with order totals
non_cancelled_orders = orders_df[
    orders_df["order_status"] != "Cancelled"
].copy()

non_cancelled_orders["total_amount"] = (
    non_cancelled_orders["total_amount"]
    .astype(float)
    .round(2)
)

expected_order_totals = (
    non_cancelled_orders
    .set_index("order_id")["total_amount"]
)

successful_payment_totals = (
    payments_df[
        payments_df["payment_status"] == "Successful"
    ]
    .groupby("order_id")["payment_amount"]
    .sum()
    .round(2)
)

reconciliation_df = pd.concat(
    [
        expected_order_totals.rename("order_total"),
        successful_payment_totals.rename(
            "successful_payment_total"
        ),
    ],
    axis=1,
).fillna(0)

reconciliation_df["difference"] = (
    reconciliation_df["order_total"]
    - reconciliation_df["successful_payment_total"]
).abs()

reconciliation_errors = reconciliation_df[
    reconciliation_df["difference"] > 0.01
]

assert reconciliation_errors.empty, (
    "Payment reconciliation failed.\n"
    f"{reconciliation_errors.head(10)}"
)


# ============================================================
# SAVE PAYMENTS CSV
# ============================================================

payments_output_path = RAW_DATA_PATH / "payments.csv"

payments_df.to_csv(
    payments_output_path,
    index=False,
)


# ============================================================
# SUMMARY
# ============================================================

successful_count = (
    payments_df["payment_status"] == "Successful"
).sum()

failed_count = (
    payments_df["payment_status"] == "Failed"
).sum()

retry_count = (
    payments_df["payment_attempt"] == 2
).sum()

split_order_count = (
    payments_df[
        payments_df["payment_status"] == "Successful"
    ]
    .groupby("order_id")
    .size()
    .gt(1)
    .sum()
)

print("\nPayment generation completed!")
print(f"Total non-cancelled orders: {len(non_cancelled_orders)}")
print(f"Total payment records: {len(payments_df)}")
print(f"Successful payment records: {successful_count}")
print(f"Failed payment records: {failed_count}")
print(f"Successful retries: {retry_count}")
print(f"Split-payment orders: {split_order_count}")
print("All payment validations passed!")
print(f"payments.csv saved to: {payments_output_path}")
# ============================================================
# INVENTORY DATA GENERATION
# ============================================================

warehouses = [
    "Dallas",
    "Chicago",
    "Atlanta",
    "Phoenix",
]

inventory = []
inventory_id = 1

for product in products:
    product_id = product["product_id"]

    # Assign each product to 1–3 distinct warehouses
    num_warehouses = random.randint(1, 3)

    assigned_warehouses = random.sample(
        warehouses,
        num_warehouses,
    )

    for warehouse in assigned_warehouses:
        stock_quantity = random.randint(10, 500)
        reorder_level = random.randint(10, 50)

        days_since_restock = random.randint(0, 90)

        last_restock_date = (
            date.today()
            - timedelta(days=days_since_restock)
        )

        inventory.append({
            "inventory_id": inventory_id,
            "product_id": product_id,
            "warehouse": warehouse,
            "stock_quantity": stock_quantity,
            "reorder_level": reorder_level,
            "last_restock_date": last_restock_date,
        })

        inventory_id += 1


inventory_df = pd.DataFrame(inventory)

inventory_df["last_restock_date"] = (
    pd.to_datetime(inventory_df["last_restock_date"])
    .dt.strftime("%Y-%m-%d")
)
# Validate inventory_id uniqueness
assert inventory_df["inventory_id"].is_unique, \
    "Duplicate inventory IDs found"

# Validate (product_id, warehouse) uniqueness
assert not inventory_df.duplicated(
    subset=["product_id", "warehouse"]
).any(), \
    "Duplicate product/warehouse combinations found"

# Validate valid product IDs
valid_product_ids = {p["product_id"] for p in products}

assert inventory_df["product_id"].isin(valid_product_ids).all(), \
    "Invalid product IDs found"

# Validate positive stock
assert (inventory_df["stock_quantity"] > 0).all(), \
    "Invalid stock quantities"

# Validate positive reorder levels
assert (inventory_df["reorder_level"] > 0).all(), \
    "Invalid reorder levels"

print("Inventory validation passed!")
inventory_output_path = RAW_DATA_PATH / "inventory.csv"

inventory_df.to_csv(
    inventory_output_path,
    index=False,
)

print()
print(f"Generated {len(inventory_df)} inventory records")
print("inventory.csv created successfully!")
print(f"inventory.csv saved to: {inventory_output_path}")