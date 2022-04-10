from os import path
import pytest
from uuid import uuid4
from chris.cube.feed import Feed
from chris import ChrisClient


@pytest.fixture()
def feed(client: ChrisClient, tmp_path) -> Feed:
    file = tmp_path / "example.txt"
    file.write_text("hello, this is an example", encoding="utf-8")
    upload = client.upload(file, path.join(str(uuid4()), "example.txt"))
    dircopy = client.get_plugin_by_name("pl-dircopy")
    plinst = dircopy.create_instance({"dir": upload.fname[: upload.fname.rindex("/")]})
    return plinst.get_feed()


def test_set_name(feed: Feed):
    feed = feed.set_name("A New Name for my Feed")
    assert feed.name == "A New Name for my Feed"


def test_set_description(feed: Feed):
    feed.set_description("A new description for my feed.")
    assert feed.get_note().content == "A new description for my feed."
