import typer

from chris.client import Pipeline, PluginInstance


def run_pipeline_with_progress(chris_pipeline: Pipeline, plugin_instance: PluginInstance):
    """
    Helper to execute a pipeline with a progress bar.
    """
    with typer.progressbar(plugin_instance.append_pipeline(chris_pipeline),
                           length=len(chris_pipeline.pipings), label='Scheduling pipeline') as proto_pipeline:
        for _ in proto_pipeline:
            pass
