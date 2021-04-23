# ChRIS Application Workflows

A command-line client for _ChRIS_ supporting execution of pipelines.

## Installation

```shell
pip install -U caw
```

## Development

```shell
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Testing

You must set up the _ChRIS_ backend on `http://localhost:8000/api/v1/`
(say, using [_miniChRIS_](https://github.com/FNNDSC/miniChRIS))
and install the pipeline https://chrisstore.co/api/v1/pipelines/1/

```shell
./testing/upload_reconstruction_pipeline.sh
```

Run all tests using the command

```shell
python -m unittest
```
