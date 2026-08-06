# Retail Analytics Platform Architecture

```mermaid
flowchart TD
    A[Python Data Generator] --> B[Raw CSV Files]

    B --> C[Amazon S3 Raw Layer]
    C --> D[S3 ObjectCreated Event]

    D --> E[AWS Lambda]
    E --> F[AWS Glue Crawler]

    F --> G[AWS Glue Data Catalog]
    G --> H[AWS Glue ETL Job - PySpark]

    H --> I[Clean and Transform Data]
    I --> J[Deduplicate Records]
    I --> K[Handle Null Values]
    I --> L[Standardize Dates]
    I --> M[Validate Revenue]
    I --> N[Join Orders Customers Products]

    J --> O[Amazon S3 Processed Layer - Parquet]
    K --> O
    L --> O
    M --> O
    N --> O

    O --> P[Snowflake]
    P --> Q[dbt Staging Models]
    Q --> R[dbt Dimension Models]
    Q --> S[dbt Fact Models]
    R --> T[SQL Analytics]
    S --> T

    T --> U[Power BI Executive Dashboard]

    V[Apache Airflow] --> F
    V --> H
    V --> P
    V --> Q