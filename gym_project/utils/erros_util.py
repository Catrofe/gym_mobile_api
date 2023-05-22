from datetime import datetime
from typing import Optional, Union

from fastapi import HTTPException, Request


class RaiseErrorGym(BaseException):
    def __init__(
        self,
        request: Union[Request | None],
        status_code: int,
        message: str = "",
    ):
        self.status_code = status_code
        self.message = message
        if message:
            raise HTTPException(status_code, self.create_error_dict(request))

        raise HTTPException(status_code)

    def create_error_dict(
        self, request: Optional[Request]
    ) -> dict[str, Union[str | int]]:
        return {
            "statusCode": self.status_code,
            "messageCode": self.return_message_status_code(self.status_code),
            "message": self.message,
            "timestamp": str(datetime.now()),
            "path": request.url.path if request else "/api/gym/...",
        }

    def return_message_status_code(self, status_code: int) -> str:
        code = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            409: "Conflict",
            500: "Internal Server Error",
            503: "Service Unavailable",
        }
        return code[status_code]
