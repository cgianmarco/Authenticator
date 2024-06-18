from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os
import base64
from typing import Optional

from models import User
from db import get_session

class UserRepository:
    
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session
        
    async def get_all_users(self):
        results = await self._session.execute(select(User))
        return results.scalars().all()
    
    async def find_user_by_email(self, email: str) -> Optional[User]:
        result = await self._session.execute(select(User).filter_by(email=email))
        return result.scalars().first()

    async def add_user(self, email: str, password: str, enable_tfa: bool):
        secret_key = self._generate_secret_key()

        user = User(
            email=email,
            password=password,
            enable_tfa=enable_tfa,
            secret_key=secret_key,
        )
        self._session.add(user)
        await self._session.commit()

    def _generate_secret_key(self):
        return base64.b32encode(os.urandom(20)).decode("utf-8")