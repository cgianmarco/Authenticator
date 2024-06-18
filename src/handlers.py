from typing import Any
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.requests import Request

from constants import Messages
from entity import *

class ErrorHandler:
    def __call__(self, request: Request, exc: Exception) -> Any:
        print(exc.with_traceback)


class CredentialsErrorHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=BasicResponse(success=False, message=exc.message).model_dump(),
        )


class UserAlreadyExistsHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=BasicResponse(success=False, message=exc.message).model_dump(),
        )


class ValidationExceptionHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BasicResponse(success=False, message=Messages.VALIDATION_ERROR).model_dump(),
        )


class RateExceptionHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content=BasicResponse(success=False, message=exc.message).model_dump(),
        )


class ServerErrorHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=BasicResponse(success=False, message=Messages.INTERNAL_SERVER_ERROR).model_dump(),
        )
