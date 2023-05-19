from fastapi import HTTPException, status

class RaiseErrorGym:

    def __init__(self, status_code: int, message: str = None):
        self.status_code = status_code
        if message:
            raise HTTPException(status_code, message)

        raise HTTPException(status_code)
