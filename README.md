# 🛒 Event-Driven Retail Analytics Platform

[![CI](https://github.com/Sowmyakandi/retail-analytics-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/Sowmyakandi/retail-analytics-platform/actions/workflows/ci.yml)

An end-to-end retail analytics pipeline built around AWS, Snowflake, dbt, and Airflow. It generates synthetic retail data, lands it in S3, transforms it through an event-driven Glue pipeline, and models it in dbt for reporting.

---

# 📌 Project Overview

This project simulates a production-grade retail analytics pipeline: data generation, event-driven ingestion, PySpark transformation, and dbt modeling, with Snowflake and Power BI as the intended production warehouse/BI layer.

The pipeline processes retail data including:

- Customers
- Products
- Orders
- Payments
- Inventory

---

# ✅ Status: What's implemented vs. planned

| Component | Status |
|---|---|
| Synthetic data generator (`scripts/generate_retail_data.py`) | Implemented — generates 1,000 customers, 200 products, 10,000 orders, ~10,400 payments, ~400 inventory rows |
| Lambda trigger (`lambda/lambda_function.py`) | Implemented — starts the Glue crawler on `raw/` uploads |
| Glue ETL job (`glue_etl/retail_etl_job.py`) | Implemented — dedup, null handling, type casting, revenue reconciliation, enrichment join |
| Airflow DAG (`airflow/retail_pipeline_dag.py`) | Implemented — orchestrates S3 sensor → crawler → Glue ETL |
| dbt staging + mart models (`retail_dbt/`) | Implemented — 5 staging models, 5 marts, 30 schema tests. Runnable locally/in CI against DuckDB with no cloud credentials (see below), or against Snowflake in production |
| CI (`.github/workflows/ci.yml`) | Implemented — lints Python, runs `dbt build` on every push/PR |
| S3 → Lambda event wiring | Implemented — S3 upload events under `raw/` trigger the Lambda directly, which starts the AWS Glue Crawler for new raw uploads.
| Snowflake warehouse | Implemented — Snowflake warehouse configured with RETAIL_ANALYTICS database, RAW and MART schemas, dimensional models (DIM_CUSTOMERS, DIM_PRODUCTS, FACT_ORDERS), and analytical SQL queries for reporting.
| Power BI dashboard | Implemented — interactive Power BI dashboard (`powerbi/Retail_Analytics_Dashboard.pbix`) included along with screenshots in the `/screenshots` folder. Dashboard includes KPI cards, monthly revenue trends, top customers, top products, order status distribution, and geographic sales analysis. |

---

# 🏗️ Architecture 
See `architecture/architecture.md` for the full Mermaid diagram.

---

# 🚀 Technology Stack

### Cloud
- AWS S3, Lambda, Glue

### Data Warehouse
- Snowflake (production) / DuckDB (local dev + CI, via dbt seeds)

### Transformation
- dbt, PySpark, SQL

### Orchestration
- Apache Airflow

### Visualization
- Power BI

---

# 📂 Repository Structure 
---

# 🔄 Data Pipeline

1. Generate retail datasets using Python (`scripts/generate_retail_data.py`).
2. Upload raw CSV files to Amazon S3 under `raw/`.
3. S3 triggers an ObjectCreated event that invokes the Lambda directly.
4. Lambda starts the Glue crawler.
5. Glue ETL (PySpark) cleans, deduplicates, and enriches the data.
6. Processed Parquet lands back in S3, then loads into Snowflake.
7. dbt builds staging and mart models on top of it.
8. Power BI connects to Snowflake for reporting.

---

# 🧪 Getting Started (local dev)

```bash
# Python deps for the data generator / Lambda
pip install -r requirements.txt

# Generate fresh synthetic data (optional -- data/raw/ already has sample data)
python scripts/generate_retail_data.py

# dbt: build and test everything against DuckDB, no cloud credentials needed
cd retail_dbt
pip install -r requirements.txt
dbt seed --profiles-dir ./ci_profiles
dbt run  --profiles-dir ./ci_profiles
dbt test --profiles-dir ./ci_profiles
```

To target the real Snowflake warehouse instead, set the `SNOWFLAKE_*` environment variables (see `.env.example`) and run dbt with `--target prod` against the profile in `retail_dbt/../profiles.yml` (not checked in — configure locally or via CI secrets).

Lint:

```bash
pip install ruff
ruff check lambda/ glue_etl/ airflow/ scripts/
```

---

# 🗃️ dbt Models

**Staging** (`retail_dbt/models/staging/`): `stg_customers`, `stg_products`, `stg_orders`, `stg_payments`, `stg_inventory` — 1:1 cleaned views over the raw sources, with type casting and a `revenue_difference` / `has_revenue_mismatch` check on orders.

**Marts** (`retail_dbt/models/marts/`): `dim_customers` (with lifetime order/revenue rollups), `dim_products` (with stock position), `fct_orders` (enriched with payment status), `fct_payments`, `fct_inventory`.

30 schema tests (`unique`, `not_null`, `relationships`, `accepted_values`) run on every CI build.

---

# 🔐 Configuration

No AWS account IDs or bucket names are hardcoded in source. The Glue job reads its output path from a `--OUTPUT_S3_PATH` job parameter, and the Airflow DAG reads the bucket name from an Airflow Variable (`retail_analytics_bucket_name`) or the `RETAIL_ANALYTICS_BUCKET_NAME` environment variable. See `.env.example` for the full list of configuration values.

---

# 📊 Dashboard Metrics

The Power BI dashboard surfaces: total revenue, total orders, total customers, average order value, monthly revenue trend, order status distribution, top products by revenue, top customers, and sales by state — computed from `fct_orders` / `dim_customers` / `dim_products`.

---

# 👩‍💻 Author

**Sowmya Kandi**