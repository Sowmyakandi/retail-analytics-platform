import os
import urllib.parse

import boto3

glue = boto3.client("glue")

CRAWLER_NAME = os.environ.get(
    "CRAWLER_NAME",
    "retail-analytics-crawler",
)


def lambda_handler(event, context):
    """
    Triggered by an S3 ObjectCreated event.

    It checks whether the uploaded object is inside the raw/ prefix.
    If it is, the function starts the AWS Glue crawler.
    """

    processed_records = []

    for record in event.get("Records", []):
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )

        if not object_key.startswith("raw/"):
            processed_records.append(
                {
                    "bucket": bucket_name,
                    "key": object_key,
                    "action": "ignored",
                    "reason": "Object is outside raw/",
                }
            )
            continue

        try:
            glue.start_crawler(Name=CRAWLER_NAME)

            processed_records.append(
                {
                    "bucket": bucket_name,
                    "key": object_key,
                    "action": "crawler_started",
                    "crawler": CRAWLER_NAME,
                }
            )

        except glue.exceptions.CrawlerRunningException:
            processed_records.append(
                {
                    "bucket": bucket_name,
                    "key": object_key,
                    "action": "crawler_already_running",
                    "crawler": CRAWLER_NAME,
                }
            )

    return {
        "statusCode": 200,
        "processedRecords": processed_records,
    }