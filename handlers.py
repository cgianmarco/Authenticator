from typing import Any
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.requests import Request


class ErrorHandler:
    def __call__(self, request: Request, exc: Exception) -> Any:
        print(exc.with_traceback)


class CredentialsErrorHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
            },
        )


class UserAlreadyExistsHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
            },
        )


class ValidationExceptionHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": exc.__class__.__name__,
                "message": "Validation error. Check the request payload.",
            },
        )


class RateExceptionHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
            },
        )


class ServerErrorHandler(ErrorHandler):
    def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        super().__call__(request, exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": exc.__class__.__name__,
                "message": "Internal server error.",
            },
        )
