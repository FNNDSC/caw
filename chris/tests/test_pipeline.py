from pytest_mock import MockerFixture
from chris.cube.registered_pipeline import Piping, MutablePluginTreeNode
from chris.cube.plugin_tree import PluginTree
from chris.types import PluginId, PipingId, PipelineId, CUBEUrl, ParameterName


r"""
    a --bow wow
   / \
  b   c
     / \
    d   e --this isit
"""


def test_freeze(mocker: MockerFixture):
    session = mocker.Mock()
    ep = Piping(
        s=session,
        id=PipingId(5),
        url=CUBEUrl('https://example.com/api/v1/pipelines/3/pipings/5/'),
        previous=PipingId(2),
        plugin_id=PluginId(20),
        plugin=CUBEUrl('https://example.com/api/v1/plugins/20/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )
    dp = Piping(
        s=session,
        id=PipingId(4),
        url=CUBEUrl('https://example.com/api/v1/pipelines/3/pipings/4/'),
        previous=PipingId(2),
        plugin_id=PluginId(30),
        plugin=CUBEUrl('https://example.com/api/v1/plugins/30/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )
    cp = Piping(
        s=session,
        id=PipingId(2),
        url=CUBEUrl('https://example.com/api/v1/pipelines/3/pipings/2/'),
        previous=PipingId(1),
        plugin_id=PluginId(40),
        plugin=CUBEUrl('https://example.com/api/v1/plugins/40/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )
    bp = Piping(
        s=session,
        id=PipingId(3),
        url=CUBEUrl('https://example.com/api/v1/pipelines/3/pipings/3/'),
        previous=PipingId(1),
        plugin_id=PluginId(50),
        plugin=CUBEUrl('https://example.com/api/v1/plugins/50/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )
    ap = Piping(
        s=session,
        id=PipingId(1),
        url=CUBEUrl('https://example.com/api/v1/pipelines/3/pipings/1/'),
        previous=None,
        plugin_id=PluginId(60),
        plugin=CUBEUrl('https://example.com/api/v1/plugins/60/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )

    em = MutablePluginTreeNode(s=session, piping=ep, params={ParameterName('this'): 'isit'})
    dm = MutablePluginTreeNode(s=session, piping=dp, params={})
    cm = MutablePluginTreeNode(s=session, piping=cp, params={})
    bm = MutablePluginTreeNode(s=session, piping=bp, params={})
    am = MutablePluginTreeNode(s=session, piping=ap, params={ParameterName('bow'): 'wow'})

    cm.children.append(dm)
    cm.children.append(em)
    am.children.append(bm)
    am.children.append(cm)

    et = PluginTree(s=session, plugin=ep.plugin, default_parameters={ParameterName('this'): 'isit'})
    dt = PluginTree(s=session, plugin=dp.plugin, default_parameters={})
    ct = PluginTree(s=session, plugin=cp.plugin, default_parameters={},
                    children=(dt, et))
    bt = PluginTree(s=session, plugin=bp.plugin, default_parameters={})
    at = PluginTree(s=session, plugin=ap.plugin, default_parameters={ParameterName('bow'): 'wow'},
                    children=(bt, ct))

    assert at == am.freeze()
