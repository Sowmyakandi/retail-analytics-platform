import os
from datetime import datetime, timedelta

from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

from airflow import DAG

# Resolved from an Airflow Variable (set in the Airflow UI / CLI) with an
# environment-variable fallback, so the S3 bucket name -- and the AWS
# account ID embedded in it -- never has to be committed to source control.
BUCKET_NAME = Variable.get(
    "retail_analytics_bucket_name",
    default_var=os.environ.get("RETAIL_ANALYTICS_BUCKET_NAME", "REPLACE_ME"),
)
RAW_PREFIX = "raw/"
CRAWLER_NAME = "retail-analytics-crawler"
GLUE_JOB_NAME = "retail-analytics-etl-job"

default_args = {
    "owner": "sowmya",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="retail_analytics_pipeline",
    description="Orchestrates S3 validation, Glue crawler, and Glue ETL processing",
    default_args=default_args,
    start_date=datetime(2026, 8, 1),
    schedule=None,
    catchup=False,
    tags=["retail", "aws", "glue", "data-engineering"],
) as dag:

    start = EmptyOperator(task_id="start")

    wait_for_raw_data = S3KeySensor(
        task_id="wait_for_raw_data",
        bucket_name=BUCKET_NAME,
        bucket_key=f"{RAW_PREFIX}*",
        wildcard_match=True,
        aws_conn_id="aws_default",
        poke_interval=30,
        timeout=600,
    )

    run_glue_crawler = GlueCrawlerOperator(
        task_id="run_glue_crawler",
        config={"Name": CRAWLER_NAME},
        aws_conn_id="aws_default",
    )

    run_glue_etl = GlueJobOperator(
        task_id="run_glue_etl",
        job_name=GLUE_JOB_NAME,
        script_args={"--OUTPUT_S3_PATH": f"s3://{BUCKET_NAME}/processed"},
        aws_conn_id="aws_default",
        wait_for_completion=False,
    )

    wait_for_glue_etl = GlueJobSensor(
        task_id="wait_for_glue_etl",
        job_name=GLUE_JOB_NAME,
        run_id="{{ ti.xcom_pull(task_ids='run_glue_etl') }}",
        aws_conn_id="aws_default",
        poke_interval=30,
        timeout=1800,
    )

    end = EmptyOperator(task_id="end")

    (
        start
        >> wait_for_raw_data
        >> run_glue_crawler
        >> run_glue_etl
        >> wait_for_glue_etl
        >> end
    )