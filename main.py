from fastapi import FastAPI

from handlers import *
from exceptions import *
from middleware import RateLimitMiddleware
from config import Config
from routers import authenticator_router_v1

app = FastAPI()

app.add_exception_handler(InvalidCredentialsError, CredentialsErrorHandler())
app.add_exception_handler(UserAlreadyExistsError, UserAlreadyExistsHandler())
app.add_exception_handler(RequestValidationError, ValidationExceptionHandler())
app.add_exception_handler(RateLimitError, RateExceptionHandler())
app.add_exception_handler(Exception, ServerErrorHandler())

if Config.RATE_LIMIT_ENABLED:
    app.add_middleware(RateLimitMiddleware)

app.include_router(authenticator_router_v1.router, prefix="/v1")
