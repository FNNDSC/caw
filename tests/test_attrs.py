import pytest
from chris.client import ChrisClient
from chris.types import Username


def test_username(username: Username, client: ChrisClient):
    assert client.username == username
