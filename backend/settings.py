import os

from dotenv import load_dotenv

load_dotenv()


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
    PROCESSING_FOLDER_PATH = "{}/converter/in_process".format(os.path.curdir)
    UPLOAD_FOLDER = PROCESSING_FOLDER_PATH
    PROCESSED_FOLDER_PATH = "{}/converter/processed".format(os.path.curdir)
    BANNER_FOLDER_PATH = "{}/img/banner".format(os.path.curdir)
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_SERVER_PORT = os.getenv("EMAIL_SERVER_PORT")
    EMAIL_SERVER_HOST = os.getenv("EMAIL_SERVER_HOST")


config = Config()
