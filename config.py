import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # JWT Config
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    
    # OTP Config
    OTP_LENGTH: int = int(os.getenv("OTP_LENGTH"))
    OTP_VALIDITY: int = int(os.getenv("OTP_VALIDITY"))
    
    # DB Config
    DB_URI: str = os.getenv("DB_URI")
    
    # Rate Limit Config
    RATE_LIMIT_ENABLED : bool = bool(os.getenv("RATE_LIMIT_ENABLED"))
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS"))
    RATE_LIMIT_TIME_WINDOW: int = int(os.getenv("RATE_LIMIT_TIME_WINDOW"))
    
    # Test Config
    TEST_DB_URI: str = os.getenv("TEST_DB_URI")