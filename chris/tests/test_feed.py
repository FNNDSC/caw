import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock

from chris.cube.feed import Feed
from chris.tests.mocks.data.feed import data


@pytest.fixture
def session(mocker: MockerFixture) -> Mock:
    return mocker.Mock()


@pytest.fixture
def feed(session) -> Feed:
    return Feed(s=session, **data)


def test_set_name(session: Mock, feed: Feed):
    feed.set_name('A New Name for my Feed')
    session.put.assert_called_once_with(
        'https://example.com/api/v1/3/',
        json={
            'template': {
                'data': [
                    {
                        'name': 'name',
                        'value': 'A New Name for my Feed'
                    }
                ]
            }
        }
    )


def test_set_description(session: Mock, feed: Feed):
    feed.set_description('A new description for my feed.')
    session.put.assert_called_once_with(
        'https://example.com/api/v1/note3/',
        json={
            'template': {
                'data': [
                    {
                        'name': 'title',
                        'value': 'Description'
                    },
                    {
                        'name': 'content',
                        'value': 'A new description for my feed.'
                    }
                ]
            }
        }
    )
