import json
from chris.client import ChrisClient

expected = r"""
{"template":
  {"data":[{"name":"name","value":"Example branching pipeline"},
  {"name": "authors", "value": "Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>"},
  {"name": "category", "value": "Example"},
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
"""
expected = expected.replace("\n", " ")


def test_deserialize():
    client = ChrisClient.from_login(
        address="http://localhost:8000/api/v1/", username="chris", password="chris1234"
    )
    pipeline = client.get_pipeline("Example branching pipeline")
    expected_plugin_tree = json.loads(
        json.loads(expected)["template"]["data"][-1]["value"]
    )
    actual = pipeline.get_root().deserialize_tree()

    # limitation: retrieved plugin tree will have all parameter defaults
    for piping in actual:
        __remove_defaults_except_prefix(piping)

    assert sorted_pipings(actual) == sorted_pipings(expected_plugin_tree)


def __remove_defaults_except_prefix(piping: dict) -> None:
    piping["plugin_parameter_defaults"] = [
        p for p in piping["plugin_parameter_defaults"] if p["name"] == "prefix"
    ]


def sorted_pipings(plugin_tree: list) -> list:
    return sorted(plugin_tree, key=SerializedPiping)


class SerializedPiping:
    def __init__(self, __d: dict):
        self.plugin_name = __d["plugin_name"]
        self.plugin_version = __d["plugin_version"]
        self.previous_index = __d["previous_index"]

    def __lt__(self, other: "SerializedPiping") -> bool:
        if self.previous_index is None:
            return True
        if other.previous_index is None:
            return False
        if self.previous_index < other.previous_index:
            return True
        if self.plugin_name < other.plugin_name:
            return True
        if self.plugin_version < other.plugin_version:
            return True
        return False
