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

    def get_plugin(self, plugin_name):
        payload = {
            'name_exact': plugin_name
        }
        res = self.s.get(self.search_addr, params=payload)
        res.raise_for_status()
        data = res.json()
        if data['count'] < 1:
            raise PluginNotFoundError(plugin_name)
        return data['results'][0]  # is first result always latest version?

    def run(self, plugin_name, params: dict = None) -> PluginInstance:
        """
        Create a plugin instance.
        :param plugin_name: name of plugin to run
        :param params: plugin parameters as key-value pairs (not collection+json)
        :return:
        """
        if params is None:
            params = {}

        pl = self.get_plugin(plugin_name)

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
