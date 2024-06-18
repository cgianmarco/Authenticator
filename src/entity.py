from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    enable_tfa: Optional[bool] = False
    
class OTPValidation(BaseModel):
    email: EmailStr
    otp: str
    
class TokenResponse(BaseModel):
    token: str
    
class BasicResponse(BaseModel):
    success: bool = True
    message: str
    
