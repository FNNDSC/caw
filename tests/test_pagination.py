import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock, call

from chris.helpers.pagination import fetch_paginated_raw

from tests.mocks.session import mock_session
from tests.mocks.data.pagination import responses


@pytest.fixture
def session(mocker: MockerFixture) -> Mock:
    return mock_session(mocker, responses)


def test_pagination(session: Mock):
    url = "https://example.com/api/v1/something/"
    all_things = list(fetch_paginated_raw(session, url))
    assert all_things == [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
        {"id": 6},
        {"id": 7},
        {"id": 8},
    ]
    session.get.assert_has_calls(
        [
            call("https://example.com/api/v1/something/"),
            call("https://example.com/api/v1/something/?limit=3&offset=3"),
            call("https://example.com/api/v1/something/?limit=3&offset=6"),
        ]
    )
