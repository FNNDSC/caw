#!/bin/bash -e


CUBE_URL=${CUBE_URL:-http://localhost:8000/api/v1/}
CHRIS_USER=${CUBE_USER:-chris:chris1234}

# pl-simpledsapp v2.0.2
res=$(curl -su "$CHRIS_USER" \
  -H 'Accept: application/json' \
  "${CUBE_URL}plugins/search/?name_exact=pl-simpledsapp&version=2.0.2")

if [ "$(jq -r '.count' <<< "$res")" -lt 1 ]; then
  docker exec chris python plugins/services/manager.py register host \
    --pluginurl https://chrisstore.co/api/v1/plugins/23/
fi

linear="$(
cat << EOF
{"template":
  {"data":[{"name":"name","value":"Example linear pipeline"},
  {"name": "authors", "value": "Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>"},
  {"name": "Category", "value": "Example"},
  {"name": "description", "value":
  "A linear and boring pipeline."},
  {"name":"locked","value":false},
  {"name":"plugin_tree","value":"[
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":null,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"first\"}]},
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":0,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"second\"}]},
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":1,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"third\"}]}
  ]"}]}}
EOF
)"

#     a
#    / \
#   b   c
# / | \  \
# e f g   d
#     |
#     h

branching="$(
cat << EOF
{"template":
  {"data":[{"name":"name","value":"Example branching pipeline"},
  {"name": "authors", "value": "Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>"},
  {"name": "Category", "value": "Example"},
  {"name": "description", "value":
  "A more complicated but nonetheless useless pipeline."},
  {"name":"locked","value":false},
  {"name":"plugin_tree","value":"[
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":null,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"a\"}]},
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":0,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"b\"}]},
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":0,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"c\"}]},
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":1,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"d\"}]},
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":2,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"e\"}]},
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":2,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"f\"}]},
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":2,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"g\"}]},
    {\"plugin_name\":\"pl-simpledsapp\",\"plugin_version\":\"2.0.2\",\"previous_index\":6,
      \"plugin_parameter_defaults\":[{\"name\":\"prefix\",\"default\":\"h\"}]}
  ]"}]}}
EOF
)"

examples=( "$linear" "$branching" )

for payload in "${examples[@]}"; do
  curl -u "$CHRIS_USER" "${CUBE_URL}pipelines/" \
    -H 'Content-Type:application/vnd.collection+json' \
    -H 'Accept:application/vnd.collection+json' \
    --data "$(tr -d '\n' <<< "$payload")"
done
