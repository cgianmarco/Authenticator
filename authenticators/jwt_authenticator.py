from datetime import datetime, timedelta, timezone
import jwt

from config import Config
from models import User

class JWTAuthenticator:
    def generate_access_token(self, user: User):
        payload = {
            "sub": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        }

        access_token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
        
        return access_token