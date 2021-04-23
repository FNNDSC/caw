class PaginationNotImplementedException(Exception):
    pass


def collection_helper(obj: dict) -> dict:
    return {
        'template': {
            'data': [{'name': k, 'value': v} for k, v in obj.items()]
        }
    }

