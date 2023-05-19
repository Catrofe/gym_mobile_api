from pydantic import BaseSettings


class Settings(BaseSettings):
    db_test: str = "sqlite+aiosqlite:///db.db"
    secret_key: str = "h#62yvKrzYjnIc7Cl1Pv%cWK5lkJb8uGTj2u%Phh8%hdnSE6#0"
    refresh_secret_key: str = "381iIFbg@Y1ndgcPvf*JQh6pq7Nqwb!oF9r3eHU1mPUpusVI9p"
    secret_expires: int = 7200
    refresh_expires: int = 3600
