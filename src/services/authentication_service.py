from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Union

from entity import *
from .mail_service import MailService
from authenticators import JWTAuthenticator, OTPAuthenticator
from exceptions import *
from repositories import UserRepository
from constants import *


class AuthenticationService:

    def __init__(
        self,
        mail_service: MailService = Depends(),
        jwtAuth: JWTAuthenticator = Depends(),
        otpAuth: OTPAuthenticator = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.mail_service = mail_service
        self.user_repository = user_repository
        self.jwtAuth = jwtAuth
        self.otpAuth = otpAuth

    async def register(self, userRegister: UserRegister) -> BasicResponse:
        user = await self.user_repository.find_user_by_email(userRegister.email)
        
        if user:
            raise UserAlreadyExistsError()
        
        await self.user_repository.add_user(
            userRegister.email, userRegister.password, userRegister.enable_tfa
        )
        
        return BasicResponse(message=Messages.REGISTRATION_SUCCESS)

    async def login(self, userLogin: UserLogin) -> Union[TokenResponse, BasicResponse]:
        user = await self.user_repository.find_user_by_email(userLogin.email)

        if not user:
            raise InvalidCredentialsError()

        if not user.verify_password(userLogin.password):
            raise InvalidCredentialsError()

        if user.enable_tfa:
            otp = self.otpAuth.get_otp(user.secret_key)
            self.mail_service.send_otp_mail(user.email, otp)
            return BasicResponse(message=Messages.OTP_SENT)
        else:
            access_token = self.jwtAuth.generate_access_token(user)
            return TokenResponse(token=access_token)

    async def validate_otp(self, tfauthIn: OTPValidation) -> TokenResponse:
        user = await self.user_repository.find_user_by_email(tfauthIn.email)

        if not user:
            raise InvalidCredentialsError()

        if self.otpAuth.verify_otp(user.secret_key, tfauthIn.otp):
            access_token = self.jwtAuth.generate_access_token(user)
            return TokenResponse(token=access_token)
        else:
            raise InvalidCredentialsError()

    async def get_all_users(self):
        return await self.user_repository.get_all_users()
    
