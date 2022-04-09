import abc
from requests import Session, Response
from serde import from_dict
from typing import Union
from chris.helpers.deserialize import deserialize


class ConnectedResource(abc.ABC):
    """
    A base class for resource models which have a session object which is
    used to make requests to CUBE. The session should have an authorization
    token for CUBE.

    ## Protocol

    Classes which extend `ConnectedResource` **must** be decorated with
    [`@serde.deserialize`](https://yukinarit.github.io/pyserde/api/serde/de.html#deserialize).
    Since `ConnectedResource` itself is not a
    [dataclass](https://docs.python.org/3/library/dataclasses.html),
    its `session` field are not part of the subclass's `__init__`,
    and are not deserialized by _pyserde_.
    After calling `serde.json.from_json`, the program **must** assign a value
    to the deserialized object's `session` field.

    ```python
    @serde.deserialize()
    class Thing(ConnectedResource):
        id: int

    def get_thing() -> Thing:
        res = session.get(url)
        return Thing.deserialize(res, session)
    ```

    ## Visibility

    This class and its fields are private-ish. They may be used inside the
    `chris` module, but they should not be used by clients.
    (`protected` in Java-speak, `pub(crate)` in Rust-speak).
    """

    session: Session

    @classmethod
    def deserialize(cls, data: Union[Response, dict], session: Session):
        if isinstance(data, Response):
            o: cls = deserialize(cls, data)
        elif isinstance(data, dict):
            o: cls = from_dict(cls, data)
        else:
            raise TypeError(f"data type {type(data)} is not Union[Response, dict]")
        object.__setattr__(o, "session", session)
        return o
