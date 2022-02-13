import os

from dotenv import load_dotenv

load_dotenv()

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
SQLALCHEMY_DB_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
JWT_SECRET_KEY = os.getenv("SECRET")
PROPAGATE_EXCEPTIONS = True
PROCESSING_FOLDER_PATH = "{}/converter/in_process".format(os.path.curdir)
UPLOAD_FOLDER = PROCESSING_FOLDER_PATH
PROCESSED_FOLDER_PATH = "{}/converter/processed".format(os.path.curdir)
