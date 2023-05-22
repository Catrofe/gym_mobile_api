import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_test: str = str(os.environ.get("GYM_DB_TEST"))
    secret_key: str = str(os.environ.get("GYM_ACCESS_TOKEN"))
    refresh_secret_key: str = str(os.environ.get("GYM_REFRESH_TOKEN"))
    secret_expires: int = 7200
    refresh_expires: int = 3600
