# Python _ChRIS_ Client

[![PyPI](https://img.shields.io/pypi/v/caw)](https://pypi.org/project/caw/)
[![License - MIT](https://img.shields.io/pypi/l/caw)](https://github.com/FNNDSC/caw/blob/master/LICENSE)
[![CI](https://github.com/FNNDSC/caw/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/caw/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python _ChRIS_ client library.

## Installation

```shell
pip install -U caw
```

## Example

```python
from pathlib import Path
from chris.client import ChrisClient

client = ChrisClient.from_login(
    address="https://cube.chrisproject.org/api/v1/",
    username="chris",
    password="chris1234"
)
client.upload(Path("example.txt"), "my_examples")
dircopy = client.get_plugin_by_name("pl-dircopy")
plinst = dircopy.create_instance({"dir": "chris/uploads/my_examples/example.txt"})
```

## Async

Looking for an `async` _ChRIS_ client? Let us know!
We have one implemented
[here](https://github.com/FNNDSC/chrisomatic/tree/master/chris),
though it's not published to PyPI.

## Command-Line Client

[chrs](https://github.com/FNNDSC/chrs/tree/master/chrs#readme)
is the next-generation _ChRIS_ command-line client, please check it out.

`caw` previously included a command-line client for _ChRIS_, however
since v0.7.0 it was deprecated and removed.

To use the `caw` command:

```shell
pip install caw==0.6.1
```

Usage: https://github.com/FNNDSC/caw/blob/d5b05b28af312b97ac80bd96376d70626db737a5/README.md
