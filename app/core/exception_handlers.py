from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import AppException


async def app_exception_handler(request: Request,
                                exc: AppException) -> JSONResponse:
    return JSONResponse(
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )
