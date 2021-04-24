# ChRIS Automated Workflows

[![Unit Tests](https://github.com/FNNDSC/caw/actions/workflows/test.yml/badge.svg)](https://github.com/FNNDSC/caw/actions)
[![PyPI](https://img.shields.io/pypi/v/caw)](https://pypi.org/project/caw/)
[![License - MIT](https://img.shields.io/pypi/l/caw)](https://github.com/FNNDSC/caw/blob/master/LICENSE)

A command-line client for _ChRIS_ for pipeline execution and data maangement.

## Installation

### Pip

```shell
pip install -U caw
caw --install-completion
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

_ChRIS_ user account credentials can be passed via command-line arguments or environment variables.
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

- `search`:   Search for pipelines that are saved in _ChRIS_.
- `pipeline`: Run a pipeline on an existing feed.
- `upload`:   Upload files into _ChRIS_ storage and run [`pl-dircopy`](https://chrisstore.co/plugin/25).
- `download`: Download everything from a _ChRIS_ url.

#### `caw search`

Search for pipelines that are saved in _ChRIS_.

###### Examples

```shell
# list all pipellines
$ caw search
https://cube.chrisproject.org/api/v1/pipelines/1/           Automatic Fetal Brain Reconstruction Pipeline
https://cube.chrisproject.org/api/v1/pipelines/2/           Infant FreeSurfer with Cerebellum Step
https://cube.chrisproject.org/api/v1/pipelines/2/           COVID-Net Chest CT Analysis and Report

# search for pipelines by name
$ caw search 'Fetal Brain'
https://cube.chrisproject.org/api/v1/pipelines/1/           Automatic Fetal Brain Reconstruction Pipeline
```

#### `caw pipeline`

Run a pipeline on an existing feed.

###### Examples

```shell
# specify source as a plugin instance ID
$ caw pipeline --target 3 'Automatic Fetal Brain Reconstruction Pipeline'

# specify source by URL
$ caw pipeline --target https://cube.chrisproject.org/api/v1/plugins/instances/3/ 'Automatic Fetal Brain Reconstruction Pipeline'
```

#### `caw upload`

Upload files into _ChRIS_ storage and then run pl-dircopy, printing the URL for the newly created plugin instance.

###### Examples

```shell
# upload files and create a new feed by running pl-dircopy
$ caw upload something.txt picture.jpg

# upload a folder and create a new feed by running pl-dircopy
$ caw upload data/

# create a feed with a title and description
$ caw upload --name 'Caw caw, ima crow' --description 'A murder of crows' \
    something.txt picture.jpg

# create a feed and run a pipeline after the pl-dircopy instance
$ caw upload --name 'In-utero study' \
    --pipeline 'Automatic Fetal Brain Reconstruction Pipeline' \
    data/T2_*.nii
```

#### `caw download`

Download files from _ChRIS_.

```bash
# download everything from a feed
$ caw download 'https://cube.chrisproject.org/api/v1/3/files/' results/

# download the output directory of a specific plugin instance
$ caw download 'https://cube.chrisproject.org/api/v1/plugins/instances/5/files/' results/

# download everything from a path 'chris/uploads/test'
$ caw download 'https://cube.chrisproject.org/api/v1/uploadedfiles/search/?fname=chris%2Fuploads%2Ftest' results/

# example results
$ tree results/
wow
└── uploads
    └── test
        ├── a.txt
        ├── b.txt
        ├── c.txt
        ├── d.txt
        └── e.txt
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
