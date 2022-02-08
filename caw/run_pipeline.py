import sys
import typer

from chris.cube.pipeline import Pipeline
from chris.cube.plugin_instance import PluginInstance


def run_pipeline_with_progress(chris_pipeline: Pipeline, plugin_instance: PluginInstance):
    """
    Helper to execute a pipeline with a progress bar.
    """
    plugin_root = chris_pipeline.get_root()
    with typer.progressbar(plugin_root.run(plugin_instance.id),
                           length=len(plugin_root), label='Scheduling pipeline',
                           file=sys.stderr) as proto_pipeline:
        for _ in proto_pipeline:
            pass
