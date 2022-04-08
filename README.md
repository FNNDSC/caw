# Python _ChRIS_ Client

[![CI](https://github.com/FNNDSC/caw/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/caw/actions)
[![PyPI](https://img.shields.io/pypi/v/caw)](https://pypi.org/project/caw/)
[![License - MIT](https://img.shields.io/pypi/l/caw)](https://github.com/FNNDSC/caw/blob/master/LICENSE)

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

## Command-Line Client

[chrs](https://github.com/FNNDSC/chrs/tree/master/chrs#readme)
is the next-generation _ChRIS_ command-line client, please check it out.

`caw` includes a command-line client for _ChRIS_.
Its last supported version was 0.6.1 and is deprecated as of version 0.7.0.
It will be removed in an upcoming release.
For usage, see https://github.com/FNNDSC/caw/blob/d5b05b28af312b97ac80bd96376d70626db737a5/README.md
