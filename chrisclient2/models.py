import requests
from chrisclient2.util import collection_helper, PaginationNotImplementedException
from typing import Optional, Set, List


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


class Piping:
    """
    A node of a directed acyclic graph representation of a pipeline.
    """
    def __init__(self, id: int, pipeline: str, pipeline_id: int, plugin: str, plugin_id: int, url: str,
                 default_parameters: List[dict], previous: Optional[str], previous_id: Optional[int] = None):
        self.id = id
        self.pipeline = pipeline
        self.pipeline_id = pipeline_id
        self.plugin = plugin
        self.plugin_id = plugin_id
        self.url = url
        self.previous = previous
        self.previous_id = previous_id
        self.next: Set['Piping'] = set()
        self.parent: Optional['Piping'] = None
        self.default_parameters = default_parameters

    def __hash__(self):
        return hash((self.id, self.pipeline_id))

    def add_child(self, child: 'Piping'):
        self.next.add(child)


class PipelineAssemblyException(Exception):
    """
    Pipeline JSON representation cannot be reassembled as a Piping DAG.
    """
    pass


class PipelineHasMultipleRootsException(PipelineAssemblyException):
    """
    Multiple pipings with 'previous': null were found in the pipeline JSON representation.
    """
    pass


class PipelineRootNotFoundException(PipelineAssemblyException):
    """
    No piping found in the pipelines JSON representation with 'previous': null.
    """
    pass


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

    def assemble(self) -> Piping:
        """
        Convert the responses from CUBE to a DAG with parent --> child relationships
        (whereas CUBE's response represents a pipeline via child --> parent relationships
        through the previous key) and couples parameter info with plugin info.
        :return: DAG
        """

        # collect all default parameters
        assembled_params = {}
        for param_info in self.get_default_parameters():
            i = param_info['plugin_piping_id']
            if i not in assembled_params:
                assembled_params[i] = []
            assembled_params[i].append({
                param_info['param_name']: param_info['value']
            })

        pipings = {}
        root = None

        # create DAG nodes
        for piping_info in self.get_pipings():
            i = piping_info['id']
            if i in assembled_params:
                params = assembled_params[i]
            else:
                params = []
            piping = Piping(**piping_info, default_parameters=params)
            if not piping.previous:
                if root:
                    raise PipelineHasMultipleRootsException()
                root = piping
            pipings[i] = piping
        if not root:
            raise PipelineRootNotFoundException()

        # create bidirectional DAG edges
        for _, piping in pipings.items():
            i = piping.previous_id
            if not i:
                continue
            pipings[i].add_child(piping)
            piping.parent = pipings[i]

        return root
