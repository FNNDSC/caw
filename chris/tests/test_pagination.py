import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock, call

from chris.types import CUBEUrl
from chris.cube.pagination import PaginatedResource

from chris.tests.mocks.session import mock_session
from chris.tests.mocks.data.pagination import responses


@pytest.fixture
def session(mocker: MockerFixture) -> Mock:
    return mock_session(mocker, responses)


def test_pagination(session: Mock):
    resource = PaginatedResource(url='https://example.com/', s=session)
    url = CUBEUrl('https://example.com/api/v1/something/')
    all_things = list(resource.fetch_paginated_raw(url, max_requests=10))
    assert all_things == [
        {'id': 1}, {'id': 2}, {'id': 3},
        {'id': 4}, {'id': 5}, {'id': 6},
        {'id': 7}, {'id': 8}
    ]
    session.get.assert_has_calls([
        call('https://example.com/api/v1/something/'),
        call('https://example.com/api/v1/something/?limit=3&offset=3'),
        call('https://example.com/api/v1/something/?limit=3&offset=6')
    ])
