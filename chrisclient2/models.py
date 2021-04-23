import requests
from chrisclient2.util import collection_helper


class Feed:
    def __init__(self, session: requests.Session, feed_url):
        self.s = session
        self.url = feed_url

        res = self.s.get(feed_url).json()
        self._note_url = res['note']

    def set_name(self, name):
        payload = collection_helper({'name': name})
        res = self.s.put(self.url, json=payload)
        res.raise_for_status()
        return res

    def set_description(self, description):
        payload = collection_helper({
            'title': 'Description',
            'content': description
        })
        res = self.s.put(self._note_url, json=payload)
        res.raise_for_status()
        return res


class PluginInstance:
    def __init__(self, url: str, id: int, title: str, feed: str, session: requests.Session, **kwargs):
        self.url = url
        self.id = id
        self.title = title
        self.feed = feed
        self._session = session

    def get_feed(self):
        return Feed(session=self._session, feed_url=self.feed)
