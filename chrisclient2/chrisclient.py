from os import path
import requests

from chrisclient2.models import PluginInstance, Feed
from chrisclient2.util import collection_helper


class PluginNotFoundError(Exception):
    pass


class ChrisClient:
    def __init__(self, address, username, password):
        self.addr = address

        # TODO put this in collection_links
        self.search_addr = path.join(address, 'plugins/search/')

        self.s = requests.Session()
        self.s.auth = (username, password)
        self.s.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/vnd.collection+json',
        })

        res = self.s.get(address).json()
        self.collection_links = res['collection_links']
        assert self.collection_links['uploadedfiles']

    def upload(self, file_path: str, upload_folder: str):
        """
        Upload a local file into ChRIS backend Swift storage.
        :param file_path: local file path
        :param upload_folder: path in Swift where to upload to
        :return: response
        """
        bname = path.basename(file_path)
        upload_path = path.join(upload_folder, bname)

        with open(file_path, 'rb') as file_object:
            files = {
                'upload_path': (None, upload_path),
                'fname': (bname, file_object)
            }
            res = self.s.post(
                self.collection_links['uploadedfiles'],
                files=files,
                headers={
                    'Accept': 'application/vnd.collection+json',
                    'Content-Type': None
                }
            )
        res.raise_for_status()
        return res.json()

    def get_plugin(self, name_exact='', version='', url=''):
        """
        Get a single plugin, either searching for it by its exact name, or by URL.
        :param name_exact: name of plugin
        :param version: (optional) version of plugin
        :param url: (alternative to name_exact) url of plugin
        :return:
        """
        if name_exact:
            search = self.search_plugin(name_exact, version)
            return search[0]
        elif url:
            res = self.s.get(url)
            res.raise_for_status()
            data = res.json()
            return data
        else:
            raise ValueError('Must give either plugin name or url')

    def search_plugin(self, name_exact: str, version: ''):
        payload = {
            'name_exact': name_exact
        }
        if version:
            payload['version'] = version
        res = self.s.get(self.search_addr, params=payload)
        res.raise_for_status()
        data = res.json()
        if data['count'] < 1:
            raise PluginNotFoundError(name_exact)
        return data['results']

    def run(self, plugin_name='', plugin_url='', params: dict = None) -> PluginInstance:
        """
        Create a plugin instance.
        :param plugin_name: name of plugin to run
        :param plugin_url: alternatively specify plugin URL
        :param params: plugin parameters as key-value pairs (not collection+json)
        :return:
        """
        if params is None:
            params = {}

        pl = self.get_plugin(plugin_name, plugin_url)
        payload = collection_helper(params)

        res = self.s.post(pl['instances'], json=payload)
        res.raise_for_status()
        result = res.json()
        return PluginInstance(**result, session=self.s)

    def get_uploadedfiles(self, fname='', fname_exact=''):
        query = {}
        if fname:
            query['fname'] = fname
        if fname_exact:
            query['fname_exact'] = fname_exact

        res = self.s.get(self.collection_links['uploadedfiles'] + 'search/', params=query).json()
        return res['results']
