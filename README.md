# 🛒 Event-Driven Retail Analytics Platform

An end-to-end cloud-based Retail Analytics Platform built using AWS, Snowflake, dbt, Airflow, Python, SQL, and Power BI. This project demonstrates how raw retail data is ingested, transformed, modeled, and visualized to generate actionable business insights.

---

# 📌 Project Overview

This project simulates a production-grade retail analytics pipeline that automates data ingestion, transformation, warehousing, and reporting.

The pipeline processes retail data including:

- Customers
- Products
- Orders
- Payments
- Inventory

The transformed data is loaded into Snowflake, modeled using dbt, and visualized in Power BI.

---

# 🏗️ Architecture

```
CSV Files
     │
     ▼
Amazon S3 (Raw Layer)
     │
     ▼
S3 Event Notification
     │
     ▼
SNS Topic
     │
     ▼
SQS Queue
     │
     ▼
AWS Lambda
     │
     ▼
AWS Glue Crawler
     │
     ▼
AWS Glue ETL (PySpark)
     │
     ▼
Amazon S3 (Processed)
     │
     ▼
Snowflake Data Warehouse
     │
     ▼
dbt Transformations
     │
     ▼
Power BI Dashboard
```

---

# 🚀 Technology Stack

### Cloud
- AWS S3
- AWS Lambda
- AWS Glue
- Amazon SNS
- Amazon SQS

### Data Warehouse
- Snowflake

### Transformation
- dbt
- PySpark
- SQL

### Programming
- Python

### Orchestration
- Apache Airflow

### Visualization
- Power BI

### Version Control
- Git
- GitHub

---

# 📂 Repository Structure

```
airflow/
architecture/
data/
glue_etl/
lambda/
retail_dbt/
scripts/
powerbi/
screenshots/
```

---

# 🔄 Data Pipeline

1. Generate retail datasets using Python.
2. Upload raw CSV files to Amazon S3.
3. S3 triggers SNS notification.
4. SNS forwards messages to SQS.
5. Lambda starts AWS Glue Crawler.
6. Glue ETL cleans and transforms data.
7. Processed data is loaded into Snowflake.
8. dbt builds analytical models.
9. Power BI connects to Snowflake for reporting.

---

# 📊 Dashboard Metrics

The Power BI dashboard includes:

- Total Revenue
- Total Orders
- Total Customers
- Average Order Value
- Monthly Revenue Trend
- Order Status Distribution
- Top Products by Revenue
- Top Customers
- Sales by State

---

# 📈 Business Insights

The platform enables business users to:

- Track sales performance
- Monitor customer purchasing behavior
- Identify top-selling products
- Analyze monthly revenue trends
- Measure order fulfillment status
- Support executive decision-making

---

# 🛠️ Tools & Technologies

- Python
- SQL
- AWS S3
- AWS Lambda
- AWS Glue
- AWS SNS
- AWS SQS
- Snowflake
- dbt
- Apache Airflow
- Power BI
- Git
- GitHub

---

# 👩‍💻 Author

**Sowmya Kandi**