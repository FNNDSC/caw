import sys
import typer

from typing import Tuple
from chris.cube.pipeline import Pipeline
from chris.cube.plugin_instance import PluginInstance


def run_pipeline_with_progress(chris_pipeline: Pipeline, parent: PluginInstance) -> Tuple[PluginInstance, ...]:
    """
    Helper to execute a pipeline with a progress bar.
    """
    root = chris_pipeline.get_root()
    with typer.progressbar(root.run(parent.id),
                           length=len(root), label='Scheduling pipeline',
                           file=sys.stderr) as proto_pipeline:
        return tuple(parent for parent, _ in proto_pipeline)
