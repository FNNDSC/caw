# ChRIS Application Workflows

A command-line client for _ChRIS_ supporting execution of pipelines.

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

```shell
plugins=(
  https://chrisstore.co/api/v1/plugins/71/
  https://chrisstore.co/api/v1/plugins/77/
  https://chrisstore.co/api/v1/plugins/81/
  https://chrisstore.co/api/v1/plugins/82/
)

for url in "${plugins[@]}"; do
  docker exec chris python plugins/services/manager.py register host --pluginurl $url
done

http -a chris:chris1234 POST http://localhost:8000/api/v1/pipelines/ Content-Type:application/vnd.collection+json Accept:application/vnd.collection+json template:='
  {"data":[{"name":"name","value":"Automatic Fetal Brain Reconstruction Pipeline"},
  {"name": "authors", "value": "Jennings Zhang <Jennings.Zhang@childrens.harvard.edu"},
  {"name": "Category", "value": "MRI"},
  {"name": "description", "value": "Automatic fetal brain reconstruction pipeline developed by Kiho'"'"'s group at the FNNDSC. Features machine-learning based brain masking and quality assessment."},
  {"name":"locked","value":false},
  {"name":"plugin_tree", "value":"[{\"plugin_name\": \"pl-fetal-brain-mask\",\"plugin_version\": \"1.2.1\",    \"previous_index\": null  },  {    \"plugin_name\": \"pl-ants_n4biasfieldcorrection\",    \"plugin_version\": \"0.2.7.1\",    \"previous_index\": 0,    \"plugin_parameter_defaults\": [      {        \"name\": \"inputPathFilter\",        \"default\": \"extracted/0.0/*.nii\"      }    ]  },  {    \"plugin_name\": \"pl-fetal-brain-assessment\",    \"plugin_version\": \"1.3.0\",    \"previous_index\": 1  },  {    \"plugin_name\": \"pl-irtk-reconstruction\",    \"plugin_version\": \"1.0.1\",    \"previous_index\": 2}]  "}]}'
```

Run all tests using the command

```shell
python -m unittest
```

## TODO

- [ ] preserve directory structure on upload
