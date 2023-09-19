import sys
import random
import string
import asyncio
from os.path import abspath
from os.path import dirname as d


import pytest
from faker import Faker
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from server.core.db import async_session
from server.main import app

fake = Faker()

# Chroot to app dir
root_dir = d(d(abspath(__file__)))
sys.path.append(f"{root_dir}/server")

client = TestClient(app)


def str_generator(length: int = 25):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def email_generator(length: int = 25):
    return f"{str_generator(length)}@mail.com"


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture
def test_client():
    return client


@pytest.fixture()
def async_test_client():
    async_client = AsyncClient(app=app, base_url="http://test")
    return async_client


@pytest.fixture()
async def session() -> AsyncSession:
    async with async_session() as sess:
        yield sess