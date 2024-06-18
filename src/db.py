from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import Config

class Base(DeclarativeBase):
    pass

async def get_session():
    engine = create_async_engine(Config.DB_URI)
    Session = async_sessionmaker(bind=engine)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    session = Session()
    try:
        yield session
    finally:
        await session.close()