from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import APIException


async def app_exception_handler(request: Request,
                                exc: APIException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )
