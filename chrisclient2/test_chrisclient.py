from unittest import TestCase
from chrisclient2.chrisclient import ChrisClient
from chrisclient2.models import Piping


class TestChrisClient(TestCase):

    client = ChrisClient(
        address='http://localhost:8000/api/v1/',
        username='chris',
        password='chris1234'
    )

    def test_get_plugin_by_name(self):
        plugin = self.client.get_plugin(name_exact='pl-tsdircopy')
        self.assertEqual(plugin.name, 'pl-tsdircopy')

    def test_get_plugin_by_version(self):
        plugin = self.client.get_plugin(name_exact='pl-dircopy', version='2.1.0')
        self.assertEqual(plugin.name, 'pl-dircopy')
        self.assertEqual(plugin.version, '2.1.0')

    def test_get_plugin_by_url(self):
        plugin = self.client.get_plugin(url='http://localhost:8000/api/v1/plugins/2/')
        self.assertEqual(plugin.url, 'http://localhost:8000/api/v1/plugins/2/')

    def test_get_pipeline(self):
        pipeline = self.client.get_pipeline('Automatic Fetal Brain Reconstruction Pipeline')
        pipings = pipeline.get_pipings()
        self.assertGreater(len(pipings), 2)
        self.assertIn('plugin', pipings[1])
        self.assertIn('previous', pipings[1])

    def test_pipeline_assembly(self):
        pipeline = self.client.get_pipeline('Automatic Fetal Brain Reconstruction Pipeline')
        assembly = pipeline.assemble()
        self.assertIs(assembly.previous, None,
                      'Root of DAG has a previous plugin.')
        second = next(assembly.next.__iter__())
        self.assertIs(second.parent, assembly,
                      'Edge from second node to its parent is not the root.')
        count = len(pipeline.get_pipings())
        self.assertTreeIsFinite(assembly, count)

    def assertTreeIsFinite(self, node: Piping, max_depth: int):
        """
        Recursively check that the tree's height is less than the given maximum.
        :param node: graph node
        :param max_depth: maximum height from the current node
        """
        if not node:
            return
        if max_depth <= 0:
            self.fail('Tree height exceeds the number of nodes from JSON description of pipeline.')
        max_depth -= 1
        for child in node.next:
            self.assertTreeIsFinite(child, max_depth)
