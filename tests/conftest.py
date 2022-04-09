import pytest

from chris.client import ChrisClient
from chris.types import Username, CUBEAddress


@pytest.fixture(scope="session")
def address() -> CUBEAddress:
    return CUBEAddress("http://localhost:8000/api/v1/")


@pytest.fixture(scope="session")
def username() -> Username:
    return Username("chris")


@pytest.fixture(scope="session")
def password() -> str:
    return "chris1234"


@pytest.fixture(scope="session")
def client(address: str, username: Username, password: str) -> ChrisClient:
    return ChrisClient.from_login(address, username, password)
