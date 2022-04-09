import requests
from pytest_mock import MockerFixture
from unittest.mock import Mock
from typing import Dict


def mock_session(mocker: MockerFixture, responses: Dict[str, any]) -> Mock:
    def create_dumb_paginated_response(url: str) -> Mock:
        res = mocker.Mock()
        res.json = mocker.Mock(return_value=responses[url])
        return res

    m = mocker.Mock(spec=requests.Session)
    m.get = mocker.Mock(wraps=create_dumb_paginated_response)
    return m
