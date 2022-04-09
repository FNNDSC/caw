"""
Python client library for
_[ChRIS](https://chrisproject.org)_.

## Installation

```shell
pip install caw
```

Note: the pip package name is `caw`, but the module name is `chris`.
"""

from chris.client import ChrisClient
from chris.helpers.pagination import Paginated

import chris.types as types
import chris.cube as cube

__docformat__ = "numpy"

__all__ = ["ChrisClient", "types", "cube", "Paginated"]
