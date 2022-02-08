# ChRIS Automated Workflows

[![Unit Tests](https://github.com/FNNDSC/caw/actions/workflows/test.yml/badge.svg)](https://github.com/FNNDSC/caw/actions)
[![PyPI](https://img.shields.io/pypi/v/caw)](https://pypi.org/project/caw/)
[![License - MIT](https://img.shields.io/pypi/l/caw)](https://github.com/FNNDSC/caw/blob/master/LICENSE)

A command-line client for _ChRIS_ for pipeline execution and data mangement.

## Installation

The easiest option is via `pip`.

### Pip

```shell
pip install -U caw

# optional, for tab completion of subcommands
caw --install-completion
# optional, for secure password storage
pip install keyring
```

Alternatively, container images are also provided. See [below](#container-usage).

### Usage

```shell
caw [OPTIONS] COMMAND [ARGS]...
```

#### Container Usage

A Docker image is also provided. Podman and Docker work equally well.

```shell
docker run --rm --net=host -v $PWD/data:/data:ro -t fnndsc/caw:latest caw upload /data
podman run --rm --net=host -v $PWD/data:/data:ro -t fnndsc/caw:latest caw upload /data
```

Container isolation can make usage finicky.
Volumes must be mounted for the container to read data which exists on the host filesystem.
If the _ChRIS_ backend is on a private network, the `--net=host` option might be necessary to resolve
the server's hostname.

Alternatively, [Singularity](https://en.wikipedia.org/wiki/Singularity_(software))
is much easier to use because of its weaker container isolation and `$HOME` is a bind path by default.

```shell
singularity exec docker://fnndsc/caw:latest caw upload ./data
```

## Documentation

Details are provided by the `--help` commaand.

```shell
caw --help
caw search --help
caw pipeline --help
caw download --help
caw upload --help
```

### Logging In

Multiple ways of providing your credentials are supported. The most secure way is to
install the optional dependency [`keyring`](https://pypi.org/project/keyring/)
and run `caw login`.

```shell
# install optional dependency
pip install keyring
caw --address https://cube.chrisproject.org/api/v1/ --username 'a_crow' login
```

Alternatively, _ChRIS_ user account credentials can be passed via command-line arguments or environment variables.
It's safer to use environment variables (so that your password isn't saved to history)
and also easier (no need to retype it out everytime).

```shell
# using cli arguments
caw --address https://cube.chrisproject.org/api/v1/ \
    --username 'a_crow'      \
    --password notchris1234  \
    search

# using environment variables
export CHRIS_URL=https://cube.chrisproject.org/api/v1/
export CHRIS_USERNAME=a_crow
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

###### Piping

If a feed is successfully created from an upload, `caw` will print out the created feed's URL.

`caw` is feature-incomplete and common use cases will require light understanding
of the CUBE API and the combination of `caw` with other tools such as `curl ... | jq ...`.

For example, to get the URL of created _plugin instances_ following a `caw upload`:

```shell
caw upload file.dat \
  | xargs curl -fsu 'chris:chris1234' -H 'accept:application/json' \
  | jq -r '.plugin_instances' \
  | xargs curl -fsu 'chris:chris1234' -H 'accept:application/json' \
  | jq -r '.results[] | .url'
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

First, set up the _ChRIS_ backend on `http://localhost:8000/api/v1/`
(say, using [_miniChRIS_](https://github.com/FNNDSC/miniChRIS)).

Next, install the example pipeline.

```shell
./examples/dummy_pipeline.sh
./examples/upload_reconstruction_pipeline.sh
```

Install testing dependencies:

```shell
pip install pytest pytest_mock
```

Run all tests using the command

```shell
pytest
```

The end-to-end test is disabled by default because it will create a _ChRIS_ account and
affect `caw` user settings. It is recommended to run it in a container instead.

```shell
docker build -t caw -f Dockerfile.dev .
docker run --rm --net=host --userns=host -v $PWD:/usr/local/src/caw:ro \
       -t -e CAW_TEST_FULL=y caw
```

## Roadmap

Bugs will be fixed, but new features will not be added.

For the next-generation _ChRIS_ client, see
[chrs](https://github.com/FNNDSC/chrs),
and how it compares to `caw`:
https://github.com/FNNDSC/chrs/wiki/Feature-Table
