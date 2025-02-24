import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.models import Base
from app.app import app
import redis
import os

# Set up a test database

main_engine = create_engine(os.getenv('DATABASE_URL'), isolation_level="AUTOCOMMIT")


def create_test_database():
    # with main_engine.connect() as conn:
    with main_engine.connect() as conn:
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'test_logs_db';"))
        if not result.scalar():  # If no result, database doesn't exist
            conn.execute(text("CREATE DATABASE test_logs_db;"))


create_test_database()

TEST_DATABASE_URL = f"{os.getenv('DATABASE_URL')}test_logs_db"
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Redis settings
TEST_REDIS_DB = 1  # Use a separate Redis database for testing

# Create Redis test connection
test_redis_conn = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=TEST_REDIS_DB)


# test_redis_conn = redis.Redis(host='localhost', port=6379,db=TEST_REDIS_DB)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def setup_redis():
    """Ensure Redis is clean before and after each test."""
    test_redis_conn.flushdb()  # Clear Redis before the test
    yield
    test_redis_conn.flushdb()  # Clear Redis after the test


@pytest.fixture
def client():
    return TestClient(app)
