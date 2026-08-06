import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType

args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "OUTPUT_S3_PATH"],
)

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

DATABASE = "retail_analytics_db"
# Passed in as a --OUTPUT_S3_PATH job parameter (e.g. from Terraform/CDK or
# the Glue console), e.g. "s3://<your-bucket>/processed". Keeping the bucket
# name out of source avoids baking an AWS account ID into the repo.
OUTPUT_BASE = args["OUTPUT_S3_PATH"].rstrip("/")


def read_catalog_table(table_name: str):
    return glue_context.create_dynamic_frame.from_catalog(
        database=DATABASE,
        table_name=table_name,
    ).toDF()


def clean_column_names(df):
    for column in df.columns:
        df = df.withColumnRenamed(column, column.strip().lower())
    return df


customers = clean_column_names(read_catalog_table("customers"))
products = clean_column_names(read_catalog_table("products"))
orders = clean_column_names(read_catalog_table("orders"))
payments = clean_column_names(read_catalog_table("payments"))
inventory = clean_column_names(read_catalog_table("inventory"))

customers = customers.dropDuplicates(["customer_id"])
products = products.dropDuplicates(["product_id"])
orders = orders.dropDuplicates(["order_id"])
payments = payments.dropDuplicates(["payment_id"])
inventory = inventory.dropDuplicates(["inventory_id"])

customers = customers.dropna(subset=["customer_id"])
products = products.dropna(subset=["product_id"])
orders = orders.dropna(subset=["order_id", "customer_id", "product_id"])
payments = payments.dropna(subset=["payment_id", "order_id"])
inventory = inventory.dropna(subset=["inventory_id", "product_id"])

orders = (
    orders.withColumn("order_date", F.to_date("order_date"))
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn("unit_price", F.col("unit_price").cast(DecimalType(12, 2)))
    .withColumn("total_amount", F.col("total_amount").cast(DecimalType(14, 2)))
    .withColumn(
        "calculated_total_amount",
        F.round(F.col("quantity") * F.col("unit_price"), 2).cast(
            DecimalType(14, 2)
        ),
    )
    .withColumn(
        "revenue_difference",
        F.round(
            F.col("total_amount") - F.col("calculated_total_amount"),
            2,
        ).cast(DecimalType(14, 2)),
    )
)

payments = (
    payments.withColumn("payment_date", F.to_date("payment_date"))
    .withColumn(
        "payment_amount",
        F.col("payment_amount").cast(DecimalType(14, 2)),
    )
)

inventory = (
    inventory.withColumn("stock_quantity", F.col("stock_quantity").cast("int"))
    .withColumn("reorder_level", F.col("reorder_level").cast("int"))
    .withColumn("last_restock_date", F.to_date("last_restock_date"))
)

enriched_orders = (
    orders.alias("o")
    .join(
        customers.alias("c"),
        F.col("o.customer_id") == F.col("c.customer_id"),
        "left",
    )
    .join(
        products.alias("p"),
        F.col("o.product_id") == F.col("p.product_id"),
        "left",
    )
    .select(
        F.col("o.*"),
        F.col("c.full_name"),
        F.col("c.email"),
        F.col("c.city").alias("customer_city"),
        F.col("c.state").alias("customer_state"),
        F.col("p.product_name"),
        F.col("p.category"),
        F.col("p.brand"),
    )
)

outputs = {
    "customers": customers,
    "products": products,
    "orders": orders,
    "payments": payments,
    "inventory": inventory,
    "enriched_orders": enriched_orders,
}

for name, df in outputs.items():
    (
        df.write.mode("overwrite")
        .format("parquet")
        .save(f"{OUTPUT_BASE}/{name}/")
    )

job.commit()