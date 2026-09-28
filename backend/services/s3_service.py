import os

import boto3

from dotenv import load_dotenv


load_dotenv()


s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)


BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME"
)


def upload_file(
    file_object,
    s3_key
):

    s3.upload_fileobj(
        file_object,
        BUCKET_NAME,
        s3_key
    )

    return s3_key


def download_file(
    s3_key,
    local_path
):

    s3.download_file(
        BUCKET_NAME,
        s3_key,
        local_path
    )