from unittest import TestCase
from chrisclient2.chrisclient import ChrisClient


class TestChrisClient(TestCase):

    client = ChrisClient(
        address='http://localhost:8000/api/v1/',
        username='chris',
        password='chris1234'
    )

    def test_get_plugin_by_name(self):
        res = self.client.get_plugin(name_exact='pl-tsdircopy')
        self.assertIn('name', res)
        self.assertEqual(res['name'], 'pl-tsdircopy')

    def test_get_plugin_by_version(self):
        res = self.client.get_plugin(name_exact='pl-dircopy', version='2.1.0')
        self.assertIn('name', res)
        self.assertEqual(res['name'], 'pl-dircopy')
        self.assertIn('version', res)
        self.assertEqual(res['version'], '2.1.0')

    def test_get_plugin_by_url(self):
        res = self.client.get_plugin(url='http://localhost:8000/api/v1/plugins/2/')
        self.assertIn('name', res)
        self.assertIn('min_memory_limit', res)

    def test_get_pipeline(self):
        pipeline = self.client.get_pipeline('Automatic Fetal Brain Reconstruction Pipeline')
        pipings = pipeline.get_pipings()
        self.assertGreater(len(pipings), 2)
        self.assertIn('plugin', pipings[1])
        self.assertIn('previous', pipings[1])
