import os

from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@0.0.0.0:5432/{os.getenv('DB_NAME')}"
JWT_SECRET_KEY = os.getenv("SECRET")
PROPAGATE_EXCEPTIONS = True
