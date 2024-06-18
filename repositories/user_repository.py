from fastapi import Depends
from sqlalchemy.orm import Session
import os
import base64
from typing import Optional

from models import User
from db import get_session

class UserRepository:
    
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        
    def get_all_users(self):
        return self.session.query(User).all()

    def find_user_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter_by(email=email).first()

    def add_user(self, email: str, password: str, enable_tfa: bool):
        secret_key = self._generate_secret_key()

        user = User(
            email=email,
            password=password,
            enable_tfa=enable_tfa,
            secret_key=secret_key,
        )
        self.session.add(user)
        self.session.commit()

    def _generate_secret_key(self):
        return base64.b32encode(os.urandom(20)).decode("utf-8")