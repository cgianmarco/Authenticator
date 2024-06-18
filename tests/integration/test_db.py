from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import Config

engine = create_async_engine(
    Config.TEST_DB_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

async def get_testing_session():
    TestingSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        await session.close()
