from pytest_mock import MockerFixture
# noinspection PyProtectedMember
from chris.cube.registered_pipeline import Piping, _MutablePluginTreeNode
from chris.cube.plugin_tree import PluginTree
from chris.types import PluginId, PipingId, PipingUrl, PipelineId, PluginUrl, CUBEUrl, ParameterName


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
        previous=PipingUrl('https://example.com/api/v1/pipelines/3/pipings/2/'),
        plugin_id=PluginId(20),
        plugin=PluginUrl('https://example.com/api/v1/plugins/20/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )
    dp = Piping(
        s=session,
        id=PipingId(4),
        url=CUBEUrl('https://example.com/api/v1/pipelines/3/pipings/4/'),
        previous=PipingUrl('https://example.com/api/v1/pipelines/3/pipings/2/'),
        plugin_id=PluginId(30),
        plugin=PluginUrl('https://example.com/api/v1/plugins/30/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )
    cp = Piping(
        s=session,
        id=PipingId(2),
        url=CUBEUrl('https://example.com/api/v1/pipelines/3/pipings/2/'),
        previous=PipingUrl('https://example.com/api/v1/pipelines/3/pipings/1/'),
        plugin_id=PluginId(40),
        plugin=PluginUrl('https://example.com/api/v1/plugins/40/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )
    bp = Piping(
        s=session,
        id=PipingId(3),
        url=CUBEUrl('https://example.com/api/v1/pipelines/3/pipings/3/'),
        previous=PipingUrl('https://example.com/api/v1/pipelines/3/pipings/1/'),
        plugin_id=PluginId(50),
        plugin=PluginUrl('https://example.com/api/v1/plugins/50/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )
    ap = Piping(
        s=session,
        id=PipingId(1),
        url=CUBEUrl('https://example.com/api/v1/pipelines/3/pipings/1/'),
        previous=None,
        plugin_id=PluginId(60),
        plugin=PluginUrl('https://example.com/api/v1/plugins/60/'),
        pipeline_id=PipelineId(3),
        pipeline=CUBEUrl('https://example.com/api/v1/pipelines/3/')
    )

    em = _MutablePluginTreeNode(s=session, piping=ep, params={ParameterName('this'): 'isit'})
    dm = _MutablePluginTreeNode(s=session, piping=dp, params={})
    cm = _MutablePluginTreeNode(s=session, piping=cp, params={})
    bm = _MutablePluginTreeNode(s=session, piping=bp, params={})
    am = _MutablePluginTreeNode(s=session, piping=ap, params={ParameterName('bow'): 'wow'})

    cm.children.append(dm)
    cm.children.append(em)
    am.children.append(bm)
    am.children.append(cm)

    et = PluginTree(s=session, piping=ep, default_parameters={ParameterName('this'): 'isit'})
    dt = PluginTree(s=session, piping=dp, default_parameters={})
    ct = PluginTree(s=session, piping=cp, default_parameters={},
                    children=(dt, et))
    bt = PluginTree(s=session, piping=bp, default_parameters={})
    at = PluginTree(s=session, piping=ap, default_parameters={ParameterName('bow'): 'wow'},
                    children=(bt, ct))

    assert at == am.freeze()
