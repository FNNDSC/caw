responses = {
    'https://example.com/api/v1/something/': {
        'count': 5,
        'next': 'https://example.com/api/v1/something/?limit=3&offset=3',
        'previous': None,
        'results': [
            {'id': 1}, {'id': 2}, {'id': 3}
        ],
        'collection_links': {}
    },
    'https://example.com/api/v1/something/?limit=3&offset=3': {
        'count': 5,
        'next': 'https://example.com/api/v1/something/?limit=3&offset=6',
        'previous': 'https://example.com/api/v1/something/?limit=3',
        'results': [
            {'id': 4}, {'id': 5}, {'id': 6}
        ],
        'collection_links': {}
    },
    'https://example.com/api/v1/something/?limit=3&offset=6': {
        'count': 5,
        'next': None,
        'previous': 'https://example.com/api/v1/something/?limit=3',
        'results': [
            {'id': 7}, {'id': 8}
        ],
        'collection_links': {}
    },
}
