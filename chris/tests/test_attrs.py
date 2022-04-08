import pytest
from chris.client import ChrisClient


@pytest.fixture()
def client() -> ChrisClient:
    return ChrisClient.from_login(
        address="http://localhost:8000/api/v1/", username="chris", password="chris1234"
    )


def test_username(client: ChrisClient):
    assert client.username == "chris"
