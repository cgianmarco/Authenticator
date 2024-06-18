from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

engine = create_engine(
    Config.TEST_DB_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def get_testing_session():
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
