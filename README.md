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

```shell
caw [OPTIONS] COMMAND [ARGS]...
```

Container usage is also supported.


```shell
docker run --rm --net=host -v $PWD/data:/data:ro -t fnndsc/caw:latest caw upload /data
podman run --rm --net=host -v $PWD/data:/data:ro -t fnndsc/caw:latest caw upload /data
singularity exec docker://fnndsc/caw:latest caw upload ./data
```

## Documentation

### Logging In

ChRIS user account credentials can be passed via command-line arguments or environment variables.
It's safer to use environment variables (so that your password isn't saved to history)
and also easier (no need to retype it out everytime).

```shell
# using cli arguments
caw --address https://cube.chrisproject.org/api/v1/ \
    --username chrisy        \
    --password notchris1234  \
    search

# using environment variables
export CHRIS_URL=https://cube.chrisproject.org/api/v1/
export CHRIS_USERNAME=chrisy
export CHRIS_PASSWORD=notchris1234

caw search
```
### Commands

* `pipeline`: Run a pipeline on an existing feed.
* `search`: Search for pipelines that are saved in ChRIS.
* `upload`: Upload files into ChRIS storage and then run...
* `version`: Print version.

#### `caw pipeline`

Run a pipeline on an existing feed.

**Usage**:

```shell
$ caw pipeline [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of pipeline to run.  [required]

**Options**:

* `--target TEXT`: Plugin instance ID or URL.  [default: ]
* `--help`: Show this message and exit.

#### `caw search`

Search for pipelines that are saved in ChRIS.

**Usage**:

```shell
$ caw search [OPTIONS] [NAME]
```

**Arguments**:

* `[NAME]`: name of pipeline to search for  [default: ]

**Options**:

* `--help`: Show this message and exit.

#### `caw upload`

Upload files into ChRIS storage and then run pl-dircopy, printing the URL for the newly created plugin instance.

**Usage**:

```shell
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

To generate (Markdown) documentation:

```shell
pip install typer-cli
typer caw.__main__ utils docs --name caw
```
