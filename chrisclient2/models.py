import requests
from chrisclient2.util import collection_helper, PaginationNotImplementedException


class Feed:
    def __init__(self, session: requests.Session, feed_url):
        self._s = session
        self.url = feed_url

        res = self._s.get(feed_url).json()
        self._note_url = res['note']

    def set_name(self, name):
        payload = collection_helper({'name': name})
        res = self._s.put(self.url, json=payload)
        res.raise_for_status()
        return res.json()

    def set_description(self, description):
        payload = collection_helper({
            'title': 'Description',
            'content': description
        })
        res = self._s.put(self._note_url, json=payload)
        res.raise_for_status()
        return res.json()


class PluginInstance:
    def __init__(self, url: str, id: int, title: str, feed: str, session: requests.Session, **kwargs):
        self.url = url
        self.id = id
        self.title = title
        self.feed = feed
        self._session = session

    def get_feed(self):
        return Feed(session=self._session, feed_url=self.feed)


class Pipeline:
    def __init__(self, authors: str, description: str, name: str,
                 plugin_pipings: str, default_parameters: str, plugins: str, url: str,
                 session: requests.Session, **kwargs):
        self.authors = authors
        self.description = description
        self.name = name
        self.plugin_pipings = plugin_pipings
        self.default_parameters = default_parameters
        self.plugins = plugins
        self.url = url
        self._session = session

    def _do_get(self, url):
        res = self._session.get(url, params={'limit': 50, 'offset': 0})
        res.raise_for_status()
        data = res.json()
        if data['next']:
            raise PaginationNotImplementedException()
        return data['results']

    def get_pipings(self):
        return self._do_get(self.plugin_pipings)

    def get_default_parameters(self):
        return self._do_get(self.default_parameters)
