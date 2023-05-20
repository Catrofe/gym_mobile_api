from fastapi import HTTPException


class RaiseErrorGym(BaseException):
    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        if message:
            raise HTTPException(status_code, message)

        raise HTTPException(status_code)
