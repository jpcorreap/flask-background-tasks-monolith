import os

from dotenv import load_dotenv
from kombu.utils.url import safequote
import requests

load_dotenv()


# def get_access_keys():
#     response = requests.get(
#         "http://169.254.169.254/latest/meta-data/iam/security-credentials/LabRole"
#     )
#     response_json = response.json()
#     access_key = response_json.get("AccessKeyId")
#     secret_access_key = response_json.get("SecretAccessKey")
#     return access_key, secret_access_key


class Config(object):
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{PG_USER}:{PG_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    )
    JWT_SECRET_KEY = os.getenv("SECRET")
    PROPAGATE_EXCEPTIONS = True
    PROCESSING_FOLDER_PATH = "converter/in_process"
    PROCESSED_FOLDER_PATH = "converter/processed"
    BANNER_FOLDER_PATH = "img/banner"
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_SERVER_PORT = os.getenv("EMAIL_SERVER_PORT")
    EMAIL_SERVER_HOST = os.getenv("EMAIL_SERVER_HOST")
    SENDGRID_USER = os.getenv("SENDGRID_USER")
    SENDGRID_SECRET = os.getenv("SENDGRID_SECRET")
    PYNAMO_HOST = os.getenv("PYNAMO_HOST", "http://localhost:8000")
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", "")
    CELERY_BROKER_TRANSPORT_OPTIONS = {
        "region": "us-east-1",
        "predefined_queues": {
            "supervoices7": {
                "url": "https://sqs.us-east-1.amazonaws.com/833464877364/supervoices7.fifo"
            }
        },
    }
    BROKER_URL = (
        f"sqs://{safequote(AWS_ACCESS_KEY_ID)}:{safequote(AWS_SECRET_ACCESS_KEY)}@"
    )


config = Config()
for dir in [
    config.PROCESSED_FOLDER_PATH,
    config.PROCESSING_FOLDER_PATH,
    config.BANNER_FOLDER_PATH,
]:
    subdirs = dir.split("/")
    for pos in range(len(subdirs)):
        curr_dir = "/".join(subdirs[: pos + 1])
        if not os.path.exists(curr_dir):
            os.mkdir(curr_dir)
