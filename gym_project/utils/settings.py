import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_test: str = (
        str(os.environ.get("GYM_DB_TEST"))
        if os.environ.get("GYM_DB_TEST")
        else "sqlite+aiosqlite:///gym_test.db"
    )
    db_prod: str = str(os.environ.get("GYM_DB_PROD"))
    ambiente: str = (
        str(os.environ.get("GYM_AMBIENTE"))
        if os.environ.get("GYM_AMBIENTE")
        else "TEST"
    )
    secret_key: str = (
        str(os.environ.get("GYM_ACCESS_TOKEN"))
        if os.environ.get("GYM_ACCESS_TOKEN")
        else "TEST_SECRET"
    )
    refresh_secret_key: str = (
        str(os.environ.get("GYM_REFRESH_TOKEN"))
        if os.environ.get("GYM_REFRESH_TOKEN")
        else "TEST_REFRESH"
    )
    secret_expires: int = 7200
    refresh_expires: int = 3600
