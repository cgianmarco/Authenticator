import os

os.environ["RATE_LIMIT_ENABLED"] = "False"

import pytest
from fastapi.testclient import TestClient
from fastapi import status
import asyncio

from main import app
from test_db import get_testing_session, engine
from db import get_session, Base


client = TestClient(app, root_path="127.0.0.1/8000")
app.dependency_overrides[get_session] = get_testing_session

register_endpoint = "/v1/register"
login_endpoint = "/v1/login"

@pytest.fixture(autouse=True)
def setup_and_teardown(event_loop: asyncio.AbstractEventLoop):
    event_loop.run_until_complete(setup())
    yield
    event_loop.run_until_complete(teardown())

async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def teardown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

class TestIntegration:
        
    def test_register_user_ok(self):
        response = client.post(
            register_endpoint,
            json={"email": "prova@gmail.com", "password": "password"},
        )

        assert response.status_code == status.HTTP_200_OK

    def test_register_user_throws_error_when_user_exists(self):
        client.post(
            register_endpoint,
            json={"email": "prova@gmail.com", "password": "password"},
        )

        response = client.post(
            register_endpoint,
            json={"email": "prova@gmail.com", "password": "password"},
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_login_user_without_tfa_ok(self):
        client.post(
            register_endpoint,
            json={"email": "prova@gmail.com", "password": "password"},
        )

        response = client.post(
            login_endpoint,
            json={"email": "prova@gmail.com", "password": "password"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.json().keys()

    def test_login_user_with_tfa_ok(self):
        client.post(
            register_endpoint,
            json={
                "email": "prova@gmail.com",
                "password": "password",
                "enable_tfa": True,
            },
        )

        response = client.post(
            login_endpoint,
            json={"email": "prova@gmail.com", "password": "password"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert "token" not in response.json().keys()

    def test_login_user_throws_error_when_password_is_wrong(self):
        client.post(
            register_endpoint,
            json={"email": "prova@gmail.com", "password": "password"},
        )

        response = client.post(
            login_endpoint,
            json={"email": "prova@gmail.com", "password": "passwor"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_user_throws_error_when_user_does_not_exist(self):
        response = client.post(
            login_endpoint,
            json={"email": "prova@gmail.com", "password": "password"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
