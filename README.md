# ChRIS Automated Workflows

[![Unit Tests](https://github.com/FNNDSC/caw/actions/workflows/test.yml/badge.svg)](https://github.com/FNNDSC/caw/actions)
[![PyPI](https://img.shields.io/pypi/v/caw)](https://pypi.org/project/caw/)
[![License - MIT](https://img.shields.io/pypi/l/caw)](https://github.com/FNNDSC/caw/blob/master/LICENSE)

A command-line client for _ChRIS_ supporting execution of pipelines.

## Installation

### Pip

```shell
pip install -U caw
```

### Usage

```console
$ caw [OPTIONS] COMMAND [ARGS]...
```

Container usage is also supported.


```console
docker run --rm -t -v $PWD/data:/data:ro fnndsc/caw:latest caw upload /data
podman run --rm -t -v $PWD/data:/data:ro fnndsc/caw:latest caw upload /data
singularity exec docker://fnndsc/caw:latest caw upload ./data
```

## Documentation


**Options**:

* `-a, --address TEXT`: [env var: CHRIS_URL; default: http://localhost:8000/api/v1/]
* `-u, --username TEXT`: [env var: CHRIS_USERNAME; default: chris]
* `-p, --password TEXT`: [env var: CHRIS_PASSWORD; default: chris1234]
* `--help`: Show this message and exit.

**Commands**:

* `pipeline`: Run a pipeline on an existing feed.
* `search`: Search for pipelines that are saved in ChRIS.
* `upload`: Upload files into ChRIS storage and then run...
* `version`: Print version.

## `caw pipeline`

Run a pipeline on an existing feed.

**Usage**:

```console
$ caw pipeline [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of pipeline to run.  [required]

**Options**:

* `--target TEXT`: Plugin instance ID or URL.  [default: ]
* `--help`: Show this message and exit.

## `caw search`

Search for pipelines that are saved in ChRIS.

**Usage**:

```console
$ caw search [OPTIONS] [NAME]
```

**Arguments**:

* `[NAME]`: name of pipeline to search for  [default: ]

**Options**:

* `--help`: Show this message and exit.

## `caw upload`

Upload files into ChRIS storage and then run pl-dircopy, printing the URL for the newly created plugin instance.

**Usage**:

```console
$ caw upload [OPTIONS] FILES...
```

**Arguments**:

* `FILES...`: Files to upload. Folder upload is supported, but directories are destructured.  [required]

**Options**:

* `-t, --threads INTEGER`: Number of threads to use for file upload.  [default: 4]
* `--create-feed / --no-create-feed`: Run pl-dircopy on the newly uploaded files.  [default: True]
* `-n, --name TEXT`: Name of the feed.  [default: ]
* `-d, --description TEXT`: Description of the feed.  [default: ]
* `-p, --pipeline TEXT`: Name of pipeline to run on the data.  [default: ]
* `--help`: Show this message and exit.



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
