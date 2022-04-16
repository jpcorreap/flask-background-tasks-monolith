#from settings import config
import os
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "test-python-boto3-cloud"

def get_boto3_client(service_name: str):
    """
        :type service_name: string
        :param service_name: The name of a service, e.g. "s3" or "ec2". You
            can get a list of available services via
            :py:meth:`get_available_services`.
    """
    return boto3.client(
        service_name,
        aws_access_key_id="ASIA5TXLE3M66BCM2ZKR",
        aws_secret_access_key="m9/BJ3JCzGCgoDjWohZnpHLVr3uuCu2S7fhBufXp",
        aws_session_token="FwoGZXIvYXdzEAUaDAFF3+3vsTUrXSB/SyLKAS2LRRLAvrXCHWzu+vD+LDA8teZX3zBwQHqHX48AY1USvJgp93w+iGfx7+I4qI4puHsWz4W8Ko3dEiG1po0cQVKnNCLeOwRz2/4E4v8nRZ14g7IFWWllt4lboZ62TQ4gFSpqV+vdQM6G4h9T3SNzswEaJocIZyPSmnXsUwKkN18UqQlwBtSyFoFVwK959Mg0fmwNn0rocg4/i30/870HsPeWis4MAPiaMfprTlDqnJijrX+8HIEmXg88QnZ7SPQttCwFTi7c0Uaj/WYo0uTokgYyLTs5ZBux2pPZ4/NVy4zG+3Ncux61PUK6ItVCCza+naWfVGhJ7Cp8I6nhPWUTgA==",
        region_name="us-east-1"
    )
    if config.AWS_ACCESS_KEY and config.AWS_SECRET_KEY and config.AWS_SESSION_TOKEN and config.AWS_REGION_NAME:
        return boto3.client(
            service_name,
            aws_access_key_id=config.AWS_SECRET_KEY,
            aws_secret_access_key=config.AWS_ACCESS_KEY,
            aws_session_token=config.AWS_SESSION_TOKEN,
            region_name=config.AWS_REGION_NAME
        )
    else:
        # This will force boto3 to look into machine aws credentials
        return boto3.client(service_name)



def list_files_in_s3_bucket(bucket: str):
    s3_client = get_boto3_client("s3")
    response = s3_client.list_objects_v2(Bucket=bucket)
    keys=[]
    for content in response["Contents"]:
        obj_dict = s3_client.get_object(Bucket=bucket, Key=content["Key"])
        print(content["Key"], obj_dict["LastModified"])
        keys.append(content["Key"])
    return keys


def upload_file_to_s3(file, bucket, filename):
    """Upload a file to an S3 bucket

    :param file: File to upload
    :param bucket: Bucket to upload to
    :param filename: S3 object name
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = get_boto3_client("s3")
    try:
        s3_client.put_object(Body=file, Bucket=bucket, Key=filename)
    except ClientError as e:
        print(e)
        return False
    return True


def get_value():
    client = get_boto3_client("dynamodb")
    # Available methods:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html


def put_value():
    client = get_boto3_client("dynamodb")
    # Available methods:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html


print("ANTES:")
list_files_in_s3_bucket(BUCKET_NAME)

with open("./gala.png", "rb") as f:
    upload_file_to_s3(f, BUCKET_NAME, "mi archivo.png")

print("DESPUES:")
list_files_in_s3_bucket(BUCKET_NAME)