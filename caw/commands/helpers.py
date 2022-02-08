"""
Badly implemented --- calls ``typer.Abort`` directly, because
I am so done with this.

I want to work on chrs!
"""

import typer
from chris.types import CUBEAddress, CUBEUrl


def api_address(s: CUBEUrl) -> CUBEAddress:
    i = s.find('/api/v1/')
    if i == -1:
        typer.secho(f'Invalid URL: {s}', color=typer.colors.RED, err=True)
        raise typer.Abort()
    return CUBEAddress(s[:i + 8])


assert api_address(CUBEUrl('http://localhost:8080/api/v1/files/')) == CUBEAddress('http://localhost:8080/api/v1/')
assert api_address(CUBEUrl('https://example.com/api/v1/uploadedfiles/')) == CUBEAddress('https://example.com/api/v1/')
assert api_address(CUBEUrl('https://example.com/api/v1/')) == CUBEAddress('https://example.com/api/v1/')
