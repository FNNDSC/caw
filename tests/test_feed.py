import json

import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock
from requests import Response
from chris.cube.feed import Feed
from tests.mocks.data.feed import data
import serde


@pytest.fixture
def session(mocker: MockerFixture) -> Mock:
    mock_res = mocker.Mock(spec=Response)
    mock_res.text = json.dumps(data)
    mock_res.json.return_value = data
    s = mocker.Mock()
    s.get.return_value = mock_res
    return s


@pytest.fixture
def feed(session) -> Feed:
    f = serde.from_dict(Feed, data)
    object.__setattr__(f, "session", session)
    return f


def test_set_name(session: Mock, feed: Feed):
    feed.set_name("A New Name for my Feed")
    session.put.assert_called_once_with(
        "https://example.com/api/v1/3/",
        json={"name": "A New Name for my Feed"},
    )


def test_set_description(session: Mock, feed: Feed):
    feed.set_description("A new description for my feed.")
    session.put.assert_called_once_with(
        "https://example.com/api/v1/note3/",
        json={"title": "Description", "content": "A new description for my feed."},
    )
