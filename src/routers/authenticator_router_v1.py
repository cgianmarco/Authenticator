from functools import wraps
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from typing import Union

from middleware import RateLimitMiddleware
from services import AuthenticationService
from entity import *

router = APIRouter()


@router.post("/register")
async def register_user(
    userRegister: UserRegister,
    user_service: AuthenticationService = Depends(),
) -> BasicResponse:
    return await user_service.register(userRegister)


@router.post("/login", tags=["rate-limit"])
async def login(
    userLogin: UserLogin,
    user_service: AuthenticationService = Depends(),
) -> Union[TokenResponse, BasicResponse]:
    return await user_service.login(userLogin)


@router.post("/validate_otp", tags=["rate-limit"])
async def validate_otp(
    otpValidation: OTPValidation,
    user_service: AuthenticationService = Depends(),
) -> TokenResponse:
    return await user_service.validate_otp(otpValidation)


@router.get("/users")
async def get_users(
    user_service: AuthenticationService = Depends(),
):
    users = await user_service.get_all_users()
    return {"users": users}
