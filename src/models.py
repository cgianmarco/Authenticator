from sqlalchemy import Column, Integer, String, Boolean
import bcrypt

from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    _password = Column('password', String(120), nullable=False)
    enable_tfa = Column(Boolean, default=False)
    secret_key = Column(String(32))
    
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, plaintext_password: str):
        self._password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plaintext_password: str):
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), self._password.encode('utf-8'))