from fastapi import APIRouter, Depends
from typing import Union

from services import UserService
from entity import *

router = APIRouter()

@router.post("/register")
def register_user(
    userRegister: UserRegister,
    user_service: UserService = Depends(UserService),
) -> BasicResponse:
    return user_service.register(userRegister)


@router.post("/login")
def login(
    userLogin: UserLogin,
    user_service: UserService = Depends(UserService),
) -> Union[TokenResponse, BasicResponse]:
    return user_service.login(userLogin)


@router.post("/validate_otp")
def validate_otp(
    otpValidation: OTPValidation,
    user_service: UserService = Depends(UserService),
) -> TokenResponse:
    return user_service.validate_otp(otpValidation)


@router.get("/users")
def get_users(
    user_service: UserService = Depends(UserService)
):
    users = user_service.get_all_users()
    return {"users": users}