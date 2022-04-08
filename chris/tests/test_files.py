import pytest
from uuid import uuid4
from pathlib import Path
from chris.client import ChrisClient
from io import BytesIO


@pytest.fixture()
def client() -> ChrisClient:
    return ChrisClient.from_login(
        address="http://localhost:8000/api/v1/", username="chris", password="chris1234"
    )


def test_upload_and_download(client: ChrisClient, tmpdir):
    content = "i am testing caw caw caw"
    input_file = Path(tmpdir) / "example.txt"
    input_file.write_text(content, encoding="utf-8")
    uploaded = client.upload(input_file, str(uuid4()))
    (file,) = client.search_uploadedfiles(fname_exact=uploaded.fname)

    output_file = tmpdir / "downloaded.out"
    file.download(output_file)
    assert file.fsize == len(content)
    assert output_file.read_text(encoding="utf-8") == content
