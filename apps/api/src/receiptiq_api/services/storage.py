import uuid

import boto3

from ..config import settings

_client = boto3.client(
    "s3",
    endpoint_url=settings.s3_endpoint_url,
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
)


def upload(data: bytes, filename: str) -> str:
    key = f"{uuid.uuid4()}-{filename}"
    _client.put_object(Bucket=settings.s3_bucket, Key=key, Body=data)
    return key
