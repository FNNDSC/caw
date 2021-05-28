import unittest

import random
import string
import requests
import subprocess as sp
from tempfile import NamedTemporaryFile


# TODO test searching for and running a pipeline


def random_string(length=12) -> str:
    return ''.join(random.choice(string.ascii_letters) for x in range(length))


address = 'http://localhost:8000/api/v1/'
username = 'caw_test_' + random_string(6)
password = random_string(12)


def create_account():
    res = requests.post(
        f'{address}users/',
        headers={
            'Content-Type': 'application/vnd.collection+json',
            'Accept': 'application/json'
        },
        json={
            'template': {
                'data': [
                    {
                        'name': 'email',
                        'value': f'{username}@babyMRI.org'
                    },
                    {
                        'name': 'username',
                        'value': username
                    },
                    {
                        'name': 'password',
                        'value': password
                    }
                ]
            }
        }
    )
    res.raise_for_status()
    data = res.json()

    assert 'username' in data
    assert data['username'] == username


class TestEndToEnd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_account()

    def test_endtoend(self):
        sp.run(['caw', '--address', address, '--username', username, 'login'],
               input=(password + '\n'), text=True, check=True)

        with NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
            f.write("If you steal from one author it's plagiarism; if you steal from"
                    "\nmany it's research."
                    '\n                -- Wilson Mizner\n')

        sp.run(['caw', 'upload', f.name], check=True)
        sp.run(['caw', 'logout'])


if __name__ == '__main__':
    unittest.main()
