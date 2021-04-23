from unittest import TestCase
from chrisclient2.chrisclient import ChrisClient


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
        self.assertGreater(len(pipeline.pipings), 2)
        self.assertIn('plugin', pipeline.pipings[1])
        self.assertIn('previous', pipeline.pipings[1])

    def test_pipeline_assembly(self):
        pipeline = self.client.get_pipeline('Automatic Fetal Brain Reconstruction Pipeline')
        assembly = pipeline.assemble()
        self.assertIs(assembly.previous, None,
                      'Root of DAG has a previous plugin.')
        second = next(assembly.children.__iter__())
        self.assertIs(second.parent, assembly,
                      'Edge from second node to its parent is not the root.')

        q = assembly.to_queue()
        counter = 0
        while not q.empty():
            q.get_nowait()
            counter += 1
        self.assertEqual(counter, len(pipeline.pipings),
                         'Queue size does not match number of nodes in pipeline.')
